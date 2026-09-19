"""Pruebas de paridad ST vs Python.

Compara la implementación de referencia con las salidas de referencia del ST
guardadas en ``tests/golden/st/``. Falla si la diferencia relativa supera ``1e-4``
(``docs/00-brief.md`` §8.6).

Se salta mientras no existan vectores dorados, para no romper CI en el andamiaje.
"""

from __future__ import annotations

from pathlib import Path

import pytest

GOLDEN_DIR = Path(__file__).parent / "golden"
ST_GOLDEN_DIR = GOLDEN_DIR / "st"

venv_golden_available = any(GOLDEN_DIR.glob("*.json")) and any(ST_GOLDEN_DIR.glob("*.json"))

pytestmark = pytest.mark.skipif(
    not venv_golden_available,
    reason="No hay vectores dorados todavía. Ver tests/golden/README.md.",
)

RELATIVE_TOLERANCE = 1e-4


def test_relative_tolerance_is_the_agreed_value() -> None:
    """La tolerancia de paridad es la declarada en el brief §8.6."""
    assert RELATIVE_TOLERANCE == 1e-4


def test_features_match_st_reference() -> None:
    """Cada feature debe coincidir con la salida de referencia del ST."""
    raise AssertionError("Pendiente: comparar tests/golden/*.json contra tests/golden/st/*.json.")
