# edge/collector — colector OPC UA

Suscriptor OPC UA que persiste rasters y resultados a Parquet fuera del repositorio
(`docs/00-brief.md` §4.1, Fase 3).

## Alcance

- Suscribirse a los nodos de `docs/03-contrato-datos.md` §2 (estado, captura, features,
  inferencia).
- Escribir Parquet en `data/raw/` (ignorado por git).
- Registrar checksum de cada lote para `data/README.md`.

## Estado

Andamiaje. Sin implementación.

## Reglas

- Los datos **no** entran al repositorio: solo su esquema y su checksum.
- Sin credenciales en el repositorio.
