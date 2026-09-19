(*
  POU_Sombra — Modo sombra y conmutación de banco de pesos
  ----------------------------------------------------------------------------
  Responsabilidad : ejecutar el modelo nuevo en paralelo sin actuar, comparar su
                    predicción con la del modelo activo, contar coincidencias y
                    habilitar la conmutación de banco cuando se cumple el umbral.
  Fórmulas        : ninguna propia. Usa la salida de POU_Inferencia.
  Entradas        : resultado del modelo activo, resultado del modelo en sombra,
                    Model.ShadowThreshold.
  Salidas         : Model.WeightBank, Model.ShadowAgree, Model.ShadowCount.
  Tiempo peor caso: PENDIENTE (suma del peor caso de dos inferencias).
  Nota            : el umbral N de piezas en sombra está PENDIENTE.
  ----------------------------------------------------------------------------
*)

(* TODO: Fase 4 — implementar. No escribir lógica en el andamiaje. *)
