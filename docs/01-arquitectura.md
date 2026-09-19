# 01 — Arquitectura

> Categoría Diátaxis: **Explicación**. Responde *por qué está hecho así*.
> Fuente: `docs/00-brief.md` §4. Los diagramas son normativos; el texto explicativo
> se completa con los `TODO`.

## 1. Capas del sistema

```mermaid
flowchart TD
  S[Array de sensores<br/>12 canales + home] --> P[PLC NX102<br/>captura, features, inferencia]
  P --> A[Actuador<br/>baliza o rechazo]
  P --> G[SCADA Ignition<br/>HMI y OEE]
  P --> E[Nodo edge<br/>captura de dataset]
  G --> B[Broker MQTT<br/>Sparkplug B]
  E --> B
  B --> H[Historian<br/>series y rasters]
  H --> T[Entrenamiento<br/>Python]
  T -->|pesos por OPC UA| P
```

La decisión rápida nunca sale del PLC. Si el enlace al edge se cae, la máquina sigue
clasificando y actuando.

<!-- TODO: desarrollar por qué la decisión vive en el PLC y no en el edge/PC.
     Argumento: latencia determinista, disponibilidad sin red, ciclo de scan acotado.
     Referir a docs/02-matematicas.md §5.11 para el costo computacional. -->

## 2. Ciclo de una pieza

```mermaid
sequenceDiagram
  participant O as Operario
  participant PLC
  participant M as Motor
  participant ML as Modelo en PLC
  O->>PLC: pieza colocada, arranque
  PLC->>M: pulsos, busca home
  M-->>PLC: marca de índice
  loop 100 barridos
    PLC->>M: 16 micropasos
    PLC->>PLC: leer 12 bits, guardar fila
  end
  PLC->>PLC: fusionar brazo B con desfase N/2
  PLC->>PLC: calcular features
  PLC->>ML: vector de features
  ML-->>PLC: clase y confianza
  PLC->>O: resultado en baliza o HMI
```

<!-- TODO: detallar el tiempo de cada etapa (peor caso) y de dónde sale cada número. -->

## 3. Máquina de estados del ciclo

```mermaid
stateDiagram-v2
  [*] --> Reposo
  Reposo --> BuscandoHome: arranque
  BuscandoHome --> Capturando: índice detectado
  BuscandoHome --> Fallo: timeout
  Capturando --> Fusionando: 100 barridos
  Capturando --> Fallo: índice fuera de cuenta
  Fusionando --> Calculando
  Calculando --> Infiriendo
  Infiriendo --> Decidiendo
  Decidiendo --> Reposo: resultado publicado
  Fallo --> Reposo: reconocido
```

<!-- TODO: listar cada transición, su condición exacta y el temporizador asociado.
     El timeout de búsqueda de home está PENDIENTE (no está en el brief). -->

## 4. Pipeline del modelo

```mermaid
flowchart LR
  D[Dataset<br/>rasters etiquetados] --> F[Features<br/>Python]
  F --> N[Normalización<br/>media y desviación]
  N --> E[Entrenamiento<br/>árbol, logística, MLP]
  E --> V[Validación<br/>holdout estratificado]
  V --> X[Exportación<br/>pesos y escalas]
  X --> R[Registro<br/>versión, métricas, hash]
  R --> O[Despliegue<br/>OPC UA]
  O --> SH[Modo sombra<br/>N piezas]
  SH --> PR[Producción]
```

<!-- TODO: describir el contrato entre cada etapa y el layout del UDT de pesos.
     Ver docs/03-contrato-datos.md. -->

## 5. Decisiones y su razonamiento

- **Por qué el PLC y no una PC:** <!-- TODO -->
- **Por qué Sparkplug B y no MQTT plano:** <!-- TODO -->
- **Por qué brazos a 180°:** ver `docs/adr/0002-viga-diametral-180.md`.
- **Por qué PLC Omron como plataforma de captura:** ver `docs/adr/0001-plc-de-captura.md`.
- **Por qué un feature no invariante a reflexión:** ver `docs/02-matematicas.md` §5.6.

## 6. Conexiones

- Conexiones eléctricas: `hardware/cableado/`.
- Contrato de datos (OPC UA, Sparkplug, UDT de pesos): `docs/03-contrato-datos.md`.
- Tipos compartidos entre plataformas: `plc/shared/contratos.md`.
