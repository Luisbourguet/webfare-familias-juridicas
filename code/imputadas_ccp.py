# -*- coding: utf-8 -*-
"""
Lista de constituciones cuya fila de 2023 en el CCP (Characteristics of National Constitutions v5.0)
es imputada (coding_imputed = 1): los valores copian el último evento codificado. Para cada una se
listan los eventos constitucionales posteriores registrados en la cronología (ccpcce v6.0) y no codificados.
Entrada: carpeta con ccpcnc_v5.csv y ruta a ccpcce_v6.csv; dataset_2023_juriglobe_ccp.csv (muestra).
Salida: imputadas_2023_eventos_no_codificados.csv
Uso: python3 imputadas_ccp.py <ruta/ccpcnc_v5.csv> <ruta/ccpcce_v6.csv>
"""
import sys, pandas as pd
cnc, cce = sys.argv[1], sys.argv[2]
x = pd.read_csv(cnc, usecols=["cowcode","country","year","systyear","coding_available","coding_imputed",
                              "imputed_evntyear","imputation_type"], low_memory=False)
x = x[(x.year == 2023) & (x.coding_imputed == 1)]
m = pd.read_csv("dataset_2023_juriglobe_ccp.csv"); m = m[m.coded_2023]
x = x[x.cowcode.isin(m.cowcode)]
c = pd.read_csv(cce)
c = c[c.evnttype.isin(["new","amendment","reinstated","interim"])]  # eventos que cambian el texto; se excluyen suspensiones y "samendment"
rows = []
for _, r in x.iterrows():
    e = c[(c.cowcode == r.cowcode) & (c.year > r.imputed_evntyear) & (c.year <= 2023)].sort_values("year")
    rows.append(dict(cowcode=r.cowcode, country=r.country, systyear=r.systyear, imputed_evntyear=r.imputed_evntyear,
                     imputation_type=r.imputation_type, n_events=len(e),
                     types=",".join(sorted(e.evnttype.unique())), years=" ".join(str(int(y)) for y in e.year)))
o = pd.DataFrame(rows).sort_values("country"); o.to_csv("imputadas_2023_eventos_no_codificados.csv", index=False)
print(len(o), "filas imputadas;", int(o.n_events.sum()), "eventos posteriores no codificados")
