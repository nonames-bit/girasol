"""Perceptrón multicapa 10-12-K.

Referencia: ``docs/02-matematicas.md`` §5.9,
``h = tanh(W1 x_hat + b1)``, ``z = W2 h + b2``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from girasol.features import FeatureVector


@dataclass
class MLPModel:
    """MLP de una capa oculta.

    Attributes
    ----------
    w1 : NDArray
        Pesos de entrada, forma ``(n_hidden, 10)``.
    b1 : NDArray
        Sesgos de la capa oculta, longitud ``n_hidden``.
    w2 : NDArray
        Pesos de salida, forma ``(K, n_hidden)``.
    b2 : NDArray
        Sesgos de salida, longitud ``K``.
    """

    w1: NDArray[np.float64]
    b1: NDArray[np.float64]
    w2: NDArray[np.float64]
    b2: NDArray[np.float64]

    def fit(self, features: NDArray[np.float64], labels: NDArray[np.int_]) -> MLPModel:
        """Entrenar el MLP.

        Parameters
        ----------
        features : ndarray
            Matriz ``(n_samples, 10)`` ya normalizada.
        labels : ndarray
            Vector de clases ``(n_samples,)``.

        Returns
        -------
        MLPModel
            El propio modelo, ya entrenado.
        """
        raise NotImplementedError("Fase 2: entrenar el MLP 10-12-K (§5.9).")

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
        raise NotImplementedError("Fase 2: implementar el forward pass (§5.9).")
