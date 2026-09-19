# Girasol — Camera-Free Industrial Vision on a PLC

A rotating table carries a part under a diametral beam of 12 discrete photoelectric
sensors. A PLC accumulates the binary readings into a polar raster of the part's
silhouette, computes geometric descriptors by hand, and runs the machine-learning
classifier **inside the PLC itself** — no camera, no PC, no cloud in the decision loop.

<!-- TODO: replace with a photo of the assembled rig (docs/04-manual-montaje.md) -->
![Girasol rig](docs/diagramas/TODO-rig-photo.png)

<!-- TODO: replace with a 10-second GIF of the system classifying a part -->
![Girasol classifying](docs/diagramas/TODO-classification.gif)

## What it is

- **Camera-free vision.** 12 photoelectric sensors on a diametral beam sample the part's
  profile as it turns; the raster is assembled in the PLC's memory.
- **ML at cycle time.** Image moments, normalization, matrix-vector product, activation
  and argmax are all reimplemented in IEC 61131-3 Structured Text.
- **MLOps that survives the plant floor.** Weights are trained in Python, versioned,
  pushed over OPC UA, and validated in shadow mode before they take control.

The rotary stage turns at one revolution every 3.2 s; the classification decision never
leaves the controller.

## Stack

| Layer | Technology |
| --- | --- |
| Controller | Omron NX102-9000 (primary), Allen-Bradley CompactLogix L33ER (portability) |
| Sensors | 12 × Balluff BOS diffuse photoelectric with background suppression |
| Motion | NEMA 17 stepper + TB6600 driver |
| PLC language | IEC 61131-3 Structured Text (no libraries) |
| ML / training | Python, NumPy, scikit-learn |
| Data link | OPC UA (tags and weights), MQTT Sparkplug B |
| HMI / SCADA | Ignition Perspective |
| CI | GitHub Actions — lint, types, tests and ST↔Python parity on golden vectors |

## Repository layout

```
docs/       architecture, mathematics, data contract, manuals, ADRs
hardware/   CAD, STL, BOM, wiring, mounting jig
plc/        Omron NX102 and Allen-Bradley L33ER sources (Structured Text / L5X)
ml/         reference implementation in Python, models, golden vectors, tests
edge/       OPC UA collector and Sparkplug B bridge
scada/      Ignition project export
data/       dataset schema and checksums (no data lives here)
models/     model registry
```

## Documentation

| Document | Contents |
| --- | --- |
| [docs/01-arquitectura.md](docs/01-arquitectura.md) | Why the decision lives in the PLC, layer diagram, cycle state machine |
| [docs/02-matematicas.md](docs/02-matematicas.md) | Normative formulas the code is validated against |
| [docs/03-contrato-datos.md](docs/03-contrato-datos.md) | OPC UA tags, Sparkplug payload, weights UDT |
| [docs/04-manual-montaje.md](docs/04-manual-montaje.md) | Assembly, from printing to wiring |
| [docs/05-manual-operacion.md](docs/05-manual-operacion.md) | Start-up, dataset capture, fault handling |
| [docs/06-manual-entrenamiento.md](docs/06-manual-entrenamiento.md) | From dataset to deployed weights |
| [docs/07-explicacion-sencilla.md](docs/07-explicacion-sencilla.md) | Plain-language explanation, no formulas |

<!-- TODO: documentation is written in Spanish (see docs/00-brief.md); the section links above are stable. -->

## Status

<!-- TODO: keep this table in sync with the milestone tags in docs/00-brief.md §8.5 -->

| Milestone | Tag | Status |
| --- | --- | --- |
| Phase 1 — Mechanics and capture | `v0.1.0` | Not started |
| Phase 2 — Classifier in the PLC | `v0.2.0` | Not started |
| Phase 3 — SCADA and IoT | `v0.3.0` | Not started |
| Phase 4 — MLOps | `v0.4.0` | Not started |
| Phase 5 — Extensions | `v1.0.0` | Not started |

## Safety

This is **not** a safety system. No sensor in this rig is a safety component. Do not use
it as one.

## License

MIT — see [LICENSE](LICENSE).
