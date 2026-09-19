# 03 — Contrato de datos

> Categoría Diátaxis: **Referencia**. Responde *cuál es el valor exacto de X*.
> Sin este documento, Python y el PLC se desincronizan en la primera semana
> (`docs/00-brief.md` §10.2).
>
> **Estado del contrato:** propuesta inicial de andamiaje. Los **nombres** de nodo
> propuestos aquí son diseño y deben ratificarse antes de la Fase 3. Los **valores
> numéricos** que no constan en el brief van como `PENDIENTE`.

## 1. Convenciones

- Namespace OPC UA propuesto: `urn:girasol:plc` (ratificar).
- Tipos IEC: `BOOL`, `INT`, `DINT`, `UDINT`, `REAL`, `STRING`.
- Unidades: `mm` para longitudes, `°` para ángulos, adimensional para features.
- El raster es `ARRAY[0..99, 0..11] OF BOOL` (N=100, M=12) y significa `[k][j]`
  = barrido `k`, canal `j`.

## 2. Tags OPC UA — operación

### 2.1 Estado del ciclo

| Nodo propuesto | Tipo | Acceso | Unidad | Descripción |
| --- | --- | --- | --- | --- |
| `Status.State` | `INT` | R | — | Estado de la máquina de estados (`docs/01-arquitectura.md` §3) |
| `Status.FaultCode` | `INT` | R | — | Código de fallo; catálogo `PENDIENTE` |
| `Status.CycleCount` | `UDINT` | R | — | Vueltas completadas |
| `Status.HomeFound` | `BOOL` | R | — | Índice de home detectado en la vuelta actual |
| `Status.ScanIndex` | `INT` | R | — | Barrido en curso, 0…99 |

### 2.2 Captura

| Nodo propuesto | Tipo | Acceso | Unidad | Descripción |
| --- | --- | --- | --- | --- |
| `Capture.Raster` | `ARRAY[0..99,0..11] OF BOOL` | R/W | — | Raster crudo de la vuelta |
| `Capture.RasterValid` | `BOOL` | R | — | La vuelta se completó sin fallo |
| `Capture.RawChannels` | `ARRAY[0..11] OF BOOL` | R | — | Lectura instantánea de los 12 canales |

### 2.3 Features

Vector de 10 features, en el orden de `docs/02-matematicas.md` §5.7.

| Nodo propuesto | Tipo | Acceso | Unidad | Descripción |
| --- | --- | --- | --- | --- |
| `Features.Value` | `ARRAY[0..9] OF REAL` | R | mixta | Ver tabla siguiente |
| `Features.Valid` | `BOOL` | R | — | Features calculados sin división por cero |

| Índice | Feature | Unidad |
| --- | --- | --- |
| 0 | Área física $A$ | mm² |
| 1 | $\varphi_1$ | adimensional |
| 2 | $\varphi_2$ | adimensional |
| 3 | $\varphi_7$ con signo | adimensional |
| 4 | Elongación | adimensional |
| 5 | $\rho_{\max}-\rho_{\min}$ | mm |
| 6 | Transiciones medias por fila | adimensional |
| 7 | Compacidad $P^2/A$ | 1/mm² |
| 8 | Fracción de filas ocupadas | adimensional |
| 9 | $\lambda_1/\lambda_2$ | adimensional |

### 2.4 Inferencia

| Nodo propuesto | Tipo | Acceso | Unidad | Descripción |
| --- | --- | --- | --- | --- |
| `Inference.Class` | `INT` | R | — | Clase ganadora (argmax) |
| `Inference.Confidence` | `REAL` | R | 0…1 | $p_c$ con softmax estabilizado (§5.9) |
| `Inference.Reject` | `BOOL` | R | — | $|\Gamma(x)| \neq 1$: va a inspección manual |
| `Inference.PredictionSet` | `ARRAY[0..K-1] OF BOOL` | R | — | Conjunto de predicción conformal |

**`PENDIENTE`:** valor exacto de `K` (número de clases). El brief §5.11 tabula K=4;
el §11 de la Fase 2 menciona 4 clases más una variante volteada.

### 2.5 Modelo y modo sombra

| Nodo propuesto | Tipo | Acceso | Unidad | Descripción |
| --- | --- | --- | --- | --- |
| `Model.Version` | `STRING` | R/W | — | Identificador de versión desplegada |
| `Model.ShadowActive` | `BOOL` | R/W | — | Modo sombra habilitado |
| `Model.ShadowClass` | `INT` | R | — | Clase que predice el modelo nuevo |
| `Model.ShadowAgree` | `BOOL` | R | — | El modelo nuevo coincide con el activo |
| `Model.ShadowCount` | `UDINT` | R/W | — | Piezas evaluadas en sombra en la corrida |
| `Model.ShadowThreshold` | `UDINT` | R/W | piezas | N piezas en sombra antes de conmutar (**`PENDIENTE`**) |
| `Model.WeightBank` | `INT` | R/W | — | Banco activo: 0 = A, 1 = B |

### 2.6 Escritura de pesos

Todos los nodos de `Weights.*` se escriben **juntos** en un solo banco; nunca se
actualiza un campo suelto, porque $\mu$, $\sigma$ y los pesos deben ir versionados
como una unidad (`docs/02-matematicas.md` §5.8).

## 3. UDT de pesos (`Weights`)

Debe ser idéntico en ambas plataformas (ver `plc/shared/contratos.md`).

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `sVersion` | `STRING[15]` | Versión del modelo |
| `iModelKind` | `INT` | 0 = árbol, 1 = logística, 2 = MLP |
| `iK` | `INT` | Número de clases (`PENDIENTE`) |
| `iNFeatures` | `INT` | 10 |
| `rMu` | `ARRAY[0..9] OF REAL` | Media por feature (§5.8) |
| `rSigma` | `ARRAY[0..9] OF REAL` | Desviación por feature (§5.8) |
| `rEpsilon` | `REAL` | $10^{-8}$ (§5.8) |
| `rW1` | `ARRAY[0..11,0..9] OF REAL` | Pesos de entrada (logística o MLP) |
| `rB1` | `ARRAY[0..11] OF REAL` | Sesgos de la primera capa |
| `rW2` | `ARRAY[0..K-1,0..11] OF REAL` | Pesos de salida |
| `rB2` | `ARRAY[0..K-1] OF REAL` | Sesgos de salida |
| `rQhat` | `REAL` | Umbral conformal $\hat{q}$ (§5.10) |
| `rAlpha` | `REAL` | Nivel de confianza objetivo (`PENDIENTE`) |
| `aTreeNodes` | `ARRAY[0..31] OF REAL` | Árbol aplanado, profundidad ≤ 5 |

**`PENDIENTE`:** la representación exacta del árbol aplanado (índices de hijo, umbral,
feature, hoja) no está especificada en el brief. Requiere un diseño explícito antes de
la Fase 2 y probablemente un ADR.

## 4. Payload MQTT Sparkplug B

Publicación propuesta en el `NDATA` de un `DDATA` por pieza terminada.

| Métrica | Tipo Sparkplug | Unidad | Descripción |
| --- | --- | --- | --- |
| `Class` | `Int32` | — | Clase decidida |
| `Confidence` | `Double` | — | $p_c$ |
| `Reject` | `Boolean` | — | Va a inspección manual |
| `Feature0`…`Feature9` | `Double` | mixta | Vector de features |
| `CycleCount` | `UInt32` | — | Contador de vueltas |
| `ModelVersion` | `String` | — | Versión del modelo activo |
| `State` | `Int32` | — | Estado al cerrar el ciclo |

Periodicidad de publicación, QoS, y si los rasters viajan por Sparkplug o solo por el
colector OPC UA: **`PENDIENTE`**.

## 5. Referencias

- Fórmulas normativas: `docs/02-matematicas.md`.
- Tipos compartidos entre plataformas: `plc/shared/contratos.md`.
- Conmutación de banco: `docs/00-brief.md` §11, Fase 4.
