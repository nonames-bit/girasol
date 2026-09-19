(*
  POU_Inferencia — Inferencia de ML dentro del PLC
  ----------------------------------------------------------------------------
  Responsabilidad : normalizar el vector de features, evaluar el modelo activo
                    (árbol, logística o MLP) y calcular argmax y confianza.
  Fórmulas        : (* Ver docs/02-matematicas.md secciones 5.8 a 5.10 *)
                    x̂_i = (x_i − μ_i) / (σ_i + ε)               (§5.8)
                    z = Wx̂ + b                                  (§5.9)
                    h = tanh(W1x̂ + b1), z = W2h + b2            (§5.9)
                    p_c = softmax estabilizado (resta del máximo) (§5.9)
                    argmax_c z_c → clase                        (§5.9)
  Entradas        : aFeatures, UDT de pesos versionado.
  Salidas         : iClass, rConfidence, bReject, aPredictionSet.
  Tiempo peor caso: PENDIENTE. Cota por modelo en docs/02-matematicas.md §5.11.
  Cuidados        : no omitir la resta del máximo en softmax (desborde de REAL).
  ----------------------------------------------------------------------------
*)

(* TODO: Fase 2 — implementar desde la especificación, sin leer el Python. *)
