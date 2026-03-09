#!/usr/bin/env python3
"""Agrega notas por criterio para simulacao de chance de sucesso."""

import json
import sys


def classify(total: int) -> str:
    if total >= 40:
        return "alta"
    if total >= 28:
        return "media"
    return "baixa"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: simulate_output_score.py <nota1> <nota2> ...")
        sys.exit(1)
    vals = [int(x) for x in sys.argv[1:]]
    total = sum(vals)
    print(json.dumps({"total": total, "chance_sucesso": classify(total)}, ensure_ascii=False))
