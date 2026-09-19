(*
  POU_Features — Descriptores geométricos
  ----------------------------------------------------------------------------
  Responsabilidad : calcular el vector de 10 features a partir del raster fusionado,
                    con corrección de área polar y momentos de imagen a mano.
  Fórmulas        : (* Ver docs/02-matematicas.md secciones 5.3 a 5.7 *)
                    w_j = r_j                                   (§5.3)
                    M00, M10, M01, centroide x̄ ȳ             (§5.4)
                    μ20, μ02, μ11, A                            (§5.4)
                    φ (orientación), λ1 λ2, elongación          (§5.5)
                    η_pq, φ1, φ2, φ7                            (§5.6)
                    vector de 10 features                       (§5.7)
  Entradas        : aRasterFused, constantes geométricas (radios, Δθ).
  Salidas         : aFeatures (ARRAY[0..9] OF REAL), bFeaturesValid.
  Tiempo peor caso: PENDIENTE. Cota: ~1200 operaciones sobre 1200 celdas.
  Cuidados        : división por M00 ≈ 0 → marcar bFeaturesValid = FALSE,
                    no devolver NaN ni infinito.
  ----------------------------------------------------------------------------
*)

(* TODO: Fase 2 — implementar desde la especificación, sin leer el Python. *)
