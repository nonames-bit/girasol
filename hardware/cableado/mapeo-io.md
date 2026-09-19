# Mapeo de entradas y salidas

> Fuente de los datos ciertos: `docs/00-brief.md` §3.
> Todo número de punto/terminal ausente del brief está marcado **`PENDIENTE`**.

## 1. Entradas digitales — canales radiales

12 canales radiales en uso. Numeración del brief: **canal 0 = radio menor**, creciente.
Brazo A lleva canales pares; brazo B, impares.

| Canal | Brazo | Radio (mm) | Tipo de señal | Punto en NX102 | Conductor |
| --- | --- | --- | --- | --- | --- |
| CH00 | A | 30 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH01 | B | 40 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH02 | A | 50 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH03 | B | 60 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH04 | A | 70 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH05 | B | 80 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH06 | A | 90 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH07 | B | 100 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH08 | A | 110 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH09 | B | 120 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH10 | A | 130 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |
| CH11 | B | 140 | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |

Resolución radial combinada: 10 mm. Paso entre vecinos del mismo brazo: 20 mm.
Desfase angular entre brazos: 180° (N/2 = 50 barridos, con N = 100).

## 2. Entradas digitales — índice de home

| Señal | Función | Tipo de señal | Punto en NX102 | Conductor |
| --- | --- | --- | --- | --- |
| HOME | Marca en el canto del plato, una vez por vuelta | PNP, 24 VDC | `PENDIENTE` | `PENDIENTE` |

## 3. Entradas del driver de motor (salidas del PLC)

El TB6600 se comanda con señales de 24 V, cátodo común. Ver
`esquema-control.md` para el detalle eléctrico.

| Señal | Función | Punto en NX-OD5256 | Conductor |
| --- | --- | --- | --- |
| PUL | Tren de pulsos, 16 micropasos por barrido | `PENDIENTE` | `PENDIENTE` |
| DIR | Sentido de giro | `PENDIENTE` | `PENDIENTE` |
| ENA | Habilitación del driver | `PENDIENTE` | `PENDIENTE` |

Parámetros de movimiento (`docs/00-brief.md` §3): 1600 micropasos/vuelta, 16
micropasos/barrido, 100 barridos/vuelta, período de pulso 2 ms, vuelta 3.2 s.

## 4. Salidas digitales — baliza de resultado

| Señal | Función | Punto en NX-OD5256 | Conductor |
| --- | --- | --- | --- |
| LAMP_* | Indicación de clase / rechazo según resultado | `PENDIENTE` | `PENDIENTE` |

El número de colores de la baliza y el mapeo clase → color están **`PENDIENTE`**.

## 5. Módulos de E/S

| Módulo | Función | Cantidad | Puntos | Notas |
| --- | --- | --- | --- | --- |
| NX-ID5442 | Entradas digitales | 2 | 32 puntos c/u (brief §3) | Encabezado de buses del NX102 |
| NX-OD5256 | Salidas digitales | 1 | `PENDIENTE` (no consta en el brief) | Requiere datasheet |

## 6. Sensores

- 17 sensores Balluff difuso con BGS disponibles; 12 en uso, 1 de home, 4 de reserva.
- Cordsets M8 hembra 4 pines: 13.
- Distancia de trabajo: 50–80 mm entre cara óptica y plato.

**Discrepancia abierta:** el brief §3 cita el modelo `BOS ...-PU-RH10-S75`, mientras que
los CAD presentes en `CAD/` corresponden a `BALLUFF BOS 18MR-PA-LD10-S4`. Confirmar el
modelo realmente montado. El mapeo de hilos del conector M8 4 pines depende de eso:
**`PENDIENTE`**.
