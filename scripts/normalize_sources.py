#!/usr/bin/env python3
"""Normaliza bloco de fontes para formato padrao claim_id/nivel/url/data."""

import json
import sys

if __name__ == "__main__":
    rows = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            rows.append({"claim_id": parts[0], "nivel": parts[1], "url": parts[2], "data": parts[3]})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
