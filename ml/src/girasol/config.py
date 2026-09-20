"""Carga de la configuración del proyecto.

Fuente única de los parámetros geométricos y de captura: el código no define
constantes propias, las lee de ``ml/configs/girasol.yaml``. Regla del brief §7:
"sin números mágicos: todo parámetro geométrico o de captura vive en configs/".
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import yaml

CONFIG_PATH: Path = Path(__file__).resolve().parents[2] / "configs" / "girasol.yaml"


@dataclass(frozen=True, slots=True)
class GirasolConfig:
    """Parámetros de captura, geometría del array y normalización.

    Attributes
    ----------
    n_scans : int
        Barridos por vuelta (N).
    m_channels : int
        Canales radiales (M).
    radii_mm : tuple of float
        Radio de cada canal, de radio menor (0) a radio mayor (M-1).
    arm_offset_scans : int
        Desfase del brazo B, en barridos (N/2).
    microsteps_per_rev : int
        Micropasos por vuelta del motor (S).
    microsteps_per_scan : int
        Micropasos entre barridos (s).
    pulse_period_ms : float
        Período del pulso de paso, en ms (Tp).
    revolution_time_s : float
        Duración de una vuelta, en s (Trev).
    angular_resolution_deg : float
        Resolución angular, en grados.
    n_features : int
        Longitud del vector de features.
    delta_r_mm : float
        Paso radial entre canales contiguos, en mm.
    epsilon : float
        Término de estabilidad de la normalización (docs/02-matematicas.md §5.8).
    relative_tolerance : float
        Tolerancia relativa del test de paridad ST/Python (docs/00-brief.md §8.6).
    """

    n_scans: int
    m_channels: int
    radii_mm: tuple[float, ...]
    arm_offset_scans: int
    microsteps_per_rev: int
    microsteps_per_scan: int
    pulse_period_ms: float
    revolution_time_s: float
    angular_resolution_deg: float
    n_features: int
    delta_r_mm: float
    epsilon: float
    relative_tolerance: float


def _section(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ValueError(f"Falta la sección '{name}' en la configuración de Girasol.")
    return cast("dict[str, Any]", value)


def _as_float(value: Any, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"El parámetro '{where}' debe ser numérico en girasol.yaml.")
    return float(value)


def _as_int(value: Any, where: str) -> int:
    return int(_as_float(value, where))


def _radius_list(section: dict[str, Any]) -> tuple[float, ...]:
    radii = section.get("radii_mm")
    if not isinstance(radii, list) or not radii:
        raise ValueError("El parámetro 'raster.radii_mm' debe ser una lista no vacía.")
    values = cast("list[Any]", radii)
    return tuple(_as_float(item, "raster.radii_mm") for item in values)


def load_config(path: Path | None = None) -> GirasolConfig:
    """Cargar la configuración desde el YAML.

    Parameters
    ----------
    path : Path, optional
        Ruta alternativa al YAML. Por defecto, ``ml/configs/girasol.yaml``.

    Returns
    -------
    GirasolConfig
        Configuración validada.

    Raises
    ------
    ValueError
        Si el archivo no es un mapeo válido o falta un parámetro numérico.
    """
    source = CONFIG_PATH if path is None else path
    raw: Any = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"La configuración '{source}' no es un mapeo YAML.")

    raster = _section(raw, "raster")
    motion = _section(raw, "motion")
    features = _section(raw, "features")
    normalization = _section(raw, "normalization")
    parity = _section(raw, "parity")

    return GirasolConfig(
        n_scans=_as_int(raster.get("n_scans"), "raster.n_scans"),
        m_channels=_as_int(raster.get("m_channels"), "raster.m_channels"),
        radii_mm=_radius_list(raster),
        arm_offset_scans=_as_int(raster.get("arm_offset_scans"), "raster.arm_offset_scans"),
        microsteps_per_rev=_as_int(motion.get("microsteps_per_rev"), "motion.microsteps_per_rev"),
        microsteps_per_scan=_as_int(
            motion.get("microsteps_per_scan"), "motion.microsteps_per_scan"
        ),
        pulse_period_ms=_as_float(motion.get("pulse_period_ms"), "motion.pulse_period_ms"),
        revolution_time_s=_as_float(motion.get("revolution_time_s"), "motion.revolution_time_s"),
        angular_resolution_deg=_as_float(
            motion.get("angular_resolution_deg"), "motion.angular_resolution_deg"
        ),
        n_features=_as_int(features.get("n_features"), "features.n_features"),
        delta_r_mm=_as_float(features.get("delta_r_mm"), "features.delta_r_mm"),
        epsilon=_as_float(normalization.get("epsilon"), "normalization.epsilon"),
        relative_tolerance=_as_float(parity.get("relative_tolerance"), "parity.relative_tolerance"),
    )
