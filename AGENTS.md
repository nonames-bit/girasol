# AGENTS.md — Reglas del repositorio Girasol

> Documento normativo para agentes. Se lee automáticamente. Ante cualquier duda de
> contexto, la fuente última es [`docs/00-brief.md`](docs/00-brief.md) (copia íntegra
> del brief de arranque).

> **Nota de desviación:** el brief original pedía `.kilocode/rules/` y
> `.kilocode/modes/custom-modes.yaml`. Este repositorio usa `AGENTS.md` + `.kilo/agent/`
> porque es lo que la versión actual de Kilo Code carga. El contenido es equivalente.

---

## 1. Contexto del proyecto

**Girasol** es un sistema de **visión industrial sin cámara**. Una mesa giratoria pasa
una pieza bajo una fila de sensores fotoeléctricos discretos. El PLC acumula las lecturas
binarias en una matriz que representa la silueta de la pieza, calcula descriptores
geométricos, y ejecuta un clasificador de machine learning **dentro del propio PLC**.

Los pesos se entrenan en Python y se despliegan al PLC por OPC UA, con validación en
sombra antes de que el modelo nuevo tome control.

**Qué NO es:** no es un sistema de seguridad (ningún sensor es componente de seguridad),
no compite con una cámara industrial en resolución, no usa deep learning pesado.

### Glosario

| Término | Definición |
| --- | --- |
| **Barrido** / fila | Una lectura simultánea de los M canales. Vector de M bits. |
| **Raster** | Matriz de N barridos × M canales acumulada durante una vuelta. |
| **Canal** | Un sensor. Numerados de 0 (radio menor) a M−1 (radio mayor). |
| **Brazo A / brazo B** | Mitades de la viga diametral. A lleva canales pares, B impares. |
| **Índice / home** | Sensor que lee una marca en el canto del plato, una vez por vuelta. |
| **Feature** | Descriptor numérico calculado sobre el raster. |
| **Vector dorado** | Par (raster de entrada, salida esperada) para validar ST contra Python. |
| **Modo sombra** | El modelo nuevo infiere en paralelo sin actuar, solo para comparar. |
| **BGS** | Background suppression. Supresión de fondo por triangulación. |

### Hardware

| Elemento | Especificación | Cantidad |
| --- | --- | --- |
| Sensor fotoeléctrico | Balluff, difuso con BGS, PNP NO/NC, M8 4 pines, 10–30 VDC | 17 disponibles |
| Canales radiales | 12 en uso (6 por brazo) | 12 |
| Índice de home | 1 sensor al canto del plato | 1 |
| Reserva | Sin montar | 4 |
| PLC principal | Omron NX102-9000 | 1 |
| Entradas digitales | 2 × NX-ID5442 (32 puntos) | 2 |
| Salidas digitales | NX-OD5256 | 1 |
| PLC secundario | Allen-Bradley CompactLogix L33ER | 1 |
| Motor | NEMA 17 | 1 |
| Driver | TB6600, entradas 24 V, cátodo común | 1 |
| Fuente | 24 VDC, 3 A mínimo | 1 |
| Cordsets | M8 hembra 4 pines | 13 |

### Geometría del array

- Viga diametral recta apoyada en dos postes (pórtico, no voladizo).
- Brazo A, radios: 30, 50, 70, 90, 110, 130 mm.
- Brazo B, radios: 40, 60, 80, 100, 120, 140 mm.
- Paso entre vecinos del mismo brazo: 20 mm. Resolución radial combinada: 10 mm.
- Desfase angular entre brazos: 180°, es decir N/2 barridos exactos.
- Orientación del cuerpo: eje largo (43 mm) tangencial, eje corto (11 mm) radial.
- Distancia de trabajo: 50–80 mm entre cara óptica y plato.

### Parámetros de movimiento

| Parámetro | Valor | Símbolo |
| --- | --- | --- |
| Micropasos por vuelta | 1600 (1/8 de paso, 200 pasos/vuelta) | S |
| Micropasos por barrido | 16 | s |
| Barridos por vuelta | 100 | N |
| Resolución angular | 3.6° | Δθ |
| Período de pulso | 2 ms | Tp |
| Duración de vuelta | 3.2 s | Trev |
| Canales | 12 | M |

---

## 2. Convenciones de código

### Python

- Formato: `ruff format`. Lint: `ruff check`. Tipos: `mypy --strict` en `src/`.
- Docstrings estilo NumPy, en español, citando la fórmula de `docs/02-matematicas.md`.
- Sin números mágicos: todo parámetro geométrico o de captura vive en `ml/configs/`.
- `pytest` con `--cov`, umbral mínimo 85 % en `features.py`.
- Semillas fijas en todo lo que use aleatoriedad.
- `ml/src/girasol/features.py` es **la implementación de referencia**. El ST se valida
  contra ella, nunca al revés.

### Structured Text

- Un POU por responsabilidad. Nada de un bloque de 800 líneas.
- Nombres en inglés (convención de planta), comentarios en español.
- Prefijos de tipo: `b` booleano, `i` entero, `r` real, `a` array, `s` string.
- Constantes en un solo lugar, en un UDT de configuración.
- Cada POU que calcula algo de la sección 5 lleva en su encabezado la referencia exacta:
  `(* Ver docs/02-matematicas.md sección 5.4 *)`.

### Marcado de lo desconocido

Si un valor, terminal, dirección o unidad **no está** en el brief ni en el código, se
marca `PENDIENTE`. **Prohibido inventar cifras.**

---

## 3. Restricciones duras de Structured Text

Estas reglas no se negocian. Un agente que las ignore está produciendo código inválido.

- **Sin recursión.** Ninguna POU se llama a sí misma, directa o indirectamente.
- **Sin memoria dinámica.** No hay asignación en tiempo de ejecución; todo array tiene
  tamaño constante declarado en compilación.
- **Sin bucles no acotados.** Prohibido `WHILE` sin cota explícita. Preferir `FOR` con
  número de iteraciones constante.
- **Sin llamadas bloqueantes.** Ninguna POU espera a un evento; el ciclo no se detiene.
- **Un POU por responsabilidad.**
- **Todo POU declara su tiempo de ejecución peor caso** en el encabezado.
- **Constantes centralizadas** en un UDT de configuración, nunca literales dispersos.
- **Sin punteros ni direccionamiento indirecto** no soportado por el estándar.
- Si el código porta una fórmula de la sección 5, la cita es obligatoria.

---

## 4. Git y commits

Commits en **Conventional Commits con scope obligatorio**:

```
<tipo>(<scope>): <descripción en imperativo>

[cuerpo opcional]

[footer opcional: Closes #12]
```

- **Tipos:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `exp`.
- **Scopes:** `plc`, `ml`, `edge`, `scada`, `hw`, `docs`, `repo`.
- **`exp`** marca un experimento cuyo resultado se registra pero cuyo código puede no
  sobrevivir.
- Nunca commits directos a `main`. Siempre pull request, aunque trabajes solo.
- `CHANGELOG.md` se actualiza en el mismo PR que introduce el cambio.

---

## 5. Definition of Done

Una tarea está terminada cuando **todas** se cumplen:

- [ ] El código pasa lint, tipos y tests en CI.
- [ ] Si toca un cálculo de la sección 5, el test de paridad ST/Python pasa.
- [ ] La documentación afectada está actualizada en el mismo PR.
- [ ] `CHANGELOG.md` tiene su entrada.
- [ ] Si fue una decisión de diseño, hay un ADR.
- [ ] El PR explica *por qué*, no solo *qué*.
- [ ] Si es hardware, hay foto del montaje en `docs/`.

---

## 6. Antipatrones

- Pedir "implementa la fase 2". Demasiado grande: el agente inventa.
- Dejar que el agente elija el algoritmo. Es una decisión de diseño con ADR.
- Aceptar código sin correr el test. Un agente puede escribir tests que pasan siempre.
- Dar acceso a `data/` o a credenciales.
- "Arreglar" un test rojo relajando la tolerancia.
