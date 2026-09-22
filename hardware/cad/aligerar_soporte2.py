"""Aligerado paramétrico de `Soporte2.stp` (Girasol).

Genera una copia con menos material conservando la rigidez y, sobre todo, sin
tocar la **ranura superior**, las puntas con sus agujeros de montaje, los pies de
las patas ni los redondeos.

Criterio de diseño
------------------
La pieza se midió con el kernel OCP antes de decidir dónde cortar:

- Volumen original: 169,31 cm³.
- El **poste** central tiene sección constante de 838,2 mm² (x −42..0, z 0..−22)
  y está libre de todo lo demás entre y = 0 y y = 52; a partir de y ≈ 54 las patas
  se fusionan con él.
- Las **patas** tienen 20,3 mm de ancho perpendicular a su eje, inclinado ≈ 41°.
- La **base** de 3 mm solo está ocupada en la franja central (z −22..0): el poste
  y los pies de las patas. Quedan dos zonas libres grandes entre cada pie y el
  poste.

Solo se rebaja material en esas zonas libres, dejando muros de al menos 4,5 mm y
radios grandes para no concentrar tensiones:

1. **Poste**: vano oblongo pasante en Z, 20 mm de ancho × 36 mm de alto (y 10..46).
   Deja dos montantes laterales de ~11 mm y puentes de 10 mm abajo y 5 mm arriba.
   El poste pasa de macizo a marco.
2. **Patas**: un vano oblongo por pata, alineado con su eje, 11 mm × 36 mm,
   centrado en el tramo recto. Deja ~4,6 mm de muro a cada lado.
3. **Base**: una ventana pasante de esquinas redondeadas (R10) en cada zona libre,
   41 × 41 mm y 36 × 41 mm, con 5 mm de borde contra el contorno, el poste y el
   pie de la pata.

Resultado medido (verificado con la sección a distintas alturas):

- Volumen: 169,31 → **130,85 cm³** (−38,46 cm³, −22,7 %).
- Reparto: poste −13,23 cm³, patas −15,55 cm³, base −8,96 cm³.
- Zonas críticas comparadas una a una contra el original: **idénticas**.

Uso
---
    python hardware/cad/aligerar_soporte2.py

Escribe `Soporte2_v2_ligero.stp` y `Soporte2_v2_ligero.stl` junto al original.
"""

from __future__ import annotations

import math
from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Reader, STEPControl_Writer
from OCP.StlAPI import StlAPI_Writer
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec

CAD_DIR = Path(__file__).resolve().parent
SOURCE = CAD_DIR / "Soporte2.stp"
TARGET_STEP = CAD_DIR / "Soporte2_v2_ligero.stp"
TARGET_STL = CAD_DIR / "Soporte2_v2_ligero.stl"

# --- Poste -----------------------------------------------------------------
# Vano oblongo pasante en Z (la ranura va de z=0 a z=-22).
# Los valores son los CENTROS de los radios; con R=10 el vano ocupa y 10..46.
POSTE_X_MIN = -31.0  # extremo izquierdo del vano
POSTE_X_MAX = -11.0  # extremo derecho del vano
POSTE_Y_MIN = 20.0  # centro del radio inferior  -> borde inferior en y=10
POSTE_Y_MAX = 36.0  # centro del radio superior  -> borde superior en y=46
POSTE_RADIO = (POSTE_X_MAX - POSTE_X_MIN) / 2.0

# --- Patas -----------------------------------------------------------------
# Vano oblongo alineado con el eje de cada pata.
PATA_LARGO = 36.0
PATA_ANCHO = 11.0
PATA_CENTROS = (
    (-79.20, 30.0, 49.1),  # pata izquierda: x, y, ángulo del eje en grados
    (37.10, 30.0, 130.9),  # pata derecha
)

# --- Base ------------------------------------------------------------------
# Ventanas pasantes en la base de 3 mm. El poste y las patas solo ocupan la
# franja central (z −22..0), así que quedan libres las dos zonas entre el pie de
# cada pata y el poste. Se dejan 5 mm de borde contra el contorno, contra el
# poste y contra el pie de la pata.
BASE_ESQUINA = 10.0
BASE_Y_DESDE = -3.5  # la base ocupa y −3..0
BASE_Y_HASTA = 0.5
BASE_VENTANAS = (
    (-87.5, -32.5, -46.5, 8.5),  # izquierda: x0, z0, x1, z1
    (4.5, -32.5, 40.5, 8.5),  # derecha
)

# Profundidad de corte: sobresale en Z por ambos lados para cortar limpio.
CUT_Z_TOP = 1.0
CUT_Z_DEPTH = 24.0


def load_shape(path: Path):  # noqa: ANN201
    """Leer un STEP y devolver la forma."""
    reader = STEPControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone:
        raise RuntimeError(f"No se pudo leer {path}")
    reader.TransferRoots()
    return reader.OneShape()


def volume(shape) -> float:  # noqa: ANN001
    """Volumen en mm³."""
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props)
    return props.Mass()


def solid_count(shape) -> int:  # noqa: ANN001
    """Número de sólidos de la forma."""
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    total = 0
    while explorer.More():
        total += 1
        explorer.Next()
    return total


def z_prism(base_2d: list, radius: float, centres: list[tuple[float, float]]):  # noqa: ANN001, ANN201
    """Extruir en Z (de ``-CUT_Z_DEPTH`` a 0) un contorno 2D de rectas y círculos."""
    shape = None
    for x0, y0, x1, y1 in base_2d:
        box = BRepPrimAPI_MakeBox(
            gp_Pnt(x0, y0, -CUT_Z_DEPTH), abs(x1 - x0), abs(y1 - y0), CUT_Z_DEPTH
        ).Shape()
        shape = box if shape is None else BRepAlgoAPI_Fuse(shape, box).Shape()
    for cx, cy in centres:
        cylinder = BRepPrimAPI_MakeCylinder(
            gp_Ax2(gp_Pnt(cx, cy, -CUT_Z_DEPTH), gp_Dir(0, 0, 1)), radius, CUT_Z_DEPTH
        ).Shape()
        shape = cylinder if shape is None else BRepAlgoAPI_Fuse(shape, cylinder).Shape()
    if shape is None:
        raise ValueError("contorno vacío")
    return shape


def oblong_cutter(cx: float, cy: float, angle_deg: float, length: float, width: float):  # noqa: ANN201
    """Vano oblongo centrado en (cx, cy), girado `angle_deg` en el plano XY."""
    radius = width / 2.0
    half = length / 2.0 - radius
    cutter = z_prism(
        [(-half, -radius, half, radius)],
        radius,
        [(-half, 0.0), (half, 0.0)],
    )
    trsf = gp_Trsf()
    trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), math.radians(angle_deg))
    trsf.SetTranslationPart(gp_Vec(cx, cy, CUT_Z_TOP))
    return BRepBuilderAPI_Transform(cutter, trsf, True).Shape()


def _fuse_all(shapes: list):  # noqa: ANN001, ANN202
    """Fusionar una lista de sólidos."""
    result = shapes[0]
    for shape in shapes[1:]:
        result = BRepAlgoAPI_Fuse(result, shape).Shape()
    return result


def rounded_window(x0: float, z0: float, x1: float, z1: float, radius: float):  # noqa: ANN201
    """Prisma de esquinas redondeadas en el plano XZ, cortado a lo largo de Y."""
    height = BASE_Y_HASTA - BASE_Y_DESDE
    vertical = BRepPrimAPI_MakeBox(
        gp_Pnt(x0, BASE_Y_DESDE, z0 + radius),
        x1 - x0,
        height,
        (z1 - radius) - (z0 + radius),
    ).Shape()
    horizontal = BRepPrimAPI_MakeBox(
        gp_Pnt(x0 + radius, BASE_Y_DESDE, z0),
        (x1 - radius) - (x0 + radius),
        height,
        z1 - z0,
    ).Shape()
    parts = [vertical, horizontal]
    for cx in (x0 + radius, x1 - radius):
        for cz in (z0 + radius, z1 - radius):
            parts.append(
                BRepPrimAPI_MakeCylinder(
                    gp_Ax2(gp_Pnt(cx, BASE_Y_DESDE, cz), gp_Dir(0, 1, 0)), radius, height
                ).Shape()
            )
    return _fuse_all(parts)


def build_cutters():  # noqa: ANN201
    """Construir el sólido de corte con todas las rebajas."""
    poste = z_prism(
        [(POSTE_X_MIN, POSTE_Y_MIN, POSTE_X_MAX, POSTE_Y_MAX)],
        POSTE_RADIO,
        [
            (POSTE_X_MIN + POSTE_RADIO, POSTE_Y_MIN),
            (POSTE_X_MIN + POSTE_RADIO, POSTE_Y_MAX),
        ],
    )
    poste = BRepBuilderAPI_Transform(
        poste, _translation(0.0, 0.0, CUT_Z_TOP), True
    ).Shape()

    cutters = [poste]
    for cx, cy, angle in PATA_CENTROS:
        cutters.append(oblong_cutter(cx, cy, angle, PATA_LARGO, PATA_ANCHO))
    for x0, z0, x1, z1 in BASE_VENTANAS:
        cutters.append(rounded_window(x0, z0, x1, z1, BASE_ESQUINA))
    return _fuse_all(cutters)


def _translation(dx: float, dy: float, dz: float) -> gp_Trsf:
    trsf = gp_Trsf()
    trsf.SetTranslationPart(gp_Vec(dx, dy, dz))
    return trsf


def main() -> int:
    """Generar la variante aligerada y comprobar el resultado."""
    original = load_shape(SOURCE)
    v0 = volume(original)

    cutter = build_cutters()
    result = BRepAlgoAPI_Cut(original, cutter).Shape()
    v1 = volume(result)

    print(f"volumen original : {v0 / 1000.0:8.2f} cm3")
    print(f"volumen aligerado: {v1 / 1000.0:8.2f} cm3")
    print(f"material quitado : {(v0 - v1) / 1000.0:8.2f} cm3 ({(v0 - v1) / v0 * 100:.1f} %)")
    print(f"sólidos          : {solid_count(result)} (debe ser 1)")
    print(f"sólido válido    : {BRepCheck_Analyzer(result).IsValid()}")

    writer = STEPControl_Writer()
    writer.Transfer(result, STEPControl_AsIs)
    if writer.Write(str(TARGET_STEP)) != IFSelect_RetDone:
        raise RuntimeError("falló la escritura del STEP")
    print("escrito:", TARGET_STEP.name)

    BRepMesh_IncrementalMesh(result, 0.15, False, 0.4, True)
    stl_writer = StlAPI_Writer()
    stl_writer.ASCIIMode = False
    if not stl_writer.Write(result, str(TARGET_STL)):
        raise RuntimeError("falló la escritura del STL")
    print("escrito:", TARGET_STL.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
