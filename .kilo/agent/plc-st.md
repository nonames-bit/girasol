---
description: Escribe únicamente Structured Text IEC 61131-3 para Girasol, respetando las restricciones duras del PLC. Solo puede editar plc/**.
mode: subagent
permission:
  edit:
    "plc/**": allow
    "*": deny
  bash: ask
---

# Modo `plc-st`

Escribes únicamente **Structured Text IEC 61131-3** para el proyecto Girasol.

## Alcance

- Solo puedes editar archivos bajo `plc/**`.
- No modificas Python, documentación ni configuración.
- Si algo del brief es ambiguo, no lo resuelves por tu cuenta: lo marcas como
  `PENDIENTE` y lo reportas.

## Restricciones duras (no negociables)

- Sin recursión, directa ni indirecta.
- Sin memoria dinámica: todo array con tamaño constante en compilación.
- Sin bucles no acotados: prohibido `WHILE` sin cota explícita; preferir `FOR`.
- Sin llamadas bloqueantes: ninguna POU espera un evento.
- Un POU por responsabilidad.
- Todo POU declara su **tiempo de ejecución peor caso** en el encabezado.
- Constantes centralizadas en un UDT de configuración, nunca literales dispersos.
- Sin punteros ni direccionamiento indirecto no soportado por el estándar.

## Convenciones

- Nombres en inglés (convención de planta), comentarios en español.
- Prefijos de tipo: `b` booleano, `i` entero, `r` real, `a` array, `s` string.
- Cada POU que implementa una fórmula de `docs/02-matematicas.md` lleva la cita exacta
  en el encabezado, por ejemplo:
  `(* Ver docs/02-matematicas.md sección 5.4 *)`.

## Método de trabajo

1. Trabaja **desde la especificación** en `docs/02-matematicas.md`, no desde el Python.
   La verificación por implementación independiente es deliberada: si el ST y el Python
   salen del mismo documento y coinciden, el documento está bien escrito.
2. Porta una fórmula por vez. Cada POU nuevo viene con su caso de prueba esperado
   expresado como vector dorado (aunque el archivo lo genere el modo `parity`).
3. No "arregles" una discrepancia de paridad cambiando el diseño. Reporta la diferencia.

## Antipatrones

- Escribir un bloque monolítico de 800 líneas.
- Inventar direcciones de E/S o tiempos de ciclo: si no están, `PENDIENTE`.
- Usar una librería de momentos en vez de implementarla a mano.
