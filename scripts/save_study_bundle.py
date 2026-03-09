#!/usr/bin/env python3
"""Cria estrutura padrao de persistencia para estudos do AgenteAprendedor."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


FILES = [
    "00-contexto.md",
    "01-matriz-afirmacoes.csv",
    "02-fontes.json",
    "03-controversias.md",
    "04-ausencias-alertas.md",
    "05-mapa-conhecimento.md",
    "06-manual-operacional.md",
    "07-pacote-especialista.md",
    "08-monitoramento.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic-slug", required=True, help="Slug do tema do estudo")
    parser.add_argument(
        "--base-dir",
        default="reports/aprendizados",
        help="Diretorio base de persistencia (padrao: reports/aprendizados)",
    )
    parser.add_argument(
        "--agent-name",
        default="agente-aprendedor",
        help="Nome do agente/modelo para index.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(args.base_dir) / date_str / args.topic_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    for fname in FILES:
        path = out_dir / fname
        if not path.exists():
            path.write_text("", encoding="utf-8")

    index = {
        "topic": args.topic_slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_or_agent": args.agent_name,
        "method_version": "7.0",
        "certainty_summary": {
            "verdade_absoluta": 0,
            "verdade_provavel_forte": 0,
            "verdade_provavel_fraca": 0,
            "verdade_popular_sem_validacao": 0,
            "indeterminado": 0,
        },
        "files": FILES,
    }
    (out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(str(out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
