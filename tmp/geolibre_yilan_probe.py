import json, zipfile, io, hashlib, sys, os, traceback
from pathlib import Path
import requests

OUT=Path('tmp/geolibre-yilan-probe-output'); OUT.mkdir(parents=True,exist_ok=True)
SOURCES={
'bikeway_zip':'https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/906489F2-EFA0-493D-949D-191A46D0B9E4/resource/3E3DF490-AFB4-44EB-B298-8B964473B559/download',
'minstat_zip':'https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/03C1D0A5-1F39-4C1F-AA2E-BB37A0405369/resource/B3D71406-1E59-4FA6-AAA1-1211071AF6AF/download',
'minstat_population_xml':'https://segisws.moi.gov.tw/STATWSSTData/OpenService.asmx/GetStatSTDataForOpenCode?oCode=6E03CA29B955A854397166638603FC3B51A1FBEE829C41DBA1D61A4DBA84DCB4E4BD6BD69354D4F327594B53FA160158A46DEC5BF5F23516',
'schools':'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/73af13a7a027ef3f3813402aef9525d1535cb3b2/public/schools.geojson',
'markets':'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/master/public/poi/public_retail_markets_national.geojson',
'gov':'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/master/public/civic_facilities/gov_service_offices_national.geojson',
'bus':'https://raw.githubusercontent.com/ianlkl11234s/mini-taiwan-pulse/master/public/bus/yilancounty_bus_routes.json',
}
report={'sources':{},'valhalla':{}}
s=requests.Session(); s.headers.update({'User-Agent':'GeoLibre-Yilan-Acceptance-Probe/1.0','X-Client-Id':'geolibre-yilan-audit-probe'})
for name,url in SOURCES.items():
    try:
        r=s.get(url,timeout=90); info={'status':r.status_code,'content_type':r.headers.get('content-type'),'bytes':len(r.content),'final_url':r.url,'sha256':hashlib.sha256(r.content).hexdigest()}
        if r.ok and (name.endswith('_zip') or 'zip' in (r.headers.get('content-type') or '').lower()):
            try:
                z=zipfile.ZipFile(io.BytesIO(r.content)); info['zip_members']=z.namelist()[:100]; info['zip_count']=len(z.namelist())
            except Exception as e: info['zip_error']=repr(e)
        if name.endswith('_xml') or 'xml' in (r.headers.get('content-type') or '').lower():
            info['text_head']=r.text[:3000]
        if name in {'schools','markets','gov','bus'} and r.ok:
            obj=r.json()
            if isinstance(obj,dict) and obj.get('type')=='FeatureCollection':
                feats=obj['features']; info['feature_count']=len(feats)
                if name=='schools': info['yilan_count']=sum(1 for f in feats if f.get('properties',{}).get('city')=='宜蘭縣')
                elif name in {'markets','gov'}: info['yilan_count']=sum(1 for f in feats if f.get('properties',{}).get('county')=='宜蘭縣')
            elif name=='bus': info['route_variants']=len(obj)
        report['sources'][name]=info
        (OUT/f'{name}.head.txt').write_text((info.get('text_head') or str(info))[:5000],encoding='utf-8')
    except Exception as e:
        report['sources'][name]={'error':repr(e),'trace':traceback.format_exc()[-2000:]}

for host in ['https://valhalla1.openstreetmap.de','https://valhalla.openstreetmap.de']:
    try:
        st=s.get(host+'/status',timeout=60)
        h={'status_http':st.status_code,'status_text':st.text[:1000]}
        payload={'locations':[{'lat':24.751986,'lon':121.753397}], 'costing':'pedestrian','contours':[{'distance':1.0}],'polygons':True,'show_locations':True,'denoise':0.5}
        iso=s.get(host+'/isochrone',params={'json':json.dumps(payload,separators=(',',':'))},timeout=90)
        h.update({'iso_http':iso.status_code,'iso_bytes':len(iso.content),'iso_type':iso.headers.get('content-type')})
        if iso.ok:
            gj=iso.json(); h['feature_count']=len(gj.get('features',[])); h['bbox']=gj.get('bbox'); (OUT/'valhalla_1km.geojson').write_text(json.dumps(gj,ensure_ascii=False,indent=2),encoding='utf-8')
        else: h['iso_text']=iso.text[:1500]
        report['valhalla'][host]=h
        if iso.ok: break
    except Exception as e: report['valhalla'][host]={'error':repr(e)}

(OUT/'probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
val_ok=any(v.get('iso_http')==200 for v in report['valhalla'].values())
key_ok=all(report['sources'].get(k,{}).get('status')==200 for k in ['bikeway_zip','minstat_zip','minstat_population_xml'])
print('VAL_OK',val_ok,'KEY_OK',key_ok)
if not (val_ok and key_ok): sys.exit(2)
