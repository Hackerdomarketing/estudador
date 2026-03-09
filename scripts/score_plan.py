#!/usr/bin/env python3
"""Score simples para plano de social media baseado em rubricas textuais."""

import json
import re
import sys
from pathlib import Path

KEYS = [
    r"21\s*dias|3\s*semanas",
    r"kpi|meta|threshold",
    r"organic|colab|collab|comunidades|paid",
    r"risco|limit|limita",
    r"experimento|itera|teste",
]


def score(text: str) -> int:
    s = 0
    low = text.lower()
    for pat in KEYS:
        if re.search(pat, low):
            s += 1
    return s


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: score_plan.py <arquivo-output.md>")
        sys.exit(1)
    p = Path(sys.argv[1])
    txt = p.read_text(encoding="utf-8")
    val = score(txt)
    print(json.dumps({"score_0_5": val, "max": 5}, ensure_ascii=False))
