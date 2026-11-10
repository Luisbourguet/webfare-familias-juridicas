# -*- coding: utf-8 -*-
# Copyright 2026 the authors of "El Webfare en las familias jurídicas"
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Webfare en las familias jurídicas — análisis reproducible (sección IV-V del artículo)
Datos: CCP Characteristics of National Constitutions v5.0 (Elkins & Ginsburg, 2025), ccpcnc_v5_small.csv
       JuriGlobe (U. Ottawa; 2.ª ed. 2008; last updated 2024-07-24; consultado 2026-11-09), tabla limpia
Corte transversal: constitución en vigor en 2023 (year == 2023). Un país = una fila.
Recodificación: 1=sí->1; 2=no->0; 90 (remitido a ley ordinaria)->0 [no inscrito en la constitución]; 96 (otro)/98/nan->NA (por pares).
Muestra: constituciones con texto codificado en 2023 (se excluyen eventos de 2023 aún sin codificar, p. ej. Malí y Uzbekistán).
  OFFREL: 1 (religión oficial)->1; 2,3,90,98->0; 96->NA.  TREATST: 1 (tratados superiores)->1; 2,3,98->0; resto NA.
  INDPOLGR_1..7 (derechos políticos indígenas; opción múltiple 0/1): 99 (no preguntado: FEDERAL_3=0)->NA.  JUDPREC: 1->1; 98->0.
  INTERP_1..4 (intérprete de la constitución; opción múltiple 0/1, sin recodificar): INTERP_2 = tribunal o consejo constitucional;
  INTERP_3 = solo corte suprema; INTERP_1 = cualquier tribunal ordinario; INTERP_4 = sala especial de la corte suprema.
Medida de asociación: omega² (eta² ajustado por número de grupos). Se excluyen del perfil de fuentes
  las variables que luego se evalúan (evitar circularidad).
Uso: python3 analisis_webfare_ccp.py <ruta_carpeta_CCP_Update>
"""
import sys, re, unicodedata, pandas as pd, numpy as np
ccp_dir = sys.argv[1]

# ---------- 1. Cruce JuriGlobe -> CCP (cowcode) ----------
jg = pd.read_csv("juriglobe_all_entities_clean.csv")
ccp_all = pd.read_csv(f"{ccp_dir}/ccpcnc_v5_small.csv", usecols=["cowcode","country","year"], low_memory=False)
countries = (ccp_all.drop_duplicates("cowcode")[["cowcode","country"]]
             .merge(ccp_all.groupby("cowcode").year.max().rename("last_year"), on="cowcode"))
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii","ignore").decode().upper().replace("&","AND")
    s = re.sub(r"[^A-Z ]"," ",s); s = re.sub(r"\s+"," ",s).strip()
    return re.sub(r"^(THE|REPUBLIC OF|KINGDOM OF|STATE OF|FEDERAL REPUBLIC OF|PEOPLES REPUBLIC OF|DEMOCRATIC REPUBLIC OF|UNITED REPUBLIC OF) ","",s)
countries["key"] = countries.country.map(norm); jg["key"] = jg.entity.map(norm)
MANUAL = {'CONGO, POPULAR DEMOCRATIC':'Democratic Republic of the Congo','EAST TIMOR':'Timor','FIJI ISLANDS':'Fiji',
 'KOREA NORTH':'North Korea','KOREA SOUTH':'South Korea','KYRGYZSTAN':'Kyrgyz Republic','MACEDONIA':'North Macedonia',
 'MALDIVES ISLANDS':'Maldives','SAINT VINCENT AND THE GRANADINES':'Saint Vincent and the Grenadines','SLOVAKIA':'Slovak Republic',
 'SWAZILAND':'Eswatini','UNITED STATES OF AMERICA':'United States','YEMEN':'Yemen Arab Republic'}  # Yemen unificado continúa bajo COW 678
cw = jg.merge(countries, on="key", how="left"); cw["match"] = np.where(cw.cowcode.notna(),"auto","")
byname = countries.set_index("country")
for a,b in MANUAL.items():
    i = cw.index[cw.entity==a]
    if len(i) and b in byname.index:
        cw.loc[i,["cowcode","country","last_year"]] = [byname.loc[b,"cowcode"], b, byname.loc[b,"last_year"]]; cw.loc[i,"match"]="manual"
cw.loc[cw.cowcode.isna(),"match"] = "excluded_non_sovereign_or_absent"
cw = cw[cw.cowcode.notna()].copy(); cw["cowcode"] = cw.cowcode.astype(int)
cw.to_csv("cruce_juriglobe_ccp.csv", index=False)

# ---------- 2. Corte 2023 y recodificación ----------
cols = ["cowcode","country","year","systyear","infoacc","referen","voteun","privacy","census","federal_3","indpolgr_1","indpolgr_2","indpolgr_3","indpolgr_4","indpolgr_5","indpolgr_6","indpolgr_7",
        "indcit","offrel","god","treat","treatst","custlaw","interp_1","interp_2","interp_3","interp_4","judind","judprec","amndamaj","unamend"]
x = pd.read_csv(f"{ccp_dir}/ccpcnc_v5_small.csv", usecols=cols, low_memory=False); x = x[x.year==2023].copy()
yn = lambda s: s.map({1:1,2:0,90:0})
r = pd.DataFrame({"cowcode":x.cowcode,"country":x.country,"systyear":x.systyear,"coded_2023":x.infoacc.notna()})  # texto codificado en 2023 (96="otro" cuenta como codificado)
for v in ["infoacc","referen","voteun","privacy","census","god","treat","custlaw","judind"]: r[v]=yn(x[v])
r["indig_autonomy"]=x.federal_3                           # OJO: FEDERAL_3 = "grupos autónomos" en sentido amplio (étnico/lingüístico/regional), no solo indígena
r["indig_selfgov"]=x.indpolgr_6.replace({99:np.nan}); r["indig_cultural"]=x.indpolgr_7.replace({99:np.nan})
for k in range(1,8): r[f"indpolgr_{k}"]=x[f"indpolgr_{k}"].replace({99:np.nan})   # INDPOLGR_1-7, condicionadas a FEDERAL_3=1
r["offrel_official"]=x.offrel.map({1:1,2:0,3:0,90:0,98:0}); r["offrel_special_or_official"]=x.offrel.map({1:1,2:1,3:0,90:0,98:0})
r["treat_superior"]=x.treatst.map({1:1,2:0,3:0,98:0}); r["const_court_interprets"]=x.interp_2
r["supreme_court_interprets"]=x.interp_3; r["ordinary_courts_interpret"]=x.interp_1; r["supreme_chamber_interprets"]=x.interp_4
r["judprec"]=x.judprec.map({1:1,98:0}); r["supermajority_amend"]=yn(x.amndamaj); r["unamendable"]=yn(x.unamend)
d = cw.merge(r, on="cowcode", how="inner", suffixes=("_jg",""))
d["system"] = d.system.replace({"Civil law":"Civil","Common law":"Common","Customary law":"Customary","Muslim law":"Muslim"})
d["periodo"] = pd.cut(d.systyear,[0,1945,1989,2100],labels=["<1946","1946-1989","1990+"])
d["sources_profile"] = d[["offrel_official","treat_superior","const_court_interprets"]].astype("Int64").astype(str).agg("-".join,axis=1)
d.to_csv("dataset_2023_juriglobe_ccp.csv", index=False)
a = d[d.coded_2023].copy()   # muestra analítica; cada variable usa eliminación por pares de sus 96/98 (NaN)

# ---------- 3. Tablas ----------
def omega2(y,g):
    m = pd.DataFrame({"y":y,"g":g}).dropna()
    if m.g.nunique()<2: return np.nan
    gm=m.y.mean(); gr=[s for _,s in m.groupby("g",observed=True).y]; k=len(gr); N=len(m)
    ssb=sum(len(s)*(s.mean()-gm)**2 for s in gr); ssw=sum(((s-s.mean())**2).sum() for s in gr); sst=ssb+ssw
    msw=ssw/(N-k); return max(0,(ssb-(k-1)*msw)/(sst+msw)) if sst>0 else np.nan
G = ["infoacc","referen","voteun","privacy","census","indig_autonomy"]
T1 = a.groupby("system")[G+["const_court_interprets","treat_superior","offrel_official"]].mean().round(2); T1["n"]=a.groupby("system").size(); T1["anio_medio"]=a.groupby("system").systyear.mean().round(0)
T1.to_csv("T1_por_sistema.csv")
W = pd.DataFrame({v:{"familia(5)":omega2(a[v],a.system),"componentes(15)":omega2(a[v],a.components),
                     "perfil_fuentes":omega2(a[v],a.sources_profile),"periodo(3)":omega2(a[v],a.periodo)} for v in G}).T.round(3)
W.to_csv("H1_omega2_familia_vs_fuentes.csv")
H2 = a.groupby("periodo",observed=True)[["infoacc","privacy","referen","const_court_interprets","treat_superior"]].mean().round(2); H2["n"]=a.groupby("periodo",observed=True).size(); H2.to_csv("H2_por_periodo.csv")
H3 = a.groupby(["periodo","indig_autonomy"],observed=True)[["referen","infoacc","voteun"]].mean().round(2); H3["n"]=a.groupby(["periodo","indig_autonomy"],observed=True).size(); H3.to_csv("H3_autonomia_por_periodo.csv")
disc = a[(a.indig_autonomy==1)&(a.has_Customary==0)][["country","system","components","systyear"]]; disc.to_csv("discrepancia_CCP_autonomia_vs_JuriGlobe.csv",index=False)
# INTERP_3 e INDPOLGR_1-7 (nota 10): intérprete por familia y por perfil; derechos políticos indígenas donde FEDERAL_3=1
IN = ["ordinary_courts_interpret","const_court_interprets","supreme_court_interprets","supreme_chamber_interprets"]
T2 = a.groupby("system")[IN].mean().round(2); T2["n"]=a.groupby("system").size(); T2.to_csv("T2_interprete_por_sistema.csv")
a.assign(tribunal_especializado=a.const_court_interprets).groupby("tribunal_especializado")[["supreme_court_interprets","ordinary_courts_interpret"]].agg(["mean","sum"]).round(2).to_csv("T2b_interp3_segun_interp2.csv")
IP = [f"indpolgr_{k}" for k in range(1,8)]; f3 = a[a.indig_autonomy==1]
T3 = pd.DataFrame({"n_si":f3[IP].sum(),"n":f3[IP].notna().sum(),"prop":f3[IP].mean().round(2)}); T3.to_csv("T3_indpolgr_donde_federal3.csv")
f3[["country","system","systyear"]+IP].to_csv("T3b_indpolgr_por_pais.csv",index=False)
print("OK —", len(a), "países con contenido codificado en 2023; tablas escritas.")
