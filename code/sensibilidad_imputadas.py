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
Análisis de sensibilidad (IV §3): repite H1-H3 con (a) la muestra completa (n=182) y
(b) solo las constituciones cuya fila de 2023 no es imputada por el CCP (coding_imputed=0; n=87).
Entrada: dataset_2023_juriglobe_ccp.csv (salida de analisis_webfare_ccp.py) e
         imputadas_2023_eventos_no_codificados.csv (filas con coding_imputed=1 en CCP v5.0, año 2023).
Uso: python3 sensibilidad_imputadas.py
"""
import pandas as pd, numpy as np
d = pd.read_csv("dataset_2023_juriglobe_ccp.csv"); d = d[d.coded_2023].copy()
imp = pd.read_csv("imputadas_2023_eventos_no_codificados.csv")
d["imputada"] = d.cowcode.isin(imp.cowcode)
d["periodo"] = pd.cut(d.systyear,[0,1945,1989,2100],labels=["<1946","1946-1989","1990+"])
def omega2(y,g):
    m = pd.DataFrame({"y":y,"g":g}).dropna()
    if m.g.nunique()<2: return np.nan
    gm=m.y.mean(); gr=[s for _,s in m.groupby("g",observed=True).y]; k=len(gr); N=len(m)
    ssb=sum(len(s)*(s.mean()-gm)**2 for s in gr); ssw=sum(((s-s.mean())**2).sum() for s in gr); sst=ssb+ssw
    msw=ssw/(N-k); return max(0,(ssb-(k-1)*msw)/(sst+msw)) if sst>0 else np.nan
G = ["infoacc","referen","voteun","privacy","census","indig_autonomy"]
out=[]
for name,a in [("completa",d),("no_imputadas",d[~d.imputada])]:
    print("\n=====",name,"n =",len(a))
    W = pd.DataFrame({v:{"familia":omega2(a[v],a.system),"componentes":omega2(a[v],a.components),
        "perfil_fuentes":omega2(a[v],a.sources_profile),"periodo":omega2(a[v],a.periodo)} for v in G}).T.round(3)
    print(W); W.insert(0,"muestra",name); W.insert(1,"tabla","H1_omega2"); out.append(W.reset_index())
    H2 = a.groupby("periodo",observed=True)[["infoacc","privacy","referen","const_court_interprets","treat_superior"]].mean().round(2); H2["n"]=a.groupby("periodo",observed=True).size()
    print(H2); H2.insert(0,"muestra",name); H2.insert(1,"tabla","H2_periodo"); out.append(H2.reset_index())
    T1 = a.groupby("system")[["infoacc","referen","privacy","const_court_interprets"]].mean().round(2); T1["n"]=a.groupby("system").size(); T1["anio"]=a.groupby("system").systyear.mean().round(0)
    print(T1); T1.insert(0,"muestra",name); T1.insert(1,"tabla","T1_sistema"); out.append(T1.reset_index())
    r=a[a.periodo=="1990+"]; H3=r.groupby("indig_autonomy")[["infoacc","referen","voteun"]].mean().round(2); H3["n"]=r.groupby("indig_autonomy").size()
    print(H3); H3.insert(0,"muestra",name); H3.insert(1,"tabla","H3_1990+"); out.append(H3.reset_index())
    for lab,m in [("abierto",(a.offrel_official==0)&(a.treat_superior==1)&(a.const_court_interprets==1)),
                  ("ley_jurisp",(a.offrel_official==0)&(a.treat_superior==0)&(a.const_court_interprets==0))]:
        p=a[m]; print(lab,len(p),p[["infoacc","referen","voteun","privacy","indig_autonomy"]].mean().round(2).to_dict(), round(p.systyear.mean()))
pd.concat(out).to_csv("sensibilidad_imputadas_resultados.csv",index=False)
