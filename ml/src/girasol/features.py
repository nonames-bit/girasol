"""Descriptores geométricos — implementación de referencia.

Este módulo es la referencia normativa ejecutable de ``docs/02-matematicas.md``
§5.3 a §5.7. Cualquier divergencia con el ST es un fallo del ST.

El raster se indexa ``B[k, j]`` con ``k`` el barrido (0..99) y ``j`` el canal
(0..11). Cada celda se pondera por el radio del canal, ``w_j = r_j`` (§5.3),
porque en polares las celdas exteriores cubren más área física.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from girasol.raster import CHANNEL_RADII_MM, M_CHANNELS, N_SCANS, Raster

FeatureVector = NDArray[np.float64]

N_FEATURES: int = 10

# Delta radial entre canales contiguos, en mm (docs/00-brief.md §3).
DELTA_R_MM: float = 10.0


def _polar_coordinates() -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Construir las coordenadas polares y cartesianas de cada celda.

    Returns
    -------
    tuple of ndarray
        ``theta`` de forma ``(N_SCANS, 1)``, ``x`` e ``y`` de forma
        ``(N_SCANS, M_CHANNELS)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.1: ``theta_k = 2*pi*k/N``, con
    ``x = r*cos(theta)`` e ``y = r*sin(theta)``.
    """
    raise NotImplementedError("Fase 2: implementar (§5.1, §5.4).")


def raw_moments(raster: Raster) -> tuple[float, float, float]:
    """Calcular los momentos crudos ``M00``, ``M10`` y ``M01``.

    Parameters
    ----------
    raster : Raster
        Raster fusionado.

    Returns
    -------
    tuple of float
        ``(M00, M10, M01)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.4, con corrección de área polar ``w_j = r_j``.
    """
    raise NotImplementedError("Fase 2: implementar (§5.4).")


def central_moments(raster: Raster) -> tuple[float, float, float]:
    """Calcular los momentos centrales ``mu20``, ``mu02`` y ``mu11``.

    Parameters
    ----------
    raster : Raster
        Raster fusionado.

    Returns
    -------
    tuple of float
        ``(mu20, mu02, mu11)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.4.
    """
    raise NotImplementedError("Fase 2: implementar (§5.4).")


def hu_invariants(
    mu20: float, mu02: float, mu11: float, m00: float
) -> tuple[float, float, float]:
    """Calcular ``phi1``, ``phi2`` y ``phi7`` con signo.

    Parameters
    ----------
    mu20, mu02, mu11 : float
        Momentos centrales de segundo orden.
    m00 : float
        Momento de orden cero, usado para normalizar.

    Returns
    -------
    tuple of float
        ``(phi1, phi2, phi7)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.6. ``phi7`` **no** es invariante a reflexión:
    es la excepción deliberada para detectar piezas volteadas.
    """
    raise NotImplementedError("Fase 2: implementar (§5.6).")


def elongation(mu20: float, mu02: float, mu11: float) -> tuple[float, float]:
    """Calcular elongación y excentricidad a partir de los autovalores.

    Parameters
    ----------
    mu20, mu02, mu11 : float
        Momentos centrales de segundo orden.

    Returns
    -------
    tuple of float
        ``(elongacion, excentricidad)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.5.
    """
    raise NotImplementedError("Fase 2: implementar (§5.5).")


def compute_features(raster: Raster) -> FeatureVector:
    """Calcular el vector de 10 features del raster fusionado.

    Parameters
    ----------
    raster : Raster
        Raster fusionado, forma ``(N_SCANS, M_CHANNELS)``.

    Returns
    -------
    FeatureVector
        Vector de longitud ``N_FEATURES`` en el orden de la tabla §5.7.

    Raises
    ------
    ValueError
        Si el raster está vacío (``M00`` nulo) o su forma no es la esperada.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.7.
    """
    raise NotImplementedError("Fase 2: implementar el vector de features (§5.7).")


__all__ = [
    "CHANNEL_RADII_MM",
    "DELTA_R_MM",
    "M_CHANNELS",
    "N_FEATURES",
    "N_SCANS",
    "central_moments",
    "compute_features",
    "elongation",
    "hu_invariants",
    "raw_moments",
]
