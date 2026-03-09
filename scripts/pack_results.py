#!/usr/bin/env python3
"""Empacota resultados de benchmark local em um json unico."""

import json
import sys
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: pack_results.py <diretorio>")
        sys.exit(1)
    d = Path(sys.argv[1])
    out = {"files": []}
    for f in sorted(d.glob("*.json")):
        out["files"].append({"name": f.name, "content": json.loads(f.read_text(encoding="utf-8"))})
    print(json.dumps(out, ensure_ascii=False, indent=2))
