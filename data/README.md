# data — esquema y checksums

**Aquí no hay datos.** Este directorio contiene cómo obtenerlos y cómo verificarlos
(`docs/00-brief.md` §6).

## Reglas

- `data/raw/` y `data/processed/` están en `.gitignore`. Los datasets nunca entran al
  repositorio.
- Solo entran: el esquema, el procedimiento de captura y el checksum.

## Esquema de un registro de captura

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `timestamp_utc` | datetime | Instante de la vuelta |
| `cycle_count` | uint32 | Contador de vueltas |
| `raster_raw` | bool[100,12] | Raster crudo antes de fusionar brazos |
| `features` | float[10] | Vector de `docs/02-matematicas.md` §5.7 |
| `class` | int | Clase decidida (`PENDIENTE` el valor de K) |
| `confidence` | float | `p_c` |
| `model_version` | string | Versión del modelo activo |
| `label` | int \| null | Etiqueta real, solo en captura de dataset |

Formato de persistencia: **`PENDIENTE`** (Parquet propuesto en `docs/00-brief.md` §11).

## Checksums

Todo lote exportado debe registrar: nombre, filas, fecha, `sha256` y la versión de
`ml/configs/girasol.yaml` usada. La tabla de lotes va **`PENDIENTE`** hasta la Fase 3.

## Reproducibilidad

- Semillas fijas en toda captura sintética y en todo split de entrenamiento.
- El checksum de un lote es la prueba de qué dataset produjo un modelo registrado en
  `models/registry.json`.
