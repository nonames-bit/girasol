# edge/bridge — publicador Sparkplug B

Publica el resultado de cada pieza al broker MQTT con Sparkplug B
(`docs/00-brief.md` §4.1, Fase 3).

## Alcance

- Construir el `NDATA`/`DDATA` con las métricas de `docs/03-contrato-datos.md` §4.
- Gestionar `NBIRTH`/`DBIRTH` y el ciclo de vida de la sesión Sparkplug.

## Estado

Andamiaje. Sin implementación.

## Pendiente

- Periodicidad de publicación, QoS y si los rasters viajan por Sparkplug o solo por el
  colector: **`PENDIENTE`**.
- URL del broker y credenciales: **`PENDIENTE`**, nunca en el repositorio.
