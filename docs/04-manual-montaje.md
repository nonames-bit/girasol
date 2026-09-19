# 04 — Manual de montaje

> Categoría Diátaxis: **Tutorial**. Responde *cómo aprendo esto desde cero*.
> Escrito para que alguien más lo reproduzca sin ayuda.
> Fuente: `docs/00-brief.md` §3 y §10.2.

## Índice

1. Seguridad previa
2. Lista de materiales (BOM)
3. Impresión de piezas
4. Montaje de la viga diametral
5. Posicionamiento con el gálibo
6. Cableado del TB6600
7. Enseñanza de los sensores
8. Verificación final

## 1. Seguridad previa

<!-- TODO: describir bloqueo/etiquetado, alimentación 24 V, riesgo del plato giratorio.
     Recordatorio obligatorio: ningún sensor de este sistema es componente de seguridad. -->

## 2. Lista de materiales

Ver `hardware/bom.csv`. Los proveedores y precios están **PENDIENTE**.

## 3. Impresión de piezas

- Plato: <!-- TODO: el brief §11 pide un plato de 310 mm en segmentos imprimibles. -->
- Portasensor con tope de altura contra el perfil (extrusión). Detalle **PENDIENTE**.
- Gálibo con agujero de centrado en el eje. Detalle **PENDIENTE**.

<!-- TODO: insertar fotos de cada paso terminado. Este documento no está completo sin imágenes. -->

## 4. Montaje de la viga diametral

- Viga diametral recta apoyada en dos postes (pórtico, no voladizo).
- Brazo A, radios: 30, 50, 70, 90, 110, 130 mm.
- Brazo B, radios: 40, 60, 80, 100, 120, 140 mm.
- Distancia de trabajo: 50–80 mm entre la cara óptica y el plato.

<!-- TODO: secuencia de montaje, torque, fotos. -->

## 5. Posicionamiento con el gálibo

<!-- TODO: cómo se usa el gálibo para centrar y verificar la altura de los sensores. -->

## 6. Cableado del TB6600

Ver `hardware/cableado/esquema-potencia.md` y `hardware/cableado/esquema-control.md`.

Notas conocidas del brief: entradas de 24 V, cátodo común, motor NEMA 17.
Polaridad exacta de los pulsos: **PENDIENTE**.

## 7. Enseñanza de los sensores

17 sensores disponibles; 12 en uso como canales radiales, 1 como índice de home, 4 de
reserva sin montar. Cordsets M8 hembra 4 pines: 13.

<!-- TODO: procedimiento de ajuste de BGS para el fondo del plato. -->

## 8. Verificación final

- [ ] Todos los canales responden al taparlos uno por uno.
- [ ] El índice de home se activa una vez por vuelta.
- [ ] La viga no flexa apreciablemente con el motor en marcha.
- [ ] No hay interferencia óptica entre sensores vecinos a 20 mm.
- [ ] Foto del montaje completo guardada en `docs/`.
