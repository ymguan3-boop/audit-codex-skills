#!/usr/bin/env python3
import json, os
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import force_2d
from shapely.ops import unary_union

SRC=Path(os.environ.get("INPUT_DIR","tmp/geolibre-yilan-full-output"))
OUT=Path("public/geolibre/yilan-short-trip-20260926")
LAY=OUT/"layers"
LAY.mkdir(parents=True,exist_ok=True)
CRS_M=3826
RAW_BASE="https://raw.githubusercontent.com/ymguan3-boop/audit-codex-skills/main/public/geolibre/yilan-short-trip-20260926"

mins=gpd.read_file(SRC/"minstat_population_yilan.geojson")
iso=gpd.read_file(SRC/"facility_isochrones_1km.geojson")
fac=gpd.read_file(SRC/"facility_points.geojson")
bike=gpd.read_file(SRC/"bikeway_yilan.geojson")
bus=gpd.read_file(SRC/"bus_stop_service.geojson")

mins["geometry"]=mins.geometry.apply(force_2d)
mins_m=mins.to_crs(CRS_M)
iso_m=iso.to_crs(CRS_M)
bike_m=bike.to_crs(CRS_M)
bus_m=bus.to_crs(CRS_M)

iso_union=unary_union(iso_m.geometry)
mins_m["area_m2"]=mins_m.geometry.area
mins_m["network_access_area_m2"]=mins_m.geometry.intersection(iso_union).area
mins_m["network_access_ratio"]=(mins_m["network_access_area_m2"]/mins_m["area_m2"]).fillna(0).clip(0,1)
mins_m["pop_est"]=pd.to_numeric(mins_m["P_EST_2026_08"],errors="coerce").fillna(0)
mins_m["pop_density_km2"]=np.where(mins_m["area_m2"]>0,mins_m["pop_est"]/(mins_m["area_m2"]/1_000_000),0)
mins_m["rep_geom"]=mins_m.geometry.representative_point()
cand=mins_m[(mins_m["pop_est"]>0)&(mins_m["network_access_ratio"]>0)].copy()
rep=gpd.GeoDataFrame(cand[["CODEBASE"]].copy(),geometry=cand["rep_geom"],crs=CRS_M)

nb=gpd.sjoin_nearest(rep,bus_m[["stop_cluster_id","name","service_frequency_per_hour","geometry"]],how="left",distance_col="nearest_bus_dist_m")
nb=nb.sort_values(["CODEBASE","nearest_bus_dist_m"]).drop_duplicates("CODEBASE").rename(columns={"name":"nearest_bus_stop"})
nbi=gpd.sjoin_nearest(rep,bike_m[["NAME","geometry"]],how="left",distance_col="nearest_bike_dist_m")
nbi=nbi.sort_values(["CODEBASE","nearest_bike_dist_m"]).drop_duplicates("CODEBASE").rename(columns={"NAME":"nearest_bikeway"})

hits=gpd.sjoin(cand[["CODEBASE","geometry"]],iso_m[["facility_id","category","geometry"]],predicate="intersects",how="left")
fc=hits.groupby("CODEBASE").agg(
 facility_iso_intersections=("facility_id",lambda s:int(s.notna().sum())),
 school_iso_intersections=("category",lambda s:int((s=="school").sum())),
 market_iso_intersections=("category",lambda s:int((s=="market").sum())),
 government_iso_intersections=("category",lambda s:int((s=="government").sum())),
).reset_index()

cand=cand.merge(nb[["CODEBASE","nearest_bus_dist_m","nearest_bus_stop","service_frequency_per_hour"]],on="CODEBASE",how="left")
cand=cand.merge(nbi[["CODEBASE","nearest_bike_dist_m","nearest_bikeway"]],on="CODEBASE",how="left")
cand=cand.merge(fc,on="CODEBASE",how="left")
for c in ["facility_iso_intersections","school_iso_intersections","market_iso_intersections","government_iso_intersections"]:
    cand[c]=cand[c].fillna(0).astype(int)

def pct(s): return s.rank(pct=True,method="average")
cand["population_benefit_score"]=((pct(cand["pop_density_km2"])+pct(cand["pop_est"]))/2)*100
cand["walkable_destination_score"]=((pct(cand["network_access_ratio"])+pct(cand["facility_iso_intersections"]))/2)*100
cand["bus_gap_score"]=((pct(cand["nearest_bus_dist_m"])+(1-pct(cand["service_frequency_per_hour"])))/2)*100
cand["bike_gap_score"]=pct(cand["nearest_bike_dist_m"])*100
cand["score"]=cand[["population_benefit_score","walkable_destination_score","bus_gap_score","bike_gap_score"]].mean(axis=1)
q25,q50,q75=cand["score"].quantile([.25,.5,.75]).tolist()
def cls(v):
    if v>=q75:return "高改善潛力"
    if v>=q50:return "中高改善潛力"
    if v>=q25:return "中改善潛力"
    return "低改善潛力"
cand["level"]=cand["score"].map(cls)

score_cols={"人口受益":"population_benefit_score","步行目的地可達":"walkable_destination_score","公車服務缺口":"bus_gap_score","自行車路網缺口":"bike_gap_score"}
def factors(row):
    a=sorted(((k,float(row[v])) for k,v in score_cols.items()),key=lambda x:x[1],reverse=True)
    return "、".join(x[0] for x in a[:2])
cand["main_factor"]=cand.apply(factors,axis=1)
cand["人口估計_2026_08"]=cand["pop_est"].round(2)
cand["1km路網覆蓋率_pct"]=(cand["network_access_ratio"]*100).round(2)
cand["最近公車站距離_m"]=cand["nearest_bus_dist_m"].round(1)
cand["最近公車服務頻率_班每小時"]=cand["service_frequency_per_hour"].round(3)
cand["最近自行車道距離_m"]=cand["nearest_bike_dist_m"].round(1)
cand["改善潛力分數"]=cand["score"].round(2)
cand["改善潛力等級"]=cand["level"]
cand["主要改善面向"]=cand["main_factor"]

keep=["CODEBASE","TOWN","人口估計_2026_08","1km路網覆蓋率_pct","facility_iso_intersections",
      "nearest_bus_stop","最近公車站距離_m","最近公車服務頻率_班每小時",
      "nearest_bikeway","最近自行車道距離_m","改善潛力分數","改善潛力等級","主要改善面向","geometry"]
compact=cand[keep].copy()
compact["geometry"]=compact.geometry.simplify(12,preserve_topology=True)
compact=compact.to_crs(4326)

files={}
for lvl,fn in [("高改善潛力","high.geojson"),("中高改善潛力","mid-high.geojson"),("中改善潛力","mid.geojson"),("低改善潛力","low.geojson")]:
    g=compact[compact["改善潛力等級"]==lvl]
    p=LAY/fn
    p.write_text(json.dumps(json.loads(g.to_json(drop_id=True)),ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    files[lvl]=fn

# Supporting layers
fac_out=fac.to_crs(4326)
(LAY/"facilities.geojson").write_text(json.dumps(json.loads(fac_out.to_json(drop_id=True)),ensure_ascii=False,separators=(",",":")),encoding="utf-8")
bike_out=bike.to_crs(4326)
(LAY/"bikeway.geojson").write_text(json.dumps(json.loads(bike_out.to_json(drop_id=True)),ensure_ascii=False,separators=(",",":")),encoding="utf-8")
bus_keep=bus[["stop_cluster_id","name","route_direction_count","service_frequency_per_hour","geometry"]].to_crs(4326)
(LAY/"bus-stops.geojson").write_text(json.dumps(json.loads(bus_keep.to_json(drop_id=True)),ensure_ascii=False,separators=(",",":")),encoding="utf-8")
iso_keep=iso[["facility_id","category","name","network_distance_m","geometry"]].copy().to_crs(CRS_M)
iso_keep["geometry"]=iso_keep.geometry.simplify(10,preserve_topology=True)
iso_keep=iso_keep.to_crs(4326)
(LAY/"isochrones-1km.geojson").write_text(json.dumps(json.loads(iso_keep.to_json(drop_id=True)),ensure_ascii=False,separators=(",",":")),encoding="utf-8")

def vector_layer(id_,name,url,style,visible=True):
    return {
      "id":id_,"name":name,"type":"geojson","visible":visible,"opacity":1,
      "style":style,
      "source":{"type":"geojson","url":url},
      "sourcePath":url,
      "metadata":{
        "sourceKind":"maplibre-gl-vector","externalNativeLayer":True,
        "controlOwnsPaint":True,"identifiable":False,"nativeLayerIds":[],
        "sourceIds":[f"{id_}-source"],"vectorSource":"url",
        "vectorState":{"renderMode":"geojson","format":"GeoJSON","picker":True}
      }
    }

project={"version":"0.1.0","name":"宜蘭縣短程非汽車運具改善潛力分析",
 "mapView":{"center":[121.75,24.68],"zoom":9.15,"bearing":0,"pitch":0},
 "basemapStyleUrl":"https://tiles.openfreemap.org/styles/liberty","basemapVisible":True,"basemapOpacity":1,
 "layers":[],"styles":{},"metadata":{
   "taskId":"geolibre-yilan-short-trip-formal-20260926",
   "formalResultCount":int(len(compact)),"highPotentialCount":int((compact["改善潛力等級"]=="高改善潛力").sum()),
   "networkThreshold":"1 km pedestrian network distance",
   "publishedDataMode":"remote GeoJSON via anonymous HTTPS URLs"
 }}
styles={
 "high":{"fillColor":"#c2410c","strokeColor":"#7c2d12","strokeWidth":1.2,"fillOpacity":0.70},
 "midhigh":{"fillColor":"#f59e0b","strokeColor":"#92400e","strokeWidth":0.9,"fillOpacity":0.48},
 "mid":{"fillColor":"#84cc16","strokeColor":"#3f6212","strokeWidth":0.7,"fillOpacity":0.30},
 "low":{"fillColor":"#94a3b8","strokeColor":"#475569","strokeWidth":0.6,"fillOpacity":0.18},
 "fac":{"fillColor":"#2563eb","strokeColor":"#1e3a8a","strokeWidth":1,"fillOpacity":0.9,"circleRadius":4},
 "bike":{"strokeColor":"#0891b2","strokeWidth":2.3,"fillColor":"#0891b2","fillOpacity":0.0},
 "bus":{"fillColor":"#7c3aed","strokeColor":"#4c1d95","strokeWidth":0.8,"fillOpacity":0.75,"circleRadius":3},
 "iso":{"fillColor":"#38bdf8","strokeColor":"#0284c7","strokeWidth":0.8,"fillOpacity":0.08},
}
project["layers"]=[
 vector_layer("result-high","高改善潛力最小統計區",f"{RAW_BASE}/layers/high.geojson",styles["high"],True),
 vector_layer("result-mid-high","中高改善潛力最小統計區",f"{RAW_BASE}/layers/mid-high.geojson",styles["midhigh"],True),
 vector_layer("result-mid","中改善潛力最小統計區",f"{RAW_BASE}/layers/mid.geojson",styles["mid"],False),
 vector_layer("result-low","低改善潛力最小統計區",f"{RAW_BASE}/layers/low.geojson",styles["low"],False),
 vector_layer("facilities","生活設施點（學校／市場／政府服務）",f"{RAW_BASE}/layers/facilities.geojson",styles["fac"],True),
 vector_layer("bikeway","115年上半年自行車道",f"{RAW_BASE}/layers/bikeway.geojson",styles["bike"],True),
 vector_layer("bus-stops","公車站點群與服務頻率",f"{RAW_BASE}/layers/bus-stops.geojson",styles["bus"],False),
 vector_layer("isochrones-1km","生活設施1公里實際步行路網面",f"{RAW_BASE}/layers/isochrones-1km.geojson",styles["iso"],False),
]
project["styles"]={x["id"]:x["style"] for x in project["layers"]}
(OUT/"map.geolibre.json").write_text(json.dumps(project,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
manifest={"result_count":int(len(compact)),"high_count":int((compact["改善潛力等級"]=="高改善潛力").sum()),
          "q25":q25,"q50":q50,"q75":q75,
          "files":{p.name:p.stat().st_size for p in LAY.glob("*.geojson")}}
(OUT/"publish-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(manifest,ensure_ascii=False,indent=2))

# qa-rerun-trigger-20260926
