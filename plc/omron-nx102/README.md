# Omron NX102-9000

Código de producción de Girasol, exportado como texto plano y versionable.

## Contenido

| Ruta | Qué es |
| --- | --- |
| `src/POU_Captura.st` | Generación de pulsos, conteo de micropasos, detección de home, buffer del raster |
| `src/POU_Fusion.st` | Fusión de brazos con desfase N/2 (`docs/02-matematicas.md` §5.2) |
| `src/POU_Features.st` | Momentos y vector de 10 features (§5.3–5.7) |
| `src/POU_Inferencia.st` | Normalización, modelo, argmax y confianza (§5.8–5.10) |
| `src/POU_Sombra.st` | Modo sombra y conmutación de banco (Fase 4) |
| `udt/` | UDTs de configuración y de pesos |

## Cómo importar a Sysmac Studio

<!-- TODO: pasos exactos de importación de ST y de UDT, versión de Sysmac Studio
     requerida, y orden de importación. PENDIENTE. -->

## Convenciones

- Un POU por responsabilidad; sin bloques monolíticos.
- Nombres en inglés, comentarios en español.
- Prefijos de tipo: `b` booleano, `i` entero, `r` real, `a` array, `s` string.
- Cada POU declara su **tiempo de ejecución peor caso**: por ahora `PENDIENTE`, porque
  es un entregable que se mide en la Fase 1.
- Las constantes viven en un UDT de configuración, nunca como literales dispersos.

## Reglas duras

Sin recursión, sin memoria dinámica, sin bucles no acotados, sin llamadas bloqueantes.
Ver `AGENTS.md` §3.

## Archivos binarios

Los proyectos de Sysmac (`.smc2`) van por git-lfs y **no** se diferencian. La verdad
versionable es este directorio `src/`.
