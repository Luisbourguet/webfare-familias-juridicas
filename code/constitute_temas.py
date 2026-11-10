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
Descarga de Constitute (API pública, sin autenticación) las disposiciones que el propio
Comparative Constitutions Project etiqueta con cada variable del estudio, para las
constituciones de la muestra, y guarda solo su localización (sección, ancla, artículo,
ubicación). No guarda el texto de las disposiciones: muchas traducciones tienen derechos
de terceros.

Uso: python3 constitute_temas.py <cruce_constitute_ccp_muestra182.csv> <salida.json>
El cruce indica, para cada país de la muestra, el identificador de Constitute.
Etiquetas (claves de Constitute = nombres de variables del CCP): infoacc, referen, voteun,
privacy, census, offrel, treatcon (TREATST), interp y judcrts2 (INTERP_2).
"""
import sys, csv, json, re, html as H, time, urllib.request, urllib.parse
KEYS = {'infoacc': 'INFOACC', 'referen': 'REFEREN', 'voteun': 'VOTEUN', 'privacy': 'PRIVACY',
        'census': 'CENSUS', 'offrel': 'OFFREL', 'treatcon': 'TREATST', 'judcrts2': 'INTERP_2', 'interp': 'INTERP_2'}
API = 'https://www.constituteproject.org/service/sectionstopicsearch?'
cr = {r['constitute_id']: r for r in csv.DictReader(open(sys.argv[1], encoding='utf-8')) if r['constitute_id']}
ids = sorted(cr)
def clean(s): return re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', ' ', s))).strip()
out = []
for k, var in KEYS.items():
    for b in range(0, len(ids), 30):
        q = [('key', k), ('lang', 'en')] + [('cons_id', c) for c in ids[b:b + 30]]
        d = json.loads(urllib.request.urlopen(API + urllib.parse.urlencode(q), timeout=60).read())
        for cid, v in d.items():
            for h in v.get('results', []):
                crumbs = [clean(x) for x in re.findall(r'<span class="article-breadcrumb[^"]*"[^>]*>(.*?)</span>', h, re.S)]
                sec = re.search(r'data-id="section/(\d+)"', h); anc = re.search(r'#s(\d+)', h)
                ps = [clean(x) for x in re.findall(r'<p class="content">(.*?)</p>', h, re.S)]
                label = next((p for p in ps if len(p) < 45 and re.match(r'(?i)(art|section|sec\.|§|\d|amendment|rule|paragraph|clause|[ivxlc]+\b)', p)), '')
                out.append(dict(cowcode=cr[cid]['cowcode'], pais=cr[cid]['pais'], constitute_id=cid, variable=var,
                                etiqueta=k, seccion=sec.group(1) if sec else '', ancla=f's{anc.group(1)}' if anc else '',
                                articulo=label or (crumbs[-1] if crumbs else ''), ubicacion=' > '.join(crumbs)))
        time.sleep(1)
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out), 'disposiciones etiquetadas en', len({o['constitute_id'] for o in out}), 'constituciones')
