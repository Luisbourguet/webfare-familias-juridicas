# Webfare en las familias jurídicas: datos y código

Material complementario del artículo *El Webfare en las familias jurídicas: teoría constitucional comparada del reparto del valor del dato* (en evaluación). Permite reproducir los resultados descriptivos de las secciones IV y V y la comprobación de sensibilidad de IV §3 y de la nota 10.

## Contenido

| Carpeta | Archivo | Qué es |
|---|---|---|
| `code/` | `analisis_webfare_ccp.py` | Cruce JuriGlobe–CCP, corte de 2023, recodificación y tablas (H1–H3, T1–T3). |
| | `imputadas_ccp.py` | Lista de constituciones cuya fila de 2023 imputa el CCP, con los eventos posteriores no codificados según la cronología. |
| | `sensibilidad_imputadas.py` | Repite el análisis con las constituciones sin valores imputados (n = 87). |
| `data/derived/` | `juriglobe_all_entities_clean.csv` | Tabla de JuriGlobe (Universidad de Ottawa; 2.ª ed. 2008, actualizada el 24-07-2024; consulta del 9-11-2026) con los nombres normalizados. |
| | `cruce_juriglobe_ccp.csv` | Emparejamiento de las entidades de JuriGlobe con los códigos del CCP (197 filas: cuatro corresponden a homónimos históricos que el corte de 2023 descarta). |
| | `dataset_2023_juriglobe_ccp.csv` | Un Estado por fila, con las variables recodificadas; la muestra analítica son las filas con `coded_2023 = True` (n = 182). |
| | `imputadas_2023_eventos_no_codificados.csv` | 95 filas imputadas: año de la versión codificada y eventos posteriores (438 en total). |
| `results/` | `H1_…`, `H2_…`, `H3_…`, `T1_…`–`T3b_…` | Salidas del análisis principal. |
| | `sensibilidad_imputadas_resultados.csv` | Salidas de la comprobación de sensibilidad. |

## Fuentes que no se redistribuyen

- **Comparative Constitutions Project.** *Characteristics of National Constitutions*, versión 5.0 (Elkins y Ginsburg, 2025), y *Chronology of Constitutional Events*, versión 6.0 (2026). Se descargan en https://comparativeconstitutionsproject.org/download-data/. Los scripts usan `ccpcnc_v5_small.csv`, `ccpcnc_v5.csv` y `ccpcce_v6.csv`.
- **Textos constitucionales de Constitute** (constituteproject.org). Se usaron solo para leer y localizar disposiciones; muchas traducciones tienen derechos de terceros.

## Reproducción

Requisitos: Python 3.10 o posterior y `pandas`.

```bash
mkdir trabajo && cp data/derived/juriglobe_all_entities_clean.csv trabajo/ && cd trabajo
python3 ../code/analisis_webfare_ccp.py <carpeta que contiene ccpcnc_v5_small.csv>
python3 ../code/imputadas_ccp.py <ruta>/ccpcnc_v5.csv <ruta>/ccpcce_v6.csv
python3 ../code/sensibilidad_imputadas.py
```

Las salidas deben coincidir con `data/derived/` y `results/`.

## Decisiones de codificación

- **Corte.** La fila de 2023 de cada Estado, el último año del panel. Once Estados sin codificación disponible para su texto vigente quedan fuera.
- **Recodificación** (nota 10 del artículo): 1 → 1; 2 → 0; 90 → 0; 96 y 98 → valor perdido.
  - OFFREL: 2, 3, 90 y 98 → 0.
  - TREATST: 1 → 1; 2, 3 y 98 → 0; 99 → valor perdido.
  - Las variables dicotómicas (FEDERAL_3, INTERP_*, INDPOLGR_*) no se recodifican; en INDPOLGR_*, el valor 99 («no preguntado») pasa a valor perdido.
- **Imputación.** En 95 de las 182 constituciones, el CCP copia en 2023 los valores de la última versión codificada (`coding_imputed = 1`). El análisis principal usa las 182; la comprobación de sensibilidad, las 87 restantes.
- **Medida de asociación.** Omega al cuadrado.

## Licencias

Código (`code/`): MIT (`LICENSE`). Datos derivados y resultados (`data/derived/`, `results/`): CC BY 4.0 (`data/LICENSE-DATA.md`), sin perjuicio de las condiciones de las fuentes originales.
