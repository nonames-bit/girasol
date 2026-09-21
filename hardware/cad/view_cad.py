"""Visor local de los CAD de Girasol en el panel OCP CAD Viewer de VS Code.

Herramienta de taller: no forma parte del build ni es una dependencia de `ml/`.
Requiere `ocp-vscode` (que trae el kernel OCP) en el intérprete de Python que usa
VS Code.

Uso
---
1. ``Ctrl+Shift+P`` → ``OCP CAD Viewer: Open viewer``.
2. Ejecutar este archivo (botón Run, o desde la terminal):

   ``python hardware/cad/view_cad.py Soporte2.stp Soportegrande.stl``

   Sin argumentos, muestra todos los CAD de esta carpeta.

El modelo aparece en el panel del visor, no en una ventana aparte.
"""

from __future__ import annotations

import sys
from pathlib import Path

from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.StlAPI import StlAPI_Reader
from OCP.TopoDS import TopoDS_Shape
from ocp_vscode import show

CAD_DIR = Path(__file__).resolve().parent

STEP_SUFFIXES: set[str] = {".stp", ".step"}
STL_SUFFIXES: set[str] = {".stl"}
SUPPORTED_SUFFIXES: set[str] = STEP_SUFFIXES | STL_SUFFIXES


def load_step(path: Path) -> TopoDS_Shape:
    """Cargar un archivo STEP y devolver la forma del kernel.

    Parameters
    ----------
    path : Path
        Archivo ``.stp`` o ``.step``.

    Returns
    -------
    TopoDS_Shape
        Forma cargada.

    Raises
    ------
    RuntimeError
        Si el kernel no puede leer el archivo.
    """
    reader = STEPControl_Reader()
    status = reader.ReadFile(str(path))
    if status != IFSelect_RetDone:
        raise RuntimeError(f"{path.name}: STEPControl_Reader falló (status={status}).")
    reader.TransferRoots()
    return reader.OneShape()


def load_stl(path: Path) -> TopoDS_Shape:
    """Cargar una malla STL, binaria o ASCII.

    Parameters
    ----------
    path : Path
        Archivo ``.stl``.

    Returns
    -------
    TopoDS_Shape
        Malla cargada como forma del kernel.

    Raises
    ------
    RuntimeError
        Si el kernel no puede leer el archivo.
    """
    shape = TopoDS_Shape()
    if not StlAPI_Reader().Read(shape, str(path)):
        raise RuntimeError(f"{path.name}: StlAPI_Reader falló.")
    return shape


def load(path: Path) -> TopoDS_Shape:
    """Cargar un CAD según su extensión.

    Parameters
    ----------
    path : Path
        Archivo de entrada.

    Returns
    -------
    TopoDS_Shape
        Forma cargada.

    Raises
    ------
    ValueError
        Si la extensión no está soportada.
    """
    suffix = path.suffix.lower()
    if suffix in STEP_SUFFIXES:
        return load_step(path)
    if suffix in STL_SUFFIXES:
        return load_stl(path)
    raise ValueError(f"{path.name}: extensión no soportada ({suffix or 'sin extensión'}).")


def resolve(names: list[str]) -> list[Path]:
    """Resolver los archivos a mostrar.

    Parameters
    ----------
    names : list of str
        Nombres o rutas. Vacío significa "todos los CAD de esta carpeta".

    Returns
    -------
    list of Path
        Rutas resueltas, ordenadas cuando se autodetectan.
    """
    if not names:
        return sorted(
            item
            for item in CAD_DIR.iterdir()
            if item.is_file() and item.suffix.lower() in SUPPORTED_SUFFIXES
        )
    return [p if p.is_absolute() else CAD_DIR / p for p in map(Path, names)]


def main(argv: list[str]) -> int:
    """Cargar los CAD indicados y mostrarlos en el panel del visor.

    Parameters
    ----------
    argv : list of str
        Nombres de archivo o rutas.

    Returns
    -------
    int
        Código de salida.
    """
    paths = resolve(argv)
    if not paths:
        print(f"No hay CAD en {CAD_DIR}.")
        return 1

    shapes: list[TopoDS_Shape] = []
    names: list[str] = []
    for path in paths:
        if not path.is_file():
            print(f"Omitido (no existe): {path}")
            continue
        try:
            shape = load(path)
        except (RuntimeError, ValueError) as exc:
            print(f"Error: {exc}")
            continue
        shapes.append(shape)
        names.append(path.name)
        print(f"Cargado: {path.name}")

    if not shapes:
        return 1

    show(*shapes, names=names)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
