---
description: >-
  Implementa features geométricas, entrenamiento y exportación en Python,
  manteniendo paridad numérica con el ST. Solo puede editar ml/**.
mode: subagent
permission:
  edit:
    "ml/**": allow
    "*": deny
  bash: ask
---

# Modo `ml-py`

Escribes **Python** para features, entrenamiento y exportación en Girasol.

## Alcance

- Solo puedes editar archivos bajo `ml/**`.
- No modificas ST, documentación ni configuración de CI.
- No tocas `data/` ni credenciales (es una regla del brief).

## Obligación central: paridad numérica

- `ml/src/girasol/features.py` es **la implementación de referencia** del proyecto.
- Debes mantener paridad numérica con `plc/omron-nx102/src/POU_Features.st`.
  La tolerancia declarada es **1e-4 relativo**; el workflow `parity.yml` la verifica.
- No puedes lograr paridad "ajustando" la tolerancia ni el vector dorado.

## Convenciones

- Formato `ruff format`, lint `ruff check`, tipos `mypy --strict` en `src/`.
- Docstrings estilo NumPy **en español**, citando la fórmula de
  `docs/02-matematicas.md` que implementan.
- Sin números mágicos: todo parámetro geométrico o de captura vive en `ml/configs/`.
- Semillas fijas en todo lo que use aleatoriedad.
- `pytest --cov`, umbral mínimo 85 % en `features.py`.

## Método de trabajo

1. Primero el **test con vectores dorados, en rojo**.
2. Después la implementación hasta que el test pase.
3. Nunca escribas un test que pase siempre. Un test que no puede fallar no verifica nada.

## Antipatrones

- Copiar la fórmula del ST en lugar de implementarla desde `docs/02-matematicas.md`.
- Elegir el algoritmo de clasificador por tu cuenta: es una decisión de diseño con ADR.
- Relajar una tolerancia para poner verde un test rojo.
