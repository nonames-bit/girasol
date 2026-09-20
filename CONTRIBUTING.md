# Contributing to Girasol

Gracias por el interés. Este repositorio es a la vez un proyecto de automatización y un
portafolio, así que la calidad del historial importa tanto como la del código.

## Reglas no negociables

1. **Nada de código sin su test.** Las features geométricas se validan contra vectores
   dorados antes de portarse a ST.
2. **Paridad numérica.** Todo cálculo implementado dos veces (Python y ST) debe producir
   resultados idénticos dentro de la tolerancia declarada (`1e-4` relativo). Lo verifica
   `parity.yml`.
3. **Los datasets no entran al repositorio.** Solo su esquema y su checksum.
4. **Cada decisión de arquitectura no obvia se registra como ADR** en `docs/adr/`.
5. **La documentación se escribe en español.** El `README.md` raíz va en inglés (portafolio).
6. **Commits en Conventional Commits.** Sin excepciones.
7. **Nunca commits directos a `main`.** Siempre pull request, aunque trabajes solo.

## Flujo de trabajo

```bash
git switch -c feat/nombre-corto
# trabaja, con commits pequeños y atómicos
git push -u origin feat/nombre-corto
gh pr create --fill
```

Modelo trunk-based con ramas cortas. `main` siempre desplegable.

| Prefijo | Uso | Vida |
| --- | --- | --- |
| `feat/` | funcionalidad nueva | días |
| `fix/` | corrección | horas |
| `docs/` | solo documentación | horas |
| `exp/` | experimento, puede morir | lo que dure |
| `hw/` | mecánica y CAD | días |

## Commits

```
<tipo>(<scope>): <descripción en imperativo>

[cuerpo opcional]

[footer opcional: Closes #12]
```

**Tipos:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `exp`.

**Scopes:** `plc`, `ml`, `edge`, `scada`, `hw`, `docs`, `repo`.

El tipo `exp` es propio de este proyecto: marca un experimento cuyo resultado se registra
pero cuyo código puede no sobrevivir.

Ejemplos válidos:

```
feat(ml): implementar momentos de Hu con corrección de área polar
fix(plc): corregir desfase de brazo B cuando N es impar
exp(ml): comparar MLP 10-12-4 contra logística en dataset v3
docs(hw): agregar cotas del gálibo de montaje
```

## Estilo

- **Python:** `ruff format` + `ruff check`, `mypy --strict` en `src/`, docstrings NumPy en
  español citando la fórmula correspondiente de `docs/02-matematicas.md`.
- **Structured Text:** un POU por responsabilidad; nombres en inglés; sin recursión, sin
  memoria dinámica, sin bucles no acotados; constantes en un UDT de configuración; cada
  POU cita la sección de matemáticas que implementa.
- Sin números mágicos: todo parámetro geométrico o de captura vive en `ml/configs/`.

Antes de abrir un PR:

```bash
cd ml
ruff format . && ruff check . && mypy --strict src/ && pytest --cov=girasol.features --cov-fail-under=85
```

## Definition of Done

Una tarea está terminada cuando **todas** se cumplen:

- [ ] El código pasa lint, tipos y tests en CI.
- [ ] Si toca un cálculo de la sección 5, el test de paridad ST/Python pasa.
- [ ] La documentación afectada está actualizada en el mismo PR.
- [ ] `CHANGELOG.md` tiene su entrada.
- [ ] Si fue una decisión de diseño, hay un ADR.
- [ ] El PR explica *por qué*, no solo *qué*.
- [ ] Si es hardware, hay foto del montaje en `docs/`.
