"""Rasterizador sintético desde STL.

Permite generar rasters etiquetados sin capturar hardware, y construir vectores
dorados reproducibles. Ver ``docs/00-brief.md`` §11, Fase 5.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from girasol.raster import M_CHANNELS, N_SCANS, Raster


def rasterize_stl(
    stl_path: Path,
    n_scans: int = N_SCANS,
    m_channels: int = M_CHANNELS,
) -> Raster:
    """Rasterizar una malla STL a la rejilla polar del sistema.

    Parameters
    ----------
    stl_path : Path
        Malla de la pieza.
    n_scans : int, optional
        Barridos por vuelta. Por defecto ``N_SCANS``.
    m_channels : int, optional
        Canales radiales. Por defecto ``M_CHANNELS``.

    Returns
    -------
    Raster
        Raster booleano ``(n_scans, m_channels)`` sin el desfase de brazos.

    Notes
    -----
    Los radios por canal están en ``girasol.raster.CHANNEL_RADII_MM``.
    """
    raise NotImplementedError("Fase 5: implementar el rasterizador sintético.")


def sample_positions(rng: np.random.Generator, count: int) -> NDArray[np.float64]:
    """Sortear posiciones ``(x, y, angulo)`` de la pieza en el plato.

    Parameters
    ----------
    rng : numpy.random.Generator
        Generador con semilla fija: la aleatoriedad siempre es reproducible.
    count : int
        Número de muestras.

    Returns
    -------
    ndarray
        Matriz ``(count, 3)``.
    """
    raise NotImplementedError("Fase 5: implementar el muestreo de posiciones.")
