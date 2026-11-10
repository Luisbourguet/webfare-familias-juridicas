# El Webfare en las familias jurídicas: teoría constitucional comparada del reparto del valor del dato

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24110937.svg)](https://doi.org/10.5281/zenodo.24110937)

**Preprint, versión 1.0 (10 de noviembre de 2026)** · Luis Felipe Bourguet González · **versión no arbitrada y no definitiva** · enviada a una revista con evaluación por pares doble ciego (sede no indicada) · CC BY 4.0

- PDF: [`Bourguet_2026_Webfare_familias_juridicas_preprint_v1-0.pdf`](Bourguet_2026_Webfare_familias_juridicas_preprint_v1-0.pdf)
- DOCX: [`Bourguet_2026_Webfare_familias_juridicas_preprint_v1-0.docx`](Bourguet_2026_Webfare_familias_juridicas_preprint_v1-0.docx)
- Fuente: [`preprint.md`](preprint.md) (Pandoc; archivos de compilación en `build/`)

El repositorio contiene además los datos derivados y el código que permiten reproducir los resultados descriptivos de las secciones IV y V y la comprobación de sensibilidad de IV §3 y de la nota 10.

## Cómo citar

Bourguet, L. (2026). *El Webfare en las familias jurídicas: teoría constitucional comparada del reparto del valor del dato* (preprint, versión 1.0; versión no arbitrada y no definitiva). Zenodo. https://doi.org/10.5281/zenodo.24110937

## Versiones

| Versión | Fecha | DOI | Cambio |
|---|---|---|---|
| v1.0-preprint | 2026-11-10 | [10.5281/zenodo.24110938](https://doi.org/10.5281/zenodo.24110938) | Primer depósito |
| v1.0.1-preprint | 2026-11-10 | — | DOI de concepto en el PDF, el DOCX, el README y CITATION.cff; texto sin cambios |

El DOI de concepto [10.5281/zenodo.24110937](https://doi.org/10.5281/zenodo.24110937) remite siempre a la última versión.

## Contenido

| Carpeta | Archivo | Qué es |
|---|---|---|
| `code/` | `analisis_webfare_ccp.py` | Cruce JuriGlobe–CCP, corte de 2023, recodificación y tablas (H1–H3, T1–T3). |
| | `imputadas_ccp.py` | Lista de constituciones cuya fila de 2023 imputa el CCP, con los eventos posteriores no codificados según la cronología. |
| | `sensibilidad_imputadas.py` | Repite el análisis con las constituciones sin valores imputados (n = 87). |
| | `constitute_temas.py` | Descarga de la API de Constitute la localización de las disposiciones etiquetadas con cada variable. |
| | `referencias_textos.py` | Construye `referencias_textos_constitute.csv`. |
| `data/derived/` | `juriglobe_all_entities_clean.csv` | Tabla de JuriGlobe (Universidad de Ottawa; 2.ª ed. 2008, actualizada el 24-07-2024; consulta del 9-11-2026) con los nombres normalizados. |
| | `cruce_juriglobe_ccp.csv` | Emparejamiento de las entidades de JuriGlobe con los códigos del CCP (197 filas: cuatro corresponden a homónimos históricos que el corte de 2023 descarta). |
| | `dataset_2023_juriglobe_ccp.csv` | Un Estado por fila, con las variables recodificadas; la muestra analítica son las filas con `coded_2023 = True` (n = 182). |
| | `imputadas_2023_eventos_no_codificados.csv` | 95 filas imputadas: año de la versión codificada y eventos posteriores (438 en total). |
| `data/recodificacion/` | `recodificacion_2023.csv` | Recodificación de los ocho países de referencia con fila imputada (México, Colombia, Arabia Saudí, Ecuador, China, India, Italia y Vietnam) sobre los textos vigentes en 2023: 80 códigos, con fuente y artículo. Validada por el autor (10-11-2026). Tres códigos cambian: México, REFEREN; Vietnam, INFOACC; Colombia, CENSUS. El artículo los usa en la Tabla III y en los casos; los análisis agregados usan los valores del CCP. |
| `data/derived/` | `cruce_constitute_ccp_muestra182.csv` | Para cada constitución de la muestra: versión codificada por el CCP, último evento hasta 2023 y 2025, identificador y versión del texto en Constitute y categoría de versión (A–D). |
| | `constitute_temas_secciones_2026-11-10.json` | Disposiciones que el CCP etiqueta en Constitute con cada variable del estudio (consulta del 10-11-2026): sección, ancla, artículo y ubicación; sin texto. |
| | `referencias_textos_constitute.csv` | **Variable por variable y país por país, el artículo de la constitución en que se apoya cada valor**, con enlace al texto en Constitute y concordancia entre el código del CCP y la etiqueta (182 constituciones × 8 variables). |
| `manuscript/` | `manuscrito_anonimizado_v1-7.md` | Texto anonimizado preparado para la evaluación doble ciego (10-11-2026); en él la nota 10 del preprint es la nota 9. |
| `build/` | | Cabecera, filtros y finalizador DOCX con que se compila el preprint (XeLaTeX vía Pandoc). El marco y las pestañas de color dicen qué es el documento: PREPRINT (rojo), ENVIADO · SIN EVALUACIÓN POR PARES (ámbar), DATOS Y CÓDIGO ABIERTOS (verde). |
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

Referencias a los textos constitucionales (desde la raíz del repositorio):

```bash
python3 code/constitute_temas.py data/derived/cruce_constitute_ccp_muestra182.csv data/derived/constitute_temas_secciones_2026-11-10.json
python3 code/referencias_textos.py
```

Las salidas deben coincidir con `data/derived/` y `results/`. Las etiquetas de Constitute pueden cambiar con el tiempo; el archivo JSON guarda la consulta del 10-11-2026.

## Cómo leer `referencias_textos_constitute.csv`

- **`disposiciones`** y **`url_texto`**: artículos de la constitución etiquetados con la variable y el enlace al texto completo.
- **`concordancia`**: en INFOACC, REFEREN, VOTEUN, PRIVACY y CENSUS, compara el código del CCP con la existencia de la etiqueta. En OFFREL, TREATST e INTERP_2 la etiqueta solo localiza la disposición (marca, por ejemplo, cualquier norma sobre tratados), así que el valor depende de su contenido.
- **Versión del texto**: una discrepancia puede deberse a que Constitute publica una versión distinta de la que codificó el CCP (`categoria_protocolo`: A, mismo texto o posterior hasta 2023; B, anterior; C, posterior a 2023).

## Decisiones de codificación

- **Corte.** La fila de 2023 de cada Estado, el último año del panel. Once Estados sin codificación disponible para su texto vigente quedan fuera.
- **Recodificación** (nota 10 del artículo): 1 → 1; 2 → 0; 90 → 0; 96 y 98 → valor perdido.
  - OFFREL: 2, 3, 90 y 98 → 0.
  - TREATST: 1 → 1; 2, 3 y 98 → 0; 99 → valor perdido.
  - Las variables dicotómicas (FEDERAL_3, INTERP_*, INDPOLGR_*) no se recodifican; en INDPOLGR_*, el valor 99 («no preguntado») pasa a valor perdido.
- **Imputación.** En 95 de las 182 constituciones, el CCP copia en 2023 los valores de la última versión codificada (`coding_imputed = 1`). El análisis principal usa las 182; la comprobación de sensibilidad, las 87 restantes.
- **Medida de asociación.** Omega al cuadrado.

## Licencias

- **Texto del preprint** (`preprint.md`, PDF y DOCX): CC BY 4.0.
- **Código** (`code/`): Apache 2.0 (`LICENSE`).
- **Archivos derivados de JuriGlobe y del CCP** (`data/derived/`): uso no comercial con atribución, según las condiciones de esas fuentes. No se distribuyen bajo CC BY.
- **Aportación propia** (`results/` y `data/recodificacion/`): CC BY 4.0.

Detalle en `data/LICENSE-DATA.md`.
