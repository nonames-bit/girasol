"""Regresión logística multiclase.

Referencia: ``docs/02-matematicas.md`` §5.9, ``z = W x_hat + b`` con
``W`` de forma ``(K, 10)``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from girasol.features import FeatureVector


@dataclass
class LogisticModel:
    """Modelo lineal multiclase.

    Attributes
    ----------
    weights : NDArray
        Matriz ``W`` de forma ``(K, 10)``.
    biases : NDArray
        Vector ``b`` de longitud ``K``.
    """

    weights: NDArray[np.float64] = field(default_factory=lambda: np.empty((0, 0)))
    biases: NDArray[np.float64] = field(default_factory=lambda: np.empty(0))

    def fit(self, features: NDArray[np.float64], labels: NDArray[np.int_]) -> LogisticModel:
        """Entrenar el modelo.

        Parameters
        ----------
        features : ndarray
            Matriz ``(n_samples, 10)`` ya normalizada.
        labels : ndarray
            Vector de clases ``(n_samples,)``.

        Returns
        -------
        LogisticModel
            El propio modelo, ya entrenado.
        """
        raise NotImplementedError("Fase 2: entrenar la regresión logística (§5.9).")

    def predict(self, features: FeatureVector) -> int:
        """Predecir la clase por ``argmax`` de ``z``.

        Parameters
        ----------
        features : FeatureVector
            Vector de 10 features normalizado.

        Returns
        -------
        int
            Índice de clase.
        """
        raise NotImplementedError("Fase 2: implementar argmax (§5.9).")
