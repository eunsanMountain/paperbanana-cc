"""Standalone CLI script for OpenAI image generation.

Usage:
    uv run python scripts/openai_image_gen.py --prompt "A neural network diagram" --output image.png
    uv run python scripts/openai_image_gen.py --prompt-file prompt.md --output image.png --ratio 3:2
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from paperbanana_cc.image_gen import generate_image  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an academic illustration using the OpenAI gpt-image-1 model.",
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", "-p", type=str, help="Prompt text for image generation.")
    prompt_group.add_argument(
        "--prompt-file", "-f", type=str, metavar="FILE",
        help="Path to a file containing the prompt.",
    )
    parser.add_argument(
        "--output", "-o", type=str, required=True, help="Output image file path (e.g. image.png)."
    )
    parser.add_argument(
        "--ratio",
        type=str,
        default="1:1",
        choices=["1:1", "3:2", "2:3"],
        help="Aspect ratio (default: 1:1). Maps to 1024x1024, 1536x1024, 1024x1536.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-image-1",
        help="OpenAI image model to use (default: gpt-image-1).",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    output_path = await generate_image(
        prompt=args.prompt or "",
        output_path=args.output,
        provider="openai",
        ratio=args.ratio,
        prompt_file=args.prompt_file,
    )

    print(str(output_path))


if __name__ == "__main__":
    asyncio.run(main())
