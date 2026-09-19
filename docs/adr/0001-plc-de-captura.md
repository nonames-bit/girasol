# ADR-0001 — PLC Omron NX102-9000 como plataforma de captura

- Estado: propuesto
- Fecha: 2026-09-19

## Contexto

El sistema necesita: generar pulsos de paso con temporización determinista, leer 13
entradas digitales (12 canales + home) de forma sincrónica con el avance del motor,
acumular un raster de $100 \times 12$ bits durante una vuelta, y ejecutar todo el
cálculo de features e inferencia dentro del ciclo de scan. El brief fija el Omron
NX102-9000 como PLC principal y un Allen-Bradley CompactLogix L33ER como plataforma
secundaria de portabilidad.

<!-- TODO: completar con las restricciones que motivaron la elección (plataforma ya
     disponible, soporte de ST, OPC UA nativo, tarea periódica de alta velocidad). -->

## Opciones consideradas

1. Omron NX102-9000 con módulos NX-ID5442 / NX-OD5256.
2. Allen-Bradley CompactLogix L33ER.
3. <!-- TODO: ¿se consideró alguna otra plataforma? Si no, decirlo. -->

## Decisión

Usar el Omron NX102-9000 como plataforma principal de captura, features e inferencia,
y reservar el L33ER para la medición de portabilidad de la Fase 5.

<!-- TODO: justificar por qué el Omron y no el AB como principal. El brief no da el
     razonamiento; PENDIENTE hasta que se documente. -->

## Consecuencias

- El código de producción vive en `plc/omron-nx102/src/` como Structured Text
  exportado a texto plano, versionable y diffeable.
- La portabilidad a AB no condiciona el diseño de la Fase 1, pero sí obliga a
  mantener `plc/shared/contratos.md` libre de dependencias de plataforma.
- Los binarios de proyecto (`.smc2`, `.ACD`) van por git-lfs y no se diferencian.

## Referencias

- `docs/00-brief.md` §3 (hardware), §6 (estructura), §11 (Fase 5).
