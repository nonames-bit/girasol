"""Lectura y fusión del raster.

Referencia normativa: ``docs/02-matematicas.md`` §5.1 y §5.2.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

# Radios por canal, de radio menor (0) a radio mayor (M-1). Ver docs/00-brief.md §3.
CHANNEL_RADII_MM: tuple[float, ...] = (30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140)

N_SCANS: int = 100
M_CHANNELS: int = 12

Raster = NDArray[np.bool_]


def load_raster(path: str) -> Raster:
    """Cargar un raster crudo desde disco.

    Parameters
    ----------
    path : str
        Ruta a un raster serializado (formato PENDIENTE).

    Returns
    -------
    Raster
        Matriz booleana de forma ``(N_SCANS, M_CHANNELS)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.1.
    """
    raise NotImplementedError("Fase 1: definir el formato de raster y su carga.")


def merge_arms(raster_raw: Raster) -> Raster:
    """Fusionar los brazos A y B corrigiendo el desfase de media vuelta.

    Los canales pares (brazo A) se copian tal cual. Los impares (brazo B) se toman
    de la fila ``(k + N/2) mod N``.

    Parameters
    ----------
    raster_raw : Raster
        Raster crudo de forma ``(N_SCANS, M_CHANNELS)``.

    Returns
    -------
    Raster
        Raster fusionado de igual forma.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.2. Con ``N = 100`` el desfase es 50 filas.
    """
    raise NotImplementedError("Fase 2: implementar la fusión de brazos (§5.2).")
