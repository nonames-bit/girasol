# ml — implementación de referencia

Python para features, entrenamiento y exportación de pesos. **`src/girasol/features.py`
es la implementación de referencia del proyecto**: el Structured Text del PLC se valida
contra ella, nunca al revés (`docs/00-brief.md` §6).

## Estado

Andamiaje. Las firmas existen y la lógica se implementa en la Fase 2. Por eso el gate de
cobertura del 85 % sobre `features.py` **falla hasta que la Fase 2 esté implementada**:
es el comportamiento esperado, no un defecto de la configuración.

## Instalación

```bash
cd ml
python -m venv .venv
# activar el entorno
pip install -e ".[dev]"
```

## Comandos

```bash
ruff format .
ruff check .
mypy --strict src/
pytest --cov=girasol.features --cov-fail-under=85
```

## Estructura

| Ruta | Qué es |
| --- | --- |
| `src/girasol/config.py` | Carga de `configs/girasol.yaml`; fuente única de constantes (añadido, ver abajo) |
| `src/girasol/raster.py` | Carga y fusión de brazos (§5.1, §5.2) |
| `src/girasol/features.py` | Momentos, invariantes y vector de 10 features (§5.3–5.7) |
| `src/girasol/models/` | Árbol, regresión logística y MLP (§5.9) |
| `src/girasol/export.py` | Pesos a JSON y a constantes ST |
| `src/girasol/conformal.py` | Reject option por conformal prediction (§5.10) |
| `src/girasol/synth.py` | Rasterizador sintético desde STL (Fase 5) |
| `src/girasol/cli.py` | Interfaz de línea de comandos |
| `tests/golden/` | Vectores dorados para paridad ST↔Python |
| `configs/girasol.yaml` | Parámetros geométricos y de captura |
| `notebooks/` | Exploración. Nada de producción importa desde aquí |

### Desviación del brief

`src/girasol/config.py` no aparece en la estructura de la sección 6 del brief. Se añadió
para cumplir su propia regla de §7 ("sin números mágicos: todo parámetro geométrico o de
captura vive en `configs/`"): sin un cargador, los valores del YAML y las constantes del
código quedaban duplicados y podían divergir en silencio. Es la única forma de que el
YAML sea de verdad la fuente única.

## Reglas

- Sin números mágicos: todo parámetro vive en `configs/`.
- Docstrings NumPy en español, citando la fórmula que implementan.
- Semillas fijas en todo lo aleatorio.
- Nunca relajar una tolerancia para poner verde un test rojo.
