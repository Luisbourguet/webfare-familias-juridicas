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
"""Vincula cada variable del análisis con las disposiciones etiquetadas en Constitute (texto en inglés)
para las 182 constituciones del corte de 2023 y compara con el código del CCP recodificado."""
import json, pandas as pd, numpy as np, re
d=pd.read_csv('data/derived/dataset_2023_juriglobe_ccp.csv'); d=d[d.coded_2023]
cr=pd.read_csv('data/derived/cruce_constitute_ccp_muestra182.csv')
tags=pd.DataFrame(json.load(open('data/derived/constitute_temas_secciones_2026-11-10.json')))
tags['cowcode']=tags.cowcode.astype(int)
def art(r):
    src=r.articulo if r.articulo else r.ubicacion
    m=re.findall(r'(?:Article|Art\.?|Section|Sec\.|Amendment|Rule|Paragraph|Clause)\s*[\w.()-]+(?:\s*>\s*[\w()]+)?',src)
    return m[-1] if m else src.split(' > ')[-1]
tags['disposicion']=tags.apply(art,axis=1)
rec=pd.read_csv('data/recodificacion/recodificacion_2023.csv')
V={'INFOACC':'infoacc','REFEREN':'referen','VOTEUN':'voteun','PRIVACY':'privacy','CENSUS':'census',
   'OFFREL':'offrel_official','TREATST':'treat_superior','INTERP_2':'const_court_interprets'}
SEM={'INFOACC':'directa','REFEREN':'directa','VOTEUN':'directa','PRIVACY':'directa','CENSUS':'directa',
     'OFFREL':'localiza (la etiqueta incluye estatus especial, no solo religión oficial)',
     'TREATST':'localiza (la etiqueta marca cualquier disposición sobre tratados, no su supremacía)',
     'INTERP_2':'localiza (la etiqueta marca cualquier intérprete o tribunal constitucional)'}
rows=[]
for _,r in d.iterrows():
    c=cr[cr.cowcode==r.cowcode]
    cid=c.constitute_id.iloc[0] if len(c) and isinstance(c.constitute_id.iloc[0],str) else ''
    for v,col in V.items():
        val=r[col]; val=None if pd.isna(val) else int(val)
        rr=rec[(rec.pais==r.country)&(rec.variable==v)]
        val23=int(rr.valor_2023.iloc[0]) if len(rr) and not pd.isna(rr.valor_2023.iloc[0]) else None
        t=tags[(tags.cowcode==r.cowcode)&(tags.variable==v)]
        arts=list(dict.fromkeys(t.disposicion.tolist())); anc=list(dict.fromkeys(t.ancla.tolist()))
        n=len(t)
        if not cid: conc='sin texto en Constitute'
        elif val is None: conc='valor perdido en el CCP'
        elif SEM[v]!='directa': conc='localización' if n else 'sin disposición etiquetada'
        elif val==1 and n: conc='coincide: inscrita y localizada'
        elif val==0 and not n: conc='coincide: no inscrita, sin disposición etiquetada'
        elif val==1 and not n: conc='discrepancia: CCP inscrita, Constitute sin etiqueta'
        else: conc='discrepancia: Constitute etiqueta, CCP no inscrita'
        rows.append(dict(cowcode=r.cowcode,pais=r.country,constitute_id=cid,
            constitute_version=c.constitute_version.iloc[0] if len(c) else '',ccp_version_codificada=c.ccp_version_codificada.iloc[0] if len(c) else '',
            categoria_protocolo=c.categoria_protocolo.iloc[0] if len(c) else '',imputada=r.get('coded_2023'),
            url_texto=f'https://www.constituteproject.org/constitution/{cid}?lang=en' if cid else '',
            variable=v,valor_ccp_recodificado=val,valor_cotejado_2023=val23,tipo_correspondencia=SEM[v],
            n_secciones_etiquetadas=n,disposiciones='; '.join(arts),anclas='; '.join(a for a in anc if a),concordancia=conc))
o=pd.DataFrame(rows)
o['imputada']=o.cowcode.map(cr.set_index('cowcode').imputada)
o.to_csv("data/derived/referencias_textos_constitute.csv",index=False)
print(len(o), o.constitute_id.eq('').sum()//8, 'sin texto')
dd=o[o.tipo_correspondencia=='directa']
print(pd.crosstab(dd.variable,dd.concordancia))
print(pd.crosstab([dd.imputada,dd.categoria_protocolo.str[0]],dd.concordancia.str.startswith('discrepancia')))
