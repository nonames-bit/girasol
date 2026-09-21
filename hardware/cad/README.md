# hardware/cad — fuentes CAD

## Este directorio

- **Modelos propios** (los del proyecto): van aquí y se versionan.
- **`vendor/`**: modelos de terceros descargados del fabricante. Se conservan en local
  y **no se versionan** (ver `.gitignore`), porque son descargas con sus propias
  condiciones de uso y el repositorio es público.

## Modelos propios

Dimensiones medidas con el kernel OCP sobre los archivos reales: caja envolvente en mm
y número de caras. La finalidad es la deducible del nombre y está **por confirmar**.

| Archivo | Caja envolvente (mm) | Caras | Qué parece ser |
| --- | --- | --- | --- |
| `MESAREDONDAV1.stl` | 229,98 × 26,50 × 229,99 | 42 036 | Plato/mesa giratoria: Ø230 × 26,5 de espesor |
| `Soportegrande.stl` | 200,00 × 233,00 × 50,00 | 3 500 | Soporte grande |
| `Soporte2.stp` | 200,00 × 104,15 × 50,00 | 40 | Soporte, en STEP (sólido, 40 caras) |
| `soportesensorballuffV6.stl` | 33,00 × 15,00 × 61,00 | 7 316 | Portasensor Balluff |

**Discrepancia abierta:** el brief (`docs/00-brief.md` §11) pide un plato de **310 mm**,
y `MESAREDONDAV1.stl` mide Ø230 mm. Confirmar si el plato definitivo es de 310 mm o si
este es un prototipo. **`PENDIENTE`**.

## Cómo ver los CAD

Vía recomendada, todo dentro de VS Code:

- Extensión **OCP CAD Viewer** (`bernhard-42.ocp-cad-viewer`), ya instalada.
- Paquete Python **`ocp-vscode`** (incluye el kernel OCP 7.9.3.1), ya instalado en
  Python 3.13 y verificado cargando estos cuatro archivos.
- **`view_cad.py`**, visor de esta carpeta.

Pasos:

1. `Ctrl+Shift+P` → `OCP CAD Viewer: Open viewer`.
2. Ejecutar el visor (botón Run sobre el archivo, o en la terminal):

   ```powershell
   python hardware/cad/view_cad.py Soporte2.stp Soportegrande.stl
   ```

   Sin argumentos carga todos los CAD de esta carpeta:

   ```powershell
   python hardware/cad/view_cad.py
   ```

El modelo aparece en el panel del visor, no en una ventana aparte.

`view_cad.py` es una herramienta de taller: **no** es dependencia de `ml/`, no entra en
el build ni en CI. Si algún día falta, se reinstala con `pip install ocp-vscode`.

### Alternativas sin instalar nada

- STEP y STL: <https://viewer.autodesk.com> (arrastrar y soltar).
- Solo mallas STL: <https://3dviewer.net>.
- Escritorio: FreeCAD o CAD Assistant de OpenCascade (abren ambos formatos).

## Modelos de proveedor

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

## Estado respecto de la Fase 1

- [x] Pieza existente: plato `MESAREDONDAV1.stl` — falta confirmar que el definitivo sea
      de 310 mm en segmentos imprimibles.
- [x] Pieza existente: portasensor `soportesensorballuffV6.stl` — falta confirmar el tope
      de altura contra el perfil de extrusión.
- [x] Piezas existentes: `Soporte2.stp`, `Soportegrande.stl`.
- [ ] Gálibo con agujero de centrado en el eje (Fase 1).
- [ ] Verificación de interferencia óptica entre sensores a 20 mm (Fase 1).
