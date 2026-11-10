# Licencias de los datos

Este repositorio distingue entre lo que procede de fuentes de terceros y lo que es aportación propia.

## 1. Archivos derivados de JuriGlobe y del CCP — uso no comercial con atribución

Archivos de `data/derived/`:

| Archivo | Fuente |
|---|---|
| `juriglobe_all_entities_clean.csv` | JuriGlobe |
| `cruce_juriglobe_ccp.csv` | JuriGlobe y CCP |
| `dataset_2023_juriglobe_ccp.csv` | JuriGlobe y CCP |
| `imputadas_2023_eventos_no_codificados.csv` | CCP |

Estos archivos **no** se distribuyen bajo CC BY 4.0. Reproducen o transforman datos de terceros y solo pueden usarse **con fines no comerciales y con atribución a sus fuentes**:

- **JuriGlobe** — Groupe de recherche sur les systèmes juridiques dans le monde, Faculté de droit (Section de droit civil), Université d'Ottawa, https://www.juriglobe.ca/. Según sus condiciones, el uso personal, educativo o informativo no comercial no requiere autorización, siempre que se indique a la Universidad de Ottawa, su Facultad de Derecho y su Sección de derecho civil como fuente, con la URL. Cualquier otro uso requiere su consentimiento previo por escrito (dcivil@uottawa.ca).
- **Comparative Constitutions Project** — Elkins, Z., y Ginsburg, T. (2025). *Characteristics of National Constitutions*, versión 5.0; y (2026) *Chronology of Constitutional Events*, versión 6.0. https://comparativeconstitutionsproject.org/. Cite ambas fuentes.

La normalización de nombres, el emparejamiento con los códigos del CCP y la recodificación que contienen estos archivos se ofrecen en las mismas condiciones.

## 2. Aportación propia — CC BY 4.0

- `results/`: salidas del análisis.
- `data/recodificacion/`: recodificación de los países de referencia sobre los textos vigentes en 2023 (propuesta pendiente de validación del autor).

Se distribuyen bajo la licencia Creative Commons Atribución 4.0 Internacional (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.es

Excepción: en `recodificacion_2023.csv`, la columna `valor_ccp_recodificado` reproduce valores del CCP y sigue las condiciones del apartado 1.

## 3. Código

El código de `code/` se distribuye bajo la licencia Apache 2.0 (`LICENSE`).
