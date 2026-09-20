# 02 — Matemáticas

> Categoría Diátaxis: **Referencia**. Responde *cuál es el valor exacto de X*.
> **Este documento es la referencia normativa.** Python y ST deben implementar
> exactamente estas fórmulas. La paridad se verifica en `parity.yml` con tolerancia
> relativa `1e-4`.
> Fuente: `docs/00-brief.md` §5.

## 5.1 El raster polar

Cada celda del raster corresponde a una posición angular y un radio:

$$\theta_k = \frac{2\pi k}{N}, \quad k = 0,\dots,N-1$$

$$r_j \in \{30, 40, 50, \dots, 140\}\ \text{mm}, \quad j = 0,\dots,M-1$$

El raster crudo es $B_{\text{raw}}[k][j] \in \{0,1\}$.

Parámetros: $N = 100$ barridos por vuelta, $M = 12$ canales.

## 5.2 Fusión de los dos brazos

El brazo B está desfasado media vuelta. Los canales impares se corrigen:

$$B[k][j] = \begin{cases}
B_{\text{raw}}[k][j] & j \text{ par (brazo A)} \\
B_{\text{raw}}\left[\left(k + \tfrac{N}{2}\right) \bmod N\right][j] & j \text{ impar (brazo B)}
\end{cases}$$

Con $N = 100$, el desfase es exactamente 50 filas. Por eso $N$ debe ser par.

## 5.3 Peso de área en coordenadas polares

**Este es el error más fácil de cometer.** En coordenadas polares las celdas exteriores
cubren más área física que las interiores. Un conteo simple de bits sobreestima las
piezas cercanas al centro.

El área diferencial es $dA = r\, dr\, d\theta$, así que cada celda pesa proporcional
a su radio:

$$w_j = r_j$$

## 5.4 Momentos

Momentos crudos, con la corrección de área:

$$M_{00} = \sum_{k}\sum_{j} B[k][j]\, r_j$$

Convirtiendo a cartesianas, $x_{kj} = r_j\cos\theta_k$ y $y_{kj} = r_j\sin\theta_k$:

$$M_{10} = \sum_{k}\sum_{j} B[k][j]\, r_j\, x_{kj}, \qquad
M_{01} = \sum_{k}\sum_{j} B[k][j]\, r_j\, y_{kj}$$

Centroide:

$$\bar{x} = \frac{M_{10}}{M_{00}}, \qquad \bar{y} = \frac{M_{01}}{M_{00}}$$

Momentos centrales de segundo orden:

$$\mu_{20} = \sum_{k,j} B\, r_j (x_{kj}-\bar{x})^2, \quad
\mu_{02} = \sum_{k,j} B\, r_j (y_{kj}-\bar{y})^2, \quad
\mu_{11} = \sum_{k,j} B\, r_j (x_{kj}-\bar{x})(y_{kj}-\bar{y})$$

Momentos centrales de tercer orden (necesarios para $\varphi_7$ de §5.6; **no** estaban
en el brief original y se añaden aquí como parte de esta referencia normativa):

$$\mu_{30} = \sum_{k,j} B\, r_j (x_{kj}-\bar{x})^3, \qquad
\mu_{03} = \sum_{k,j} B\, r_j (y_{kj}-\bar{y})^3$$

$$\mu_{21} = \sum_{k,j} B\, r_j (x_{kj}-\bar{x})^2 (y_{kj}-\bar{y}), \qquad
\mu_{12} = \sum_{k,j} B\, r_j (x_{kj}-\bar{x})(y_{kj}-\bar{y})^2$$

Área física aproximada:

$$A \approx M_{00} \cdot \Delta r \cdot \Delta\theta$$

## 5.5 Orientación y elongación

$$\phi = \frac{1}{2}\arctan_2\left(2\mu_{11},\ \mu_{20}-\mu_{02}\right)$$

Los autovalores de la matriz de covarianza dan los semiejes:

$$\lambda_{1,2} = \frac{\mu_{20}+\mu_{02}}{2} \pm \frac{\sqrt{4\mu_{11}^2 + (\mu_{20}-\mu_{02})^2}}{2}$$

$$\text{elongación} = \sqrt{\lambda_1/\lambda_2}, \qquad
\text{excentricidad} = \sqrt{1 - \lambda_2/\lambda_1}$$

## 5.6 Invariancia — por qué importa aquí

La pieza se coloca en el plato **en cualquier posición y en cualquier ángulo**. El
origen angular del raster lo fija la marca de home, no la pieza. Por lo tanto los
features que entran al clasificador deben ser invariantes a traslación y rotación,
o el modelo aprenderá dónde pusiste la pieza en vez de qué pieza es.

Momentos centrales normalizados:

$$\eta_{pq} = \frac{\mu_{pq}}{\mu_{00}^{\,1+\frac{p+q}{2}}}$$

Los dos primeros invariantes de Hu:

$$\varphi_1 = \eta_{20} + \eta_{02}$$

$$\varphi_2 = (\eta_{20}-\eta_{02})^2 + 4\eta_{11}^2$$

$\varphi_7$, el invariante de tercer orden (normalizado con la misma $\eta_{pq}$ de
arriba, con $p+q=3$). **Fórmula estándar de Hu, añadida aquí**: el brief original la
exige en el vector de features (§5.7, componente 3) pero no la escribía, lo que hacía el
feature inimplementable.

$$\begin{aligned}
\varphi_7 ={} & (3\eta_{21} - \eta_{03})(\eta_{30} + \eta_{12})
\left[(\eta_{30}+\eta_{12})^2 - 3(\eta_{21}+\eta_{03})^2\right] \\
& + (3\eta_{12} - \eta_{30})(\eta_{21} + \eta_{03})
\left[3(\eta_{30}+\eta_{12})^2 - (\eta_{21}+\eta_{03})^2\right]
\end{aligned}$$

**Excepción deliberada:** para detectar una pieza volteada se necesita un feature que
NO sea invariante a reflexión. $\varphi_7$ de Hu cambia de signo bajo reflexión y es
exactamente eso. El signo debe conservarse: no usar $\lvert\varphi_7\rvert$. Documentarlo
como decisión de diseño.

## 5.7 Vector de features

| # | Feature | Invariante a |
| --- | --- | --- |
| 0 | $A$ — área física | traslación, rotación |
| 1 | $\varphi_1$ | traslación, rotación, escala |
| 2 | $\varphi_2$ | traslación, rotación, escala |
| 3 | $\varphi_7$ (con signo) | traslación, rotación — **no** a reflexión |
| 4 | elongación | traslación, rotación |
| 5 | $\rho_{\max} - \rho_{\min}$ — ancho del anillo ocupado | traslación no, rotación sí |
| 6 | transiciones medias por fila | traslación, rotación |
| 7 | compacidad $P^2/A$ | traslación, rotación, escala |
| 8 | fracción de filas ocupadas | traslación, rotación |
| 9 | $\lambda_1/\lambda_2$ | traslación, rotación, escala |

Diez features. La regla de ingeniería del proyecto: con un sensor barato, un buen
feature engineering le gana a un modelo grande.

<!-- TODO: fijar la definición exacta de P (perímetro) para la compacidad y de
     "transiciones medias por fila", que el brief nombra pero no formaliza. -->
**PENDIENTE:** definición formal de $P$ y del conteo de transiciones.

## 5.8 Normalización

Los parámetros se calculan sobre el set de entrenamiento y viajan con los pesos:

$$\hat{x}_i = \frac{x_i - \mu_i}{\sigma_i + \epsilon}, \qquad \epsilon = 10^{-8}$$

Si $\mu$ y $\sigma$ no se despliegan junto con los pesos, el modelo en el PLC da
basura. Van en el mismo UDT, versionados juntos.

## 5.9 Los tres modelos

**Árbol de decisión.** Se compila a IF/THEN anidados. Cero multiplicaciones,
determinista, auditable. Es el argumento de explainable AI en control.

**Regresión logística multiclase.**

$$z = W\hat{x} + b, \qquad W \in \mathbb{R}^{K \times 10}$$

**MLP 10-12-K.**

$$h = \tanh(W_1\hat{x} + b_1), \qquad z = W_2 h + b_2$$

En los tres casos la decisión es $\hat{y} = \arg\max_c z_c$.

**Nota de implementación:** softmax no se calcula en el PLC para decidir, porque es
monótona y no cambia el argmax. Solo se calcula si se necesita la probabilidad para
el reject option:

$$p_c = \frac{e^{z_c - \max_i z_i}}{\sum_i e^{z_i - \max_i z_i}}$$

La resta del máximo evita desbordamiento en `REAL`. No omitirla.

## 5.10 Reject option por conformal prediction

Sobre un set de calibración de $n$ muestras se calcula la no-conformidad:

$$s_i = 1 - p_{y_i}^{(i)}$$

El umbral es el cuantil empírico:

$$\hat{q} = \text{Cuantil}_{\lceil (n+1)(1-\alpha)\rceil / n}\left(\{s_i\}\right)$$

El conjunto de predicción es $\Gamma(x) = \{c : 1 - p_c \le \hat{q}\}$. Si
$|\Gamma(x)| \neq 1$, la pieza va a inspección manual en vez de adivinar.

Garantía: $P(y \in \Gamma(x)) \ge 1-\alpha$.

**PENDIENTE:** valor de $\alpha$ (nivel de confianza objetivo) y tamaño mínimo de $n$.

## 5.11 Costo computacional

| Modelo | Multiplicaciones | Memoria (REAL) |
| --- | --- | --- |
| Árbol, profundidad 5 | 0 | ~32 |
| Logística, K=4 | 40 | 44 |
| MLP 10-12-4 | 168 | 184 |

Más las ~1200 operaciones de los momentos sobre el raster. Todo cabe holgadamente en
una tarea periódica del NX102, y esa medición es uno de los entregables.

<!-- TODO: reemplazar "cabe holgadamente" por la medición real de ciclo cuando exista
     el código (Fase 2). Este es un entregable, no una afirmación. -->
