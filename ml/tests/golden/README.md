# Vectores dorados

Un **vector dorado** es un par (raster de entrada, salida esperada) que valida el ST
contra Python. Es la única forma aceptable de demostrar paridad numérica.

## Estructura

```
tests/golden/
├── README.md          # este archivo
├── <slug>.json        # salida esperada de Python
└── st/
    └── <slug>.json    # salida de referencia del ST para el mismo raster
```

El `slug` debe coincidir entre ambos archivos.

## Formato propuesto (PENDIENTE ratificar)

```json
{
  "slug": "rectangulo-centrado",
  "descripcion": "Rectángulo 43x11 mm centrado, eje corto radial",
  "math_ref": "docs/02-matematicas.md §5.7",
  "params": {
    "n_scans": 100,
    "m_channels": 12,
    "radii_mm": [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
  },
  "raster_raw": [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
  "features": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}
```

- `raster_raw` es la entrada **cruda**, antes de fusionar brazos.
- `features` tiene 10 elementos en el orden de `docs/02-matematicas.md` §5.7.
- Ninguno de los valores de ejemplo de arriba es real: son marcadores de forma.

## Reglas

- Un vector dorado **no se regenera** porque una implementación discrepe. Primero se
  determina cuál de las dos se desvía de `docs/02-matematicas.md`.
- La tolerancia de comparación es `1e-4` relativa. No se relaja para poner verde un test.
- Todo vector debe citar la sección de matemáticas que verifica.
