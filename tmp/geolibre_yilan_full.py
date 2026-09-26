#!/usr/bin/env python3
import csv, hashlib, io, json, math, os, sys, time, zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import Point, mapping, shape

OUT = Path('tmp/geolibre-yilan-full-output')
OUT.mkdir(parents=True, exist_ok=True)

VALHALLA = os.environ.get('VALHALLA_URL', 'http://127.0.0.1:8002').rstrip('/')
SESSION = requests.Session()
SESSION.headers.update({'User-Agent':'GeoLibre-Yilan-Acceptance-Recovery/1.0','X-Client-Id':'geolibre-yilan-audit-recovery'})

SOURCES = {
    'bikeway_zip': 'https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/906489F2-EFA0-493D-949D-191A46D0B9E4/resource/3E3DF490-AFB4-44EB-B298-8B964473B559/download',
    'minstat_zip': 'https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/03C1D0A5-1F39-4C1F-AA2E-BB37A0405369/resource/B3D71406-1E59-4FA6-AAA1-1211071AF6AF/download',
    'minstat_population_xml': 'https://segisws.moi.gov.tw/STATWSSTData/OpenService.asmx/GetStatSTDataForOpenCode?oCode=6E03CA29B955A854397166638603FC3B51A1FBEE829C41DBA1D61A4DBA84DCB4E4BD6BD69354D4F327594B53FA160158A46DEC5BF5F23516',
    'schools': 'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/73af13a7a027ef3f3813402aef9525d1535cb3b2/public/schools.geojson',
    'markets': 'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/master/public/poi/public_retail_markets_national.geojson',
    'gov': 'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/master/public/civic_facilities/gov_service_offices_national.geojson',
    'bus': 'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/master/public/bus/yilancounty_bus_routes.json',
}

CURRENT_POP = {
    '宜蘭市':93972,'羅東鎮':68284,'蘇澳鎮':36241,'頭城鎮':27950,'礁溪鄉':36483,'壯圍鄉':24549,
    '員山鄉':32290,'冬山鄉':52859,'五結鄉':41689,'三星鄉':21487,'大同鄉':6039,'南澳鄉':6222,
}

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def fetch_bytes(name, url, timeout=120):
    r=SESSION.get(url, timeout=timeout); r.raise_for_status(); b=r.content
    return b, {'url':url,'final_url':r.url,'http_status':r.status_code,'bytes':len(b),'sha256':sha256_bytes(b),'content_type':r.headers.get('content-type')}

def save_geojson(gdf, path):
    gdf = gdf.to_crs(4326)
    path.write_text(gdf.to_json(drop_id=True), encoding='utf-8')

def prop_first(props, names):
    for n in names:
        if n in props and props[n] not in (None,''): return props[n]
    return None

def facility_inputs(source_blobs):
    out=[]
    sch=json.loads(source_blobs['schools'].decode('utf-8'))['features']
    for f in sch:
        p=f.get('properties',{})
        if p.get('city')=='宜蘭縣' and f.get('geometry',{}).get('type')=='Point':
            out.append({'facility_id':f"school:{p.get('code') or len(out)}",'category':'school','name':p.get('school_name') or '學校','lon':f['geometry']['coordinates'][0],'lat':f['geometry']['coordinates'][1],'source':'school_snapshot_20260304'})
    mk=json.loads(source_blobs['markets'].decode('utf-8'))['features']
    for i,f in enumerate(mk):
        p=f.get('properties',{})
        if p.get('county')=='宜蘭縣' and f.get('geometry',{}).get('type')=='Point':
            out.append({'facility_id':f"market:{i}",'category':'market','name':p.get('name') or '市場','lon':f['geometry']['coordinates'][0],'lat':f['geometry']['coordinates'][1],'source':'market_snapshot'})
    gv=json.loads(source_blobs['gov'].decode('utf-8'))['features']
    for i,f in enumerate(gv):
        p=f.get('properties',{})
        if p.get('county')=='宜蘭縣' and f.get('geometry',{}).get('type')=='Point':
            out.append({'facility_id':f"gov:{i}",'category':'government','name':p.get('name') or '政府服務據點','lon':f['geometry']['coordinates'][0],'lat':f['geometry']['coordinates'][1],'source':'gov_snapshot'})
    return out

def valhalla_status():
    r=SESSION.get(VALHALLA+'/status',timeout=20); r.raise_for_status(); return r.json()

def iso_1km(fac, retries=3):
    payload={'locations':[{'lat':fac['lat'],'lon':fac['lon']}], 'costing':'pedestrian','contours':[{'distance':1.0}],'polygons':True,'show_locations':True,'denoise':0.5,'generalize':20}
    last=None
    for attempt in range(retries):
        try:
            r=SESSION.get(VALHALLA+'/isochrone', params={'json':json.dumps(payload,separators=(',',':'))}, timeout=45)
            if r.ok:
                gj=r.json(); polys=[f for f in gj.get('features',[]) if f.get('geometry',{}).get('type') in ('Polygon','MultiPolygon')]
                if polys:
                    chosen=next((f for f in polys if abs(float(f.get('properties',{}).get('contour',1))-1)<1e-6),polys[0])
                    return chosen, None
            last=f"HTTP {r.status_code}: {r.text[:300]}"
        except Exception as e: last=repr(e)
        time.sleep(1.0*(attempt+1))
    return None,last

def parse_minstat(shp_bytes, pop_xml_bytes):
    d=OUT/'minstat_src'; d.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(shp_bytes)) as z: z.extractall(d)
    shp=next(d.glob('*.shp'))
    g=gpd.read_file(shp)
    code_col=next((c for c in g.columns if c.upper()=='CODEBASE'),None)
    if not code_col:
        code_col=next((c for c in g.columns if 'CODE' in c.upper()),None)
    if not code_col: raise RuntimeError(f'No minstat code field. columns={list(g.columns)}')
    g[code_col]=g[code_col].astype(str).str.strip()
    root=ET.fromstring(pop_xml_bytes)
    rows=[]
    for rd in root.findall('.//RowData'):
        rec={child.tag:(child.text or '').strip() for child in rd}
        rows.append(rec)
    p=pd.DataFrame(rows)
    for c in ['H_CNT','P_CNT','M_CNT','F_CNT']:
        if c in p.columns: p[c]=pd.to_numeric(p[c],errors='coerce').fillna(0)
    p['CODEBASE']=p['CODEBASE'].astype(str).str.strip()
    j=g.merge(p[['INFO_TIME','CODEBASE','H_CNT','P_CNT','M_CNT','F_CNT']],left_on=code_col,right_on='CODEBASE',how='left')
    town_col=next((c for c in j.columns if c.upper() in {'TOWN','TOWNNAME'}),None)
    if town_col:
        j[town_col]=j[town_col].astype(str).str.replace('宜蘭縣','',regex=False).str.strip()
        j['P_EST_2026_08']=j['P_CNT'].astype(float)
        for town,total in CURRENT_POP.items():
            mask=j[town_col].eq(town)
            base=float(j.loc[mask,'P_CNT'].sum())
            if base>0: j.loc[mask,'P_EST_2026_08']=j.loc[mask,'P_CNT']*(total/base)
    else:
        j['P_EST_2026_08']=j['P_CNT'].astype(float)
    join_rate=float(j['P_CNT'].notna().mean())
    return j, {'shp_feature_count':len(g),'population_row_count':len(p),'join_rate':join_rate,'code_field':code_col,'town_field':town_col,'population_info_times':sorted(p['INFO_TIME'].dropna().unique().tolist())[:10]}

def parse_bikeway(b):
    feats=[]; member_names=[]
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        member_names=z.namelist()
        for n in member_names:
            if n.lower().endswith('.geojson'):
                obj=json.loads(z.read(n).decode('utf-8-sig'))
                feats.extend(obj.get('features',[]))
    y=[]; city_keys=set(); city_values=set()
    for f in feats:
        p=f.get('properties',{})
        city=prop_first(p,['CITY','City','city','COUNTY','County','county','縣市'])
        if city is not None: city_values.add(str(city))
        for k in p:
            if 'CITY' in k.upper() or 'COUNTY' in k.upper(): city_keys.add(k)
        if str(city).strip() in {'宜蘭縣','宜兰县','Yilan County'}:
            y.append(f)
    if not y:
        for f in feats:
            try:
                ge=shape(f['geometry']); x1,y1,x2,y2=ge.bounds
                if x2>=121.45 and x1<=122.05 and y2>=24.3 and y1<=25.1: y.append(f)
            except Exception: pass
    g=gpd.GeoDataFrame.from_features(y,crs=4326)
    return g, {'all_features':len(feats),'yilan_features':len(g),'zip_members':member_names,'city_keys':sorted(city_keys),'city_values_sample':sorted(city_values)[:50]}

def interpolate(route,progress):
    target=max(0,min(1,float(progress)))*float(route.get('totalDist') or 0)
    cd=route.get('cumDist') or []; cc=route.get('coords') or []
    if not cd or not cc: return None
    lo,hi=0,len(cd)-1
    while lo<hi:
        m=(lo+hi)//2
        if cd[m]<target: lo=m+1
        else: hi=m
    i=max(1,lo); d0,d1=float(cd[i-1]),float(cd[i]); t=(target-d0)/(d1-d0) if d1>d0 else 0
    return [cc[i-1][0]+(cc[i][0]-cc[i-1][0])*t, cc[i-1][1]+(cc[i][1]-cc[i-1][1])*t]

def hav(a,b):
    R=6371008.8; d=math.pi/180; p1=a[1]*d;p2=b[1]*d; dp=(b[1]-a[1])*d;dl=(b[0]-a[0])*d
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(min(1,math.sqrt(h)))

def parse_bus(b):
    routes=json.loads(b.decode('utf-8'))
    raw=[]
    for key,rt in routes.items():
        sp=rt.get('stopProgress') or []; sn=rt.get('stopNames') or []
        freq=float(rt.get('frequency') or 0)
        for i in range(min(len(sp),len(sn))):
            c=interpolate(rt,sp[i])
            if c: raw.append({'name':sn[i],'coord':c,'route_uid':rt.get('routeUid'),'direction':rt.get('direction'),'frequency':freq})
    byname=defaultdict(list); clusters=[]
    for s in raw:
        hit=None
        for idx in byname[s['name']]:
            if hav(clusters[idx]['coord'],s['coord'])<=80: hit=idx; break
        if hit is None:
            idx=len(clusters); byname[s['name']].append(idx)
            clusters.append({'name':s['name'],'coord':s['coord'][:], 'n':1, 'services':{(s['route_uid'],s['direction']):s['frequency']}})
        else:
            c=clusters[hit]; n=c['n']; c['coord']=[(c['coord'][0]*n+s['coord'][0])/(n+1),(c['coord'][1]*n+s['coord'][1])/(n+1)]; c['n']=n+1; c['services'][(s['route_uid'],s['direction'])]=s['frequency']
    feats=[]; freq_known=0
    for i,c in enumerate(clusters):
        freq=sum(v for v in c['services'].values() if v is not None)
        if freq>0: freq_known+=1
        feats.append({'type':'Feature','geometry':{'type':'Point','coordinates':c['coord']},'properties':{'stop_cluster_id':i,'name':c['name'],'route_direction_count':len(c['services']),'service_frequency_per_hour':round(freq,3),'raw_occurrences':c['n']}})
    return {'type':'FeatureCollection','features':feats},{'route_variants':len(routes),'raw_stop_occurrences':len(raw),'stop_clusters':len(clusters),'clusters_with_frequency':freq_known,'frequency_coverage':freq_known/len(clusters) if clusters else 0}

def main():
    evidence={'generated_at':datetime.now(timezone.utc).isoformat(),'sources':{},'routing':{},'checks':{}}
    blobs={}
    for name,url in SOURCES.items():
        b,meta=fetch_bytes(name,url); blobs[name]=b; evidence['sources'][name]=meta
    status=valhalla_status(); evidence['routing']['status']=status; evidence['routing']['endpoint']=VALHALLA
    facs=facility_inputs(blobs)
    fac_feats=[{'type':'Feature','geometry':{'type':'Point','coordinates':[f['lon'],f['lat']]},'properties':{k:v for k,v in f.items() if k not in ('lon','lat')}} for f in facs]
    (OUT/'facility_points.geojson').write_text(json.dumps({'type':'FeatureCollection','features':fac_feats},ensure_ascii=False),encoding='utf-8')
    isofs=[]; failures=[]
    for idx,f in enumerate(facs,1):
        poly,err=iso_1km(f)
        if poly:
            props=dict(poly.get('properties') or {}); props.update({k:v for k,v in f.items() if k not in ('lon','lat')}); props['network_distance_m']=1000
            isofs.append({'type':'Feature','geometry':poly['geometry'],'properties':props})
        else:
            failures.append({'facility_id':f['facility_id'],'name':f['name'],'category':f['category'],'error':err})
        if idx%25==0: print(f'isochrones {idx}/{len(facs)} success={len(isofs)} fail={len(failures)}', flush=True)
    (OUT/'facility_isochrones_1km.geojson').write_text(json.dumps({'type':'FeatureCollection','features':isofs},ensure_ascii=False),encoding='utf-8')
    (OUT/'routing_failures.json').write_text(json.dumps(failures,ensure_ascii=False,indent=2),encoding='utf-8')
    route_rate=len(isofs)/len(facs) if facs else 0
    evidence['routing'].update({'facility_count':len(facs),'isochrone_success':len(isofs),'isochrone_failures':len(failures),'success_rate':route_rate})
    bike,bmeta=parse_bikeway(blobs['bikeway_zip']); save_geojson(bike,OUT/'bikeway_yilan.geojson'); evidence['checks']['bikeway']=bmeta
    minstat,mmeta=parse_minstat(blobs['minstat_zip'],blobs['minstat_population_xml']); save_geojson(minstat,OUT/'minstat_population_yilan.geojson'); evidence['checks']['minstat']=mmeta
    bus,bmeta=parse_bus(blobs['bus']); (OUT/'bus_stop_service.geojson').write_text(json.dumps(bus,ensure_ascii=False),encoding='utf-8'); evidence['checks']['bus']=bmeta
    gates={
      'routing_1km': route_rate>=0.98,
      'bikeway_geometry': len(bike)>0,
      'minstat_population_join': mmeta['join_rate']>=0.98,
      'bus_stop_frequency': bmeta['frequency_coverage']>=0.95,
      'facility_categories': all(any(f['category']==c for f in facs) for c in ['school','market','government']),
    }
    evidence['checks']['gates']=gates
    evidence['analysis_inputs_ready']=all(gates.values())
    (OUT/'acceptance-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'analysis_inputs_ready':evidence['analysis_inputs_ready'],'gates':gates,'routing':evidence['routing'],'bikeway':bmeta,'minstat':mmeta,'bus':bmeta},ensure_ascii=False,indent=2))
    if not evidence['analysis_inputs_ready']: sys.exit(2)

if __name__=='__main__': main()
