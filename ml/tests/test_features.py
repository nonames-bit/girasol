"""Pruebas de los descriptores geométricos.

Implementación de referencia: ``docs/02-matematicas.md`` §5.3–5.7.
Las pruebas numéricas se activan en la Fase 2, cuando existan los vectores dorados.
"""

from __future__ import annotations

import pytest

from girasol import features, raster


def test_raster_dimensions_match_brief() -> None:
    """N y M deben ser los del brief (§3): 100 barridos y 12 canales."""
    assert raster.N_SCANS == 100
    assert raster.M_CHANNELS == 12


def test_n_scans_is_even_for_half_turn_offset() -> None:
    """El desfase de brazo B es N/2, así que N debe ser par (§5.2)."""
    assert raster.N_SCANS % 2 == 0


def test_channel_radii_match_array_geometry() -> None:
    """Los radios por canal deben cubrir 30..140 mm con paso de 10 mm (§3)."""
    assert raster.CHANNEL_RADII_MM == (30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140)
    assert len(raster.CHANNEL_RADII_MM) == raster.M_CHANNELS


def test_feature_vector_length_is_ten() -> None:
    """El vector de features tiene exactamente 10 componentes (§5.7)."""
    assert features.N_FEATURES == 10


@pytest.mark.skip(reason="Fase 2: requiere vectores dorados y la fusión de brazos.")
def test_compute_features_matches_golden_vector() -> None:
    """Paridad exacta contra el vector dorado del set de referencia (§5.7)."""
    raise AssertionError("Pendiente: cargar el vector dorado y comparar con tolerancia 1e-4.")
