# Cableado — índice

Esquemas y mapeos de conexión **eléctrica** de Girasol.

## Documentos

| Archivo | Contenido |
| --- | --- |
| [`mapeo-io.md`](mapeo-io.md) | Canal / señal → punto de entrada o salida del PLC |
| [`esquema-potencia.md`](esquema-potencia.md) | Alimentación 24 V, driver TB6600, motor NEMA 17 |
| [`esquema-control.md`](esquema-control.md) | Pulsos de paso, home, baliza de resultado |

## Convención de nombres

- Canales radiales: `CH00` … `CH11`, de radio menor (0) a radio mayor (11).
- Brazo A = canales pares; brazo B = canales impares (ver `docs/00-brief.md` §3).
- Índice de home: `HOME`.
- Señales de motor: `PUL`, `DIR`, `ENA`.
- Baliza de resultado: `LAMP_*`.

## Regla de honestidad de estos documentos

Los números de terminal, borneras y colores de conductor que **no** están en
`docs/00-brief.md` se marcan **`PENDIENTE`**. No se rellenan por estimación. Para
completarlos hace falta el datasheet de los módulos NX y el plano de borneras que se
construya en el taller.

## Advertencia de seguridad

Ningún sensor de este sistema es componente de seguridad. No usar este sistema como
protección de personas. Ver `docs/00-brief.md` §1.
