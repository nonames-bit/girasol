# Allen-Bradley CompactLogix L33ER

Plataforma secundaria, usada para medir **portabilidad** en la Fase 5
(`docs/00-brief.md` §11). No es la plataforma de producción.

## Contenido

| Ruta | Qué es |
| --- | --- |
| `src/` | Exportaciones `.L5X` (texto) |

## Alcance de la Fase 5

- Portar la inferencia al L33ER.
- Medir tiempo de scan y memoria en ambas plataformas.
- Publicar un informe comparativo Omron vs Allen-Bradley.

## Cómo importar a Studio 5000

<!-- TODO: pasos exactos de importación de L5X, versión de Studio 5000 requerida,
     y diferencias de sintaxis respecto al ST del NX102. PENDIENTE. -->

## Nota de diseño

Nada de lo que vive en `src/` debe contener APIs específicas de Rockwell que rompan la
paridad con `plc/shared/contratos.md`. Si una diferencia de plataforma obliga a un tipo
distinto (por ejemplo, empaquetar el raster en `DINT`), se documenta en
`plc/shared/contratos.md` y se resuelve con un ADR.

## Archivos binarios

Los proyectos `.ACD` van por git-lfs y no se diferencian.
