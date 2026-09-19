# hardware/cad — fuentes CAD

## Este directorio

- **Modelos propios** (paramétricos, editables): van aquí, versionados.
  El brief §11 pide el plato de 310 mm en segmentos imprimibles, el portasensor y el
  gálibo. Todavía no existen: **`PENDIENTE`**.
- **`vendor/`**: modelos de terceros descargados del fabricante. Se conservan en local
  y **no se versionan** (ver `.gitignore`), porque son descargas con sus propias
  condiciones de uso y el repositorio es público.

## Modelos de proveedor presentes

`vendor/balluff-bos-18m/` — descarga de PARTcommunity/3Dfindit (CADENAS):

| Archivo | Contenido |
| --- | --- |
| `BALLUFF BOS 18MR-PA-LD10-S4(0-).stp` | STEP del sensor |
| `BAL.BOS0142.edz` | Datos adicionales del fabricante |
| `MAN_BOS_18M_MR_LD10_DE_EN_C19_DOK_943262_00_000.pdf` | Manual del sensor |
| `readme-and-terms-of-use-3d-cad-models (1).txt` | Condiciones de uso de CADENAS |

## Discrepancia abierta sobre el sensor

El brief (`docs/00-brief.md` §3) cita el modelo `BOS ...-PU-RH10-S75`, pero los CAD
descargados son del **`BOS 18MR-PA-LD10-S4`**. Son series distintas. Confirmar cuál está
realmente montado antes de cerrar el mapeo de hilos del conector M8 en
`hardware/cableado/mapeo-io.md`. **`PENDIENTE`**.

## Pendientes de CAD propio

- [ ] Plato de 310 mm en segmentos imprimibles (Fase 1).
- [ ] Portasensor con tope de altura contra el perfil de extrusión (Fase 1).
- [ ] Gálibo con agujero de centrado en el eje (Fase 1).
- [ ] Verificación de interferencia óptica entre sensores a 20 mm (Fase 1).
