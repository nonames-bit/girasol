"""Vectores dorados de la fusión de brazos y de los momentos polares.

Referencia: ``docs/02-matematicas.md`` §5.1 a §5.4.

Los valores esperados están derivados a mano a partir de las fórmulas, no de la
implementación: cada caso coloca unas pocas celdas en ángulos donde ``cos`` y ``sin``
valen 0 o ±1, de modo que las sumas se pueden hacer en papel. Las cuentas están en el
docstring de cada caso. La tolerancia es la del brief §8.6 y no se relaja.
"""

from __future__ import annotations

import numpy as np
import pytest

from girasol import features, raster

RTOL = 1e-4
# Escala absoluta para comparar ceros: sin(pi) en float64 no es exactamente 0.
ATOL = 1e-6

# Barridos con ángulo exacto: theta_k = 2*pi*k/N (§5.1), con N = 100.
K_0_DEG = 0
K_90_DEG = 25
K_180_DEG = 50
K_270_DEG = 75


def _empty() -> raster.Raster:
    return np.zeros((raster.N_SCANS, raster.M_CHANNELS), dtype=np.bool_)


def _cells(*cells: tuple[int, int]) -> raster.Raster:
    """Raster fusionado con las celdas ``(k, j)`` indicadas encendidas."""
    b = _empty()
    for k, j in cells:
        b[k, j] = True
    return b


# ---------------------------------------------------------------------------
# §5.2 Fusión de brazos
# ---------------------------------------------------------------------------


def test_merge_arms_keeps_arm_a_channels() -> None:
    """Los canales pares (brazo A) se copian sin desplazar."""
    raw = _cells((10, 0), (73, 4), (99, 10))
    merged = raster.merge_arms(raw)
    assert merged[10, 0] and merged[73, 4] and merged[99, 10]
    assert merged.sum() == 3


def test_merge_arms_shifts_arm_b_by_half_turn() -> None:
    """Canal impar: ``B[k][j] = B_raw[(k + N/2) mod N][j]``.

    ``B_raw[0][1]`` aparece en ``k`` tal que ``(k + 50) mod 100 = 0``, es decir ``k = 50``.
    ``B_raw[60][11]`` aparece en ``k = 10``.
    """
    raw = _cells((0, 1), (60, 11))
    merged = raster.merge_arms(raw)
    assert merged[50, 1]
    assert merged[10, 11]
    assert merged.sum() == 2


def test_merge_arms_wraps_around_the_turn() -> None:
    """El índice da la vuelta: ``B_raw[49][3]`` va a ``k = 99`` y ``B_raw[50][3]`` a ``k = 0``."""
    raw = _cells((49, 3), (50, 3))
    merged = raster.merge_arms(raw)
    assert merged[99, 3]
    assert merged[0, 3]
    assert merged.sum() == 2


def test_merge_arms_is_an_involution() -> None:
    """Desplazar media vuelta dos veces devuelve el raster original (N par)."""
    rng = np.random.default_rng(20261005)
    raw = rng.random((raster.N_SCANS, raster.M_CHANNELS)) < 0.3
    np.testing.assert_array_equal(raster.merge_arms(raster.merge_arms(raw)), raw)


def test_merge_arms_does_not_modify_input() -> None:
    """La fusión devuelve un raster nuevo; la entrada cruda queda intacta."""
    raw = _cells((0, 1))
    before = raw.copy()
    raster.merge_arms(raw)
    np.testing.assert_array_equal(raw, before)


def test_merge_arms_rejects_wrong_shape() -> None:
    """Un raster que no es ``(N, M)`` es un error, no un caso a adivinar."""
    with pytest.raises(ValueError, match="forma"):
        raster.merge_arms(np.zeros((raster.N_SCANS, raster.M_CHANNELS + 1), dtype=np.bool_))


# ---------------------------------------------------------------------------
# §5.4 Momentos crudos (con peso w_j = r_j de §5.3)
# ---------------------------------------------------------------------------


def test_raw_moments_single_cell() -> None:
    """Una celda en ``k = 0``, ``j = 0`` (r = 30 mm, punto (30, 0)).

    ``M00 = 30``, ``M10 = 30 * 30 = 900``, ``M01 = 30 * 0 = 0``.
    """
    m00, m10, m01 = features.raw_moments(_cells((K_0_DEG, 0)))
    assert m00 == pytest.approx(30.0, rel=RTOL)
    assert m10 == pytest.approx(900.0, rel=RTOL)
    assert m01 == pytest.approx(0.0, abs=ATOL)


def test_raw_moments_weight_by_radius_not_by_count() -> None:
    """Dos celdas en el mismo barrido valen distinto según su radio (§5.3).

    Canal 0 (30 mm) y canal 11 (140 mm) en ``k = 25`` (90°): ``M00 = 30 + 140 = 170``,
    ``M10 = 0``, ``M01 = 30 * 30 + 140 * 140 = 900 + 19600 = 20500``.
    """
    m00, m10, m01 = features.raw_moments(_cells((K_90_DEG, 0), (K_90_DEG, 11)))
    assert m00 == pytest.approx(170.0, rel=RTOL)
    assert m10 == pytest.approx(0.0, abs=ATOL)
    assert m01 == pytest.approx(20500.0, rel=RTOL)


def test_raw_moments_full_ring_is_centred() -> None:
    """Anillo completo en el canal 0: ``M00 = 100 * 30 = 3000`` y centroide en el origen."""
    ring = _empty()
    ring[:, 0] = True
    m00, m10, m01 = features.raw_moments(ring)
    assert m00 == pytest.approx(3000.0, rel=RTOL)
    assert m10 == pytest.approx(0.0, abs=ATOL)
    assert m01 == pytest.approx(0.0, abs=ATOL)


def test_raw_moments_empty_raster_is_zero() -> None:
    """Un raster vacío tiene momentos crudos nulos; no es un error en este nivel."""
    assert features.raw_moments(_empty()) == (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# §5.4 Momentos centrales de segundo orden
# ---------------------------------------------------------------------------


def test_central_moments_opposite_cells() -> None:
    """Celdas en 0° y 180° del canal 0: puntos (30, 0) y (-30, 0), peso 30 cada uno.

    Centroide (0, 0). ``mu20 = 30 * 900 + 30 * 900 = 54000``, ``mu02 = mu11 = 0``.
    """
    mu20, mu02, mu11 = features.central_moments(_cells((K_0_DEG, 0), (K_180_DEG, 0)))
    assert mu20 == pytest.approx(54000.0, rel=RTOL)
    assert mu02 == pytest.approx(0.0, abs=ATOL)
    assert mu11 == pytest.approx(0.0, abs=ATOL)


def test_central_moments_full_ring() -> None:
    """Anillo completo en el canal 0, r = 30.

    ``sum_k cos^2(2 pi k / 100) = 50``, así que ``mu20 = 30 * 900 * 50 = 1 350 000``.
    Igual para ``mu02``; ``sum_k cos sin = 0`` da ``mu11 = 0``.
    """
    ring = _empty()
    ring[:, 0] = True
    mu20, mu02, mu11 = features.central_moments(ring)
    assert mu20 == pytest.approx(1_350_000.0, rel=RTOL)
    assert mu02 == pytest.approx(1_350_000.0, rel=RTOL)
    assert mu11 == pytest.approx(0.0, abs=ATOL)


def test_central_moments_diagonal_pair() -> None:
    """Celdas en 0° y 90° del canal 0: puntos (30, 0) y (0, 30), peso 30 cada uno.

    Centroide (15, 15). Desvíos: (15, -15) y (-15, 15).
    ``mu20 = mu02 = 30 * 225 * 2 = 13500``, ``mu11 = 30 * (-225) * 2 = -13500``.
    """
    mu20, mu02, mu11 = features.central_moments(_cells((K_0_DEG, 0), (K_90_DEG, 0)))
    assert mu20 == pytest.approx(13500.0, rel=RTOL)
    assert mu02 == pytest.approx(13500.0, rel=RTOL)
    assert mu11 == pytest.approx(-13500.0, rel=RTOL)


def test_central_moments_are_translation_free_of_single_cell() -> None:
    """Una sola celda coincide con su centroide: todos los momentos centrales son 0."""
    mu20, mu02, mu11 = features.central_moments(_cells((K_270_DEG, 7)))
    assert (mu20, mu02, mu11) == pytest.approx((0.0, 0.0, 0.0), abs=ATOL)


def test_central_moments_reject_empty_raster() -> None:
    """Sin celdas el centroide no existe (``M00 = 0``): es un error explícito."""
    with pytest.raises(ValueError, match="M00"):
        features.central_moments(_empty())


# ---------------------------------------------------------------------------
# §5.4 Momentos centrales de tercer orden
# ---------------------------------------------------------------------------


def test_third_order_moments_collinear_asymmetric() -> None:
    """Canales 0 y 2 en 0°: puntos (30, 0) peso 30 y (50, 0) peso 50.

    ``M00 = 80``, ``M10 = 900 + 2500 = 3400``, ``x̄ = 42.5``. Desvíos en x: -12.5 y 7.5.
    ``mu30 = 30 * (-12.5)^3 + 50 * 7.5^3 = -58593.75 + 21093.75 = -37500``.
    Todo en ``y = 0``: ``mu03 = mu21 = mu12 = 0``.
    """
    mu30, mu03, mu21, mu12 = features.central_moments_order3(_cells((K_0_DEG, 0), (K_0_DEG, 2)))
    assert mu30 == pytest.approx(-37500.0, rel=RTOL)
    assert mu03 == pytest.approx(0.0, abs=ATOL)
    assert mu21 == pytest.approx(0.0, abs=ATOL)
    assert mu12 == pytest.approx(0.0, abs=ATOL)


def test_third_order_moments_mixed_terms() -> None:
    """Canal 0 en 0° y canal 2 en 90°: (30, 0) peso 30 y (0, 50) peso 50.

    ``M00 = 80``, ``x̄ = 900 / 80 = 11.25``, ``ȳ = 2500 / 80 = 31.25``.
    Desvíos: (18.75, -31.25) y (-11.25, 18.75).

    - ``mu30 = 30 * 18.75^3 + 50 * (-11.25)^3 = 197753.90625 - 71191.40625 = 126562.5``
    - ``mu03 = 30 * (-31.25)^3 + 50 * 18.75^3 = -915527.34375 + 329589.84375 = -585937.5``
    - ``mu21 = 30 * 18.75^2 * (-31.25) + 50 * 11.25^2 * 18.75
      = -329589.84375 + 118652.34375 = -210937.5``
    - ``mu12 = 30 * 18.75 * 31.25^2 + 50 * (-11.25) * 18.75^2
      = 549316.40625 - 197753.90625 = 351562.5``
    """
    mu30, mu03, mu21, mu12 = features.central_moments_order3(_cells((K_0_DEG, 0), (K_90_DEG, 2)))
    assert mu30 == pytest.approx(126562.5, rel=RTOL)
    assert mu03 == pytest.approx(-585937.5, rel=RTOL)
    assert mu21 == pytest.approx(-210937.5, rel=RTOL)
    assert mu12 == pytest.approx(351562.5, rel=RTOL)


def test_third_order_moments_change_sign_under_reflection() -> None:
    """Reflejar en el eje x (``k -> N - k``) invierte el signo de ``mu03`` y ``mu21``.

    Es la propiedad que hace que ``phi7`` detecte piezas volteadas (§5.6).
    """
    piece = _cells((K_0_DEG, 0), (K_90_DEG, 2), (10, 5))
    mirrored = _cells((K_0_DEG, 0), (raster.N_SCANS - K_90_DEG, 2), (raster.N_SCANS - 10, 5))
    mu30, mu03, mu21, mu12 = features.central_moments_order3(piece)
    mu30_m, mu03_m, mu21_m, mu12_m = features.central_moments_order3(mirrored)
    assert mu30_m == pytest.approx(mu30, rel=RTOL)
    assert mu12_m == pytest.approx(mu12, rel=RTOL)
    assert mu03_m == pytest.approx(-mu03, rel=RTOL)
    assert mu21_m == pytest.approx(-mu21, rel=RTOL)


def test_third_order_moments_reject_empty_raster() -> None:
    """Sin celdas no hay centroide (``M00 = 0``)."""
    with pytest.raises(ValueError, match="M00"):
        features.central_moments_order3(_empty())


# ---------------------------------------------------------------------------
# §5.1 Coordenadas polares
# ---------------------------------------------------------------------------


def test_polar_coordinates_shapes_and_quadrants() -> None:
    """``theta`` es ``(N, 1)``; ``x`` e ``y`` son ``(N, M)`` con ``x = r cos``, ``y = r sin``."""
    theta, x, y = features._polar_coordinates()
    assert theta.shape == (raster.N_SCANS, 1)
    assert x.shape == y.shape == (raster.N_SCANS, raster.M_CHANNELS)
    assert theta[K_90_DEG, 0] == pytest.approx(np.pi / 2, rel=RTOL)
    assert x[K_0_DEG, 11] == pytest.approx(140.0, rel=RTOL)
    assert y[K_90_DEG, 0] == pytest.approx(30.0, rel=RTOL)
    assert x[K_180_DEG, 1] == pytest.approx(-40.0, rel=RTOL)
    assert y[K_270_DEG, 2] == pytest.approx(-50.0, rel=RTOL)
