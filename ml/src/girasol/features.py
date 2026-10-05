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

from girasol.config import load_config
from girasol.raster import CHANNEL_RADII_MM, M_CHANNELS, N_SCANS, Raster

_CONFIG = load_config()

FeatureVector = NDArray[np.float64]

N_FEATURES: int = _CONFIG.n_features

# Delta radial entre canales contiguos, en mm. Fuente única: ml/configs/girasol.yaml.
DELTA_R_MM: float = _CONFIG.delta_r_mm


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
    k = np.arange(N_SCANS, dtype=np.float64).reshape(-1, 1)
    theta = 2.0 * np.pi * k / N_SCANS
    r = np.asarray(CHANNEL_RADII_MM, dtype=np.float64).reshape(1, -1)
    return theta, r * np.cos(theta), r * np.sin(theta)


def _area_weights(raster: Raster) -> NDArray[np.float64]:
    """Peso de área de cada celda encendida, ``B[k][j] * r_j``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.3: ``w_j = r_j``.
    """
    r = np.asarray(CHANNEL_RADII_MM, dtype=np.float64).reshape(1, -1)
    return raster.astype(np.float64) * r


def _centred_coordinates(
    raster: Raster,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Pesos y desvíos respecto del centroide, ``(B r, x - x̄, y - ȳ)``.

    Raises
    ------
    ValueError
        Si el raster está vacío: con ``M00 = 0`` el centroide no existe.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.4: ``x̄ = M10 / M00``, ``ȳ = M01 / M00``.
    """
    m00, m10, m01 = raw_moments(raster)
    if m00 == 0.0:
        raise ValueError("Raster vacío: M00 = 0, el centroide no está definido.")
    _, x, y = _polar_coordinates()
    return _area_weights(raster), x - m10 / m00, y - m01 / m00


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
    w = _area_weights(raster)
    _, x, y = _polar_coordinates()
    return float(w.sum()), float((w * x).sum()), float((w * y).sum())


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

    Raises
    ------
    ValueError
        Si el raster está vacío (``M00 = 0``).

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.4.
    """
    w, dx, dy = _centred_coordinates(raster)
    return float((w * dx**2).sum()), float((w * dy**2).sum()), float((w * dx * dy).sum())


def central_moments_order3(raster: Raster) -> tuple[float, float, float, float]:
    """Calcular los momentos centrales de tercer orden.

    Parameters
    ----------
    raster : Raster
        Raster fusionado.

    Returns
    -------
    tuple of float
        ``(mu30, mu03, mu21, mu12)``.

    Raises
    ------
    ValueError
        Si el raster está vacío (``M00 = 0``).

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.4. Son necesarios para ``phi7`` (§5.6).
    """
    w, dx, dy = _centred_coordinates(raster)
    return (
        float((w * dx**3).sum()),
        float((w * dy**3).sum()),
        float((w * dx**2 * dy).sum()),
        float((w * dx * dy**2).sum()),
    )


def hu_invariants(
    mu20: float,
    mu02: float,
    mu11: float,
    mu30: float,
    mu03: float,
    mu21: float,
    mu12: float,
    m00: float,
) -> tuple[float, float, float]:
    """Calcular ``phi1``, ``phi2`` y ``phi7`` con signo.

    Parameters
    ----------
    mu20, mu02, mu11 : float
        Momentos centrales de segundo orden.
    mu30, mu03, mu21, mu12 : float
        Momentos centrales de tercer orden, requeridos por ``phi7``.
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
    "central_moments_order3",
    "compute_features",
    "elongation",
    "hu_invariants",
    "raw_moments",
]
