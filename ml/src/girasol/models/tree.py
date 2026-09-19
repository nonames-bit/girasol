"""Árbol de decisión compilable a IF/THEN.

El árbol se elige porque se compila a comparaciones anidadas: cero
multiplicaciones, determinista y auditable (``docs/02-matematicas.md`` §5.9).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from girasol.features import FeatureVector


@dataclass
class DecisionTreeModel:
    """Árbol de decisión aplanado para exportar al PLC.

    Attributes
    ----------
    max_depth : int
        Profundidad máxima. El brief tabula profundidad 5 (§5.9).
    nodes : NDArray
        Representación aplanada del árbol. El layout exacto está PENDIENTE.
    """

    max_depth: int = 5
    nodes: NDArray[np.float64] = field(default_factory=lambda: np.empty(0))

    def fit(self, features: NDArray[np.float64], labels: NDArray[np.int_]) -> DecisionTreeModel:
        """Entrenar el árbol.

        Parameters
        ----------
        features : ndarray
            Matriz ``(n_samples, 10)``.
        labels : ndarray
            Vector de clases ``(n_samples,)``.

        Returns
        -------
        DecisionTreeModel
            El propio modelo, ya entrenado.
        """
        raise NotImplementedError("Fase 2: entrenar el árbol. Requiere ADR del layout aplanado.")

    def predict(self, features: FeatureVector) -> int:
        """Predecir la clase de un vector de features.

        Parameters
        ----------
        features : FeatureVector
            Vector de 10 features.

        Returns
        -------
        int
            Índice de clase.
        """
        raise NotImplementedError("Fase 2: implementar la evaluación del árbol.")
