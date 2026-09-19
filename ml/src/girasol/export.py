"""Exportación de pesos a JSON y a constantes de Structured Text.

Referencia: ``docs/03-contrato-datos.md`` §3 define el layout del UDT de pesos.
``mu``, ``sigma`` y ``q_hat`` viajan con los pesos, siempre como una unidad
(``docs/02-matematicas.md`` §5.8).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def to_json(payload: dict[str, Any], path: Path) -> None:
    """Escribir el paquete de pesos como JSON versionado.

    Parameters
    ----------
    payload : dict
        Diccionario con ``version``, ``model_kind``, ``k``, ``mu``, ``sigma``,
        matrices de pesos y ``q_hat``.
    path : Path
        Destino del archivo.

    Notes
    -----
    Ver ``docs/03-contrato-datos.md`` §3.
    """
    raise NotImplementedError("Fase 2: implementar la exportación a JSON.")


def to_st_constants(weights: dict[str, Any], path: Path) -> None:
    """Emitir los pesos como constantes de Structured Text.

    Parameters
    ----------
    weights : dict
        Paquete de pesos en memoria.
    path : Path
        Destino del archivo ``.st`` generado.

    Notes
    -----
    Las matrices deben emitirse en el mismo orden de índices que
    ``plc/omron-nx102/udt/``. Ver ``docs/03-contrato-datos.md`` §3.
    """
    raise NotImplementedError("Fase 2: implementar la exportación a ST.")


def load_normalization(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Cargar ``mu`` y ``sigma`` desde el registro de modelos.

    Parameters
    ----------
    path : Path
        Ruta al JSON de pesos registrado.

    Returns
    -------
    tuple of ndarray
        ``(mu, sigma)``, ambos de longitud 10.
    """
    raise NotImplementedError("Fase 2: implementar la carga de normalización (§5.8).")
