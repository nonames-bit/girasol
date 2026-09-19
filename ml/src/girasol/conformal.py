"""Reject option por conformal prediction.

Referencia: ``docs/02-matematicas.md`` §5.10. El umbral ``q_hat`` es el cuantil
empírico de los scores de no-conformidad ``s_i = 1 - p_{y_i}``, y el conjunto de
predicción es ``Gamma(x) = {c : 1 - p_c <= q_hat}``.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def nonconformity(probabilities: NDArray[np.float64], labels: NDArray[np.int_]) -> NDArray[np.float64]:
    """Calcular los scores de no-conformidad ``s_i = 1 - p_{y_i}``.

    Parameters
    ----------
    probabilities : ndarray
        Matriz ``(n_samples, K)`` de probabilidades calibradas.
    labels : ndarray
        Etiquetas verdaderas ``(n_samples,)``.

    Returns
    -------
    ndarray
        Scores ``(n_samples,)``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.10.
    """
    raise NotImplementedError("Fase 4: implementar el score de no-conformidad (§5.10).")


def conformal_quantile(scores: NDArray[np.float64], alpha: float) -> float:
    """Calcular el cuantil empírico ``q_hat``.

    Parameters
    ----------
    scores : ndarray
        Scores de no-conformidad del set de calibración.
    alpha : float
        Nivel de error objetivo (1 - confianza).

    Returns
    -------
    float
        Umbral ``q_hat``.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.10. El valor de ``alpha`` está PENDIENTE.
    """
    raise NotImplementedError("Fase 4: implementar el cuantil conformal (§5.10).")


def prediction_set(probabilities: NDArray[np.float64], q_hat: float) -> list[int]:
    """Construir el conjunto de predicción ``Gamma(x)``.

    Parameters
    ----------
    probabilities : ndarray
        Probabilidades ``p_c`` para una muestra.
    q_hat : float
        Umbral conformal.

    Returns
    -------
    list of int
        Clases ``c`` con ``1 - p_c <= q_hat``. Si la longitud no es 1, la pieza va
        a inspección manual.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.10.
    """
    raise NotImplementedError("Fase 4: implementar el conjunto de predicción (§5.10).")


def softmax(logits: NDArray[np.float64]) -> NDArray[np.float64]:
    """Softmax estabilizado restando el máximo.

    Parameters
    ----------
    logits : ndarray
        Vector ``z`` de salida del modelo.

    Returns
    -------
    ndarray
        Probabilidades que suman 1.

    Notes
    -----
    Ver ``docs/02-matematicas.md`` §5.9. La resta del máximo evita el desborde de
    ``REAL`` en el PLC; no omitirla.
    """
    raise NotImplementedError("Fase 2: implementar softmax estabilizado (§5.9).")
