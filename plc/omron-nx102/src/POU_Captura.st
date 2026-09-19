(*
  POU_Captura — Captura sincrónica del raster
  ----------------------------------------------------------------------------
  Responsabilidad : generar los pulsos del motor, contar micropasos, detectar el
                    índice de home y almacenar cada barrido en el raster.
  Entradas        : señales de los 12 canales, señal HOME.
  Salidas         : aRaster (ARRAY[0..99,0..11] OF BOOL), iScanIndex, estado.
  Fórmulas        : ninguna. Los parámetros de movimiento son de docs/00-brief.md §3.
  Tiempo peor caso: PENDIENTE (medir en Fase 1; es un entregable del proyecto).
  Restricciones   : sin recursión, sin memoria dinámica, sin bucles no acotados.
  ----------------------------------------------------------------------------
*)

(* TODO: Fase 1 — implementar. No escribir lógica en el andamiaje. *)
