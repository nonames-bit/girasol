# ADR-0002 — Viga diametral con brazos a 180°

- Estado: aceptado
- Fecha: 2026-09-19

## Contexto

Los sensores deben cubrir el radio con resolución fina, pero el cuerpo mide 43 mm
en dirección tangencial y no caben contiguos.

## Opciones consideradas

1. Una sola fila radial, paso 14 mm. Plato de 500 mm, imposible de imprimir.
2. Dos filas paralelas separadas 25 mm. El desfase angular depende del radio, lo
   que obliga a corregir canal por canal.
3. Viga diametral, brazos a 180°, radios intercalados.

## Decisión

Opción 3.

## Consecuencias

- El desfase es constante: N/2 barridos exactos. Obliga a que N sea par.
- La captura necesita una vuelta y media de datos antes de fusionar.
- Estructura de pórtico, sin flexión de voladizo.
- Ningún sensor queda a menos de 20 mm de otro.

## Referencias

- `docs/00-brief.md` §3 (geometría del array), §5.2 (fusión de brazos).
- Implementación de la fusión: `docs/02-matematicas.md` §5.2.
