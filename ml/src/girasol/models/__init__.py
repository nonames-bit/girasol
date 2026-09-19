"""Modelos de clasificación.

Los tres modelos del brief (``docs/02-matematicas.md`` §5.9) se entrenan aquí y se
exportan a un layout de pesos común, para que el PLC pueda evaluar cualquiera de
ellos con el mismo UDT.
"""

from __future__ import annotations

from girasol.models.logistic import LogisticModel
from girasol.models.mlp import MLPModel
from girasol.models.tree import DecisionTreeModel

__all__ = ["DecisionTreeModel", "LogisticModel", "MLPModel"]
