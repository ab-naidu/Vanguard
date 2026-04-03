#!/usr/bin/env python3
"""CLI: images + note -> structured work order JSON (Gemma multimodal)."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Repo root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vanguard.mock_data import MOCK_WORK_ORDER_RESULT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    p = argparse.ArgumentParser(description="Vanguard: photos + note -> JSON")
    p.add_argument("--images", nargs="*", default=[], help="Image paths (0+)")
    p.add_argument("--note", default="", help="Technician note")
    p.add_argument(
        "--model",
        default=os.environ.get("VANGUARD_MODEL_ID", "google/gemma-3-4b-it"),
        help="HF model id (default: env VANGUARD_MODEL_ID or gemma-3-4b-it)",
    )
    p.add_argument("--output", "-o", help="Write JSON to this path")
    p.add_argument("--mock", action="store_true", help="Skip model; write mock JSON")
    p.add_argument("--max-new-tokens", type=int, default=2048)
    args = p.parse_args()

    if args.mock:
        data = MOCK_WORK_ORDER_RESULT
        raw = json.dumps(MOCK_WORK_ORDER_RESULT)
        logger.info("Mock mode: no inference.")
    else:
        from PIL import Image

        from vanguard.pipeline import generate_work_order_json, load_processor_and_model

        images: list[Image.Image] = []
        for path in args.images:
            images.append(Image.open(path).convert("RGB"))
        logger.info("Loading model %s …", args.model)
        processor, model = load_processor_and_model(args.model)
        data, raw = generate_work_order_json(
            processor,
            model,
            images,
            args.note,
            max_new_tokens=args.max_new_tokens,
        )

    text = json.dumps(data, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        logger.info("Wrote %s", args.output)


if __name__ == "__main__":
    main()
