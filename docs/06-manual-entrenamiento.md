# 06 — Manual de entrenamiento

> Categoría Diátaxis: **How-to**. Responde *cómo hago una tarea concreta*.
> Del dataset a los pesos desplegados, con los comandos exactos.
> Fuente: `docs/00-brief.md` §4.4, §5 y §10.2.

## Índice

1. Preparar el entorno
2. Capturar el dataset
3. Calcular features
4. Entrenar
5. Validar
6. Exportar pesos
7. Desplegar por OPC UA
8. Modo sombra y conmutación

## 1. Preparar el entorno

```bash
cd ml
python -m venv .venv
# activar el entorno
pip install -e ".[dev]"
```

<!-- TODO: fijar versión de Python y dependencias exactas en ml/pyproject.toml. -->

## 2. Capturar el dataset

<!-- TODO: comando del colector edge → Parquet. Los datos viven fuera del repositorio:
     solo su esquema y checksum entran (ver data/README.md). -->

## 3. Calcular features

```bash
# PENDIENTE: nombre final del comando de la CLI
python -m girasol.cli features --config configs/girasol.yaml ...
```

<!-- TODO: completar con los flags reales de ml/src/girasol/cli.py. -->

## 4. Entrenar

Tres modelos según el brief §5.9: árbol de decisión, regresión logística multiclase
y MLP 10-12-K.

```bash
# PENDIENTE: comando de entrenamiento
```

## 5. Validar

- Holdout estratificado.
- Vectores dorados y paridad ST/Python (tolerancia relativa `1e-4`).
- Calibración conformal para el reject option ($\hat{q}$ y $\alpha$).

## 6. Exportar pesos

```bash
# PENDIENTE: export.py → JSON y constantes ST
```

Los pesos viajan **junto con** $\mu$ y $\sigma$ en el mismo UDT. Ver
`docs/03-contrato-datos.md`.

## 7. Desplegar por OPC UA

<!-- TODO: lista de tags de escritura y procedimiento de escritura atómica del banco A/B. -->

## 8. Modo sombra y conmutación

<!-- TODO: número N de piezas en sombra antes de conmutar. Valor PENDIENTE. -->
