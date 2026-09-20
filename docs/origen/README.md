# Briefs de origen

Documentos **recibidos** al arrancar el proyecto, conservados sin modificar como
trazabilidad.

| Archivo | Qué es |
| --- | --- |
| `girasol-bootstrap.md` | Brief de arranque en español. Es la versión de referencia. |
| `girasol-bootstrap-en.md` | Traducción al inglés del mismo brief. |

La copia **normativa** que se cita en el resto de la documentación es
[`../00-brief.md`](../00-brief.md), que es idéntica a `girasol-bootstrap.md`. Si en el
futuro se edita el brief, la copia normativa es la que manda.

## Contradicciones conocidas entre los dos briefs

Se resolvieron a favor del brief en español, salvo donde se indica:

| Tema | Brief ES | Brief EN | Resolución |
| --- | --- | --- | --- |
| Idioma de la documentación | docs en español, README en inglés | todo en inglés | Docs en español, README en inglés |
| Directorio de configuración de agentes | `.kilocode/` | `.kilocode/` | `AGENTS.md` + `.kilo/` (requisito del entorno actual de Kilo) |
| Plantilla de issue de experimento | `experimento.yml` | `experiment.yml` | `experimento.yml` |
| Etiquetas de issue | `tipo:bug`, `tipo:experimento` | `type:bug`, `type:experiment` | `tipo:*` (taxonomía del brief ES, que es el normativo) |
| Fórmula de $\varphi_7$ | se exige en §5.7 pero no se escribe | igual | Se añade la fórmula estándar de Hu en `../02-matematicas.md` §5.6 |
