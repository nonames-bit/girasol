"""Interfaz de línea de comandos de Girasol.

Los comandos definitivos están PENDIENTES; esta es la superficie prevista:
``features``, ``train``, ``export`` y ``parity``.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Construir el parser de argumentos.

    Returns
    -------
    argparse.ArgumentParser
        Parser con los subcomandos previstos.
    """
    parser = argparse.ArgumentParser(prog="girasol", description="Herramientas de Girasol")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("features", help="Calcular features desde un raster (PENDIENTE).")
    subparsers.add_parser("train", help="Entrenar un modelo (PENDIENTE).")
    subparsers.add_parser("export", help="Exportar pesos a JSON y ST (PENDIENTE).")
    subparsers.add_parser("parity", help="Verificar paridad ST/Python (PENDIENTE).")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada de la CLI.

    Parameters
    ----------
    argv : sequence of str, optional
        Argumentos; por defecto, los de ``sys.argv``.

    Returns
    -------
    int
        Código de salida.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    raise NotImplementedError(f"Fase 2: implementar el subcomando '{args.command}'.")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
