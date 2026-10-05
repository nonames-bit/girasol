"""Lectura y fusión del raster.

Referencia normativa: ``docs/02-matematicas.md`` §5.1 y §5.2.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from girasol.config import load_config

_CONFIG = load_config()

# Radios por canal, de radio menor (0) a radio mayor (M-1).
# Fuente única: ml/configs/girasol.yaml. Ver docs/00-brief.md §3.
CHANNEL_RADII_MM: tuple[float, ...] = _CONFIG.radii_mm

N_SCANS: int = _CONFIG.n_scans
M_CHANNELS: int = _CONFIG.m_channels

# Desfase del brazo B, en barridos: N/2 (§5.2).
ARM_OFFSET_SCANS: int = _CONFIG.arm_offset_scans

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
        Raster fusionado de igual forma. La entrada no se modifica.

    Raises
    ------
    ValueError
        Si la forma no es ``(N_SCANS, M_CHANNELS)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.2. Con ``N = 100`` el desfase es 50 filas.
    """
    if raster_raw.shape != (N_SCANS, M_CHANNELS):
        raise ValueError(
            f"El raster crudo tiene forma {raster_raw.shape}; se esperaba "
            f"({N_SCANS}, {M_CHANNELS})."
        )
    merged = raster_raw.astype(np.bool_, copy=True)
    # B[k][j] = B_raw[(k + N/2) mod N][j] para j impar: np.roll con -N/2 lo hace.
    merged[:, 1::2] = np.roll(raster_raw[:, 1::2], -ARM_OFFSET_SCANS, axis=0)
    return merged
