(*
  POU_Fusion — Fusión de los brazos A y B
  ----------------------------------------------------------------------------
  Responsabilidad : corregir el desfase de media vuelta de los canales impares
                    (brazo B) y producir el raster fusionado.
  Fórmula         : (* Ver docs/02-matematicas.md sección 5.2 *)
                    B[k][j] = B_raw[k][j]                 si j es par (brazo A)
                    B[k][j] = B_raw[(k + N/2) mod N][j]   si j es impar (brazo B)
  Entradas        : aRasterRaw, N_SCANS, HALF_REV_SCANS.
  Salidas         : aRasterFused.
  Tiempo peor caso: PENDIENTE. Cota: N × M = 1200 iteraciones de bucle acotado.
  ----------------------------------------------------------------------------
*)

(* TODO: Fase 2 — implementar desde la especificación, sin leer el Python. *)
