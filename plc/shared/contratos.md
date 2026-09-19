# Contratos compartidos entre plataformas

> Tipos y constantes comunes al Omron NX102-9000 y al Allen-Bradley CompactLogix L33ER.
> Este archivo no debe contener nada específico de una plataforma: si aparece una
> sintaxis concreta, es un error.
> Ver `docs/03-contrato-datos.md` para el contrato OPC UA.

## 1. Constantes de configuración

Deben existir en un **único** UDT de configuración por plataforma
(`plc/omron-nx102/udt/`), nunca como literales dispersos.

| Constante | Valor | Origen |
| --- | --- | --- |
| `N_SCANS` | 100 | `docs/00-brief.md` §3 |
| `M_CHANNELS` | 12 | `docs/00-brief.md` §3 |
| `N_FEATURES` | 10 | `docs/02-matematicas.md` §5.7 |
| `K_CLASSES` | `PENDIENTE` | 4 en §5.11; 4 + variante volteada en §11 |
| `MICROSTEPS_PER_REV` | 1600 | `docs/00-brief.md` §3 |
| `MICROSTEPS_PER_SCAN` | 16 | `docs/00-brief.md` §3 |
| `PULSE_PERIOD_MS` | 2 | `docs/00-brief.md` §3 |
| `HALF_REV_SCANS` | `N_SCANS / 2` = 50 | `docs/02-matematicas.md` §5.2 |
| `EPSILON` | `1e-8` | `docs/02-matematicas.md` §5.8 |
| `PARITY_TOL` | `1e-4` | `docs/00-brief.md` §8.6 |

## 2. Tipos

### 2.1 Raster

- Concepto: matriz `[k][j]` de bits, `k` = barrido (0…99), `j` = canal (0…11).
- Omron: `ARRAY[0..99, 0..11] OF BOOL`.
- Allen-Bradley: `BOOL[100,12]` (o empaquetado en `DINT` si el tiempo de scan lo exige;
  esa decisión es un ADR aparte si se toma).

### 2.2 Features

- Concepto: vector de 10 `REAL`, orden fijo de `docs/02-matematicas.md` §5.7.
- Índices: 0 área, 1 φ₁, 2 φ₂, 3 φ₇, 4 elongación, 5 ancho de anillo, 6 transiciones,
  7 compacidad, 8 fracción de filas, 9 λ₁/λ₂.

### 2.3 Estado del ciclo

| Valor | Nombre | Significado |
| --- | --- | --- |
| 0 | `IDLE` | Reposo |
| 1 | `SEEKING_HOME` | Buscando el índice |
| 2 | `CAPTURING` | Acumulando barridos |
| 3 | `MERGING` | Fusionando brazos |
| 4 | `COMPUTING` | Calculando features |
| 5 | `INFERRING` | Inferencia |
| 6 | `DECIDING` | Publicando resultado |
| 7 | `FAULT` | Fallo |

### 2.4 Clase y rechazo

- `iClass`: entero, `0…K-1`; `-1` = sin decisión.
- `bReject`: verdadero si el conjunto de predicción conformal no tiene exactamente un
  elemento (`docs/02-matematicas.md` §5.10).

### 2.5 Pesos

Estructura idéntica a la de `docs/03-contrato-datos.md` §3. Regla: `rMu`, `rSigma`,
`rW1`, `rB1`, `rW2`, `rB2`, `rQhat` se actualizan **como una unidad**, nunca por campo.

## 3. Reglas de paridad

- Todo POU que porte una fórmula de la sección 5 se valida contra
  `ml/tests/golden/` con tolerancia relativa `1e-4`.
- La implementación de referencia es `ml/src/girasol/features.py`; el ST se valida
  contra ella, nunca al revés (`docs/00-brief.md` §6).
- El ST se porta **desde `docs/02-matematicas.md`**, no leyendo el Python: es
  verificación por implementación independiente (`docs/00-brief.md` §9.5).

## 4. Pendientes

- Representación aplanada del árbol de decisión: `PENDIENTE` (requiere ADR).
- Empaquetado del raster en la plataforma AB: `PENDIENTE` (requiere medir scan).
- Catálogo de `FaultCode`: `PENDIENTE`.
