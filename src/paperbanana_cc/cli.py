"""PaperBanana CC — unified CLI for uvx execution.

Usage:
    uvx paperbanana-cc generate --prompt "..." --output image.png
    uvx paperbanana-cc download --target ./data/references
    uvx paperbanana-cc filter-refs --type diagram --keywords "attention,transformer" --ref-json ref.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path


def _cmd_generate(args: argparse.Namespace) -> None:
    """Generate an image using OpenAI or Gemini API."""
    from paperbanana_cc.image_gen import generate_image

    asyncio.run(
        generate_image(
            prompt=args.prompt or "",
            output_path=args.output,
            provider=args.provider,
            ratio=args.ratio,
            prompt_file=args.prompt_file,
        )
    )
    print(args.output)


def _cmd_download(args: argparse.Namespace) -> None:
    """Download reference data from HuggingFace."""
    import shutil
    import tempfile
    import urllib.request
    import zipfile

    dataset_url = (
        "https://huggingface.co/datasets/dwzhu/PaperBananaBench"
        "/resolve/main/PaperBananaBench.zip"
    )
    target = Path(args.target)

    # Check if already exists
    if not args.force:
        exists = all(
            (target / split / "ref.json").exists()
            and (target / split / "images").exists()
            for split in ("diagram", "plot")
        )
        if exists:
            print("Reference data already exists. Use --force to re-download.")
            return

    with tempfile.TemporaryDirectory(prefix="paperbanana_") as tmp:
        tmp_dir = Path(tmp)
        zip_path = tmp_dir / "PaperBananaBench.zip"

        # Download
        print(f"Downloading from {dataset_url} ...")
        urllib.request.urlretrieve(dataset_url, str(zip_path))  # noqa: S310

        # Extract
        print("Extracting...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)

        # Find PaperBananaBench directory
        bench_dir = tmp_dir / "PaperBananaBench"
        if not bench_dir.exists():
            candidates = list(tmp_dir.glob("*/PaperBananaBench"))
            if candidates:
                bench_dir = candidates[0]
            else:
                print("Error: Could not find PaperBananaBench directory in archive.")
                sys.exit(1)

        # Install splits
        for split in ("diagram", "plot"):
            src = bench_dir / split
            if not src.exists():
                print(f"Warning: {split}/ not found in archive, skipping")
                continue

            dest = target / split
            dest.mkdir(parents=True, exist_ok=True)

            src_ref = src / "ref.json"
            if src_ref.exists():
                shutil.copy2(src_ref, dest / "ref.json")

            src_images = src / "images"
            dest_images = dest / "images"
            if src_images.exists():
                if dest_images.exists():
                    shutil.rmtree(dest_images)
                shutil.copytree(src_images, dest_images)

            # Count
            ref_json = dest / "ref.json"
            if ref_json.exists():
                data = json.loads(ref_json.read_text())
                count = len(data) if isinstance(data, list) else 0
                img_count = sum(1 for _ in dest_images.iterdir()) if dest_images.exists() else 0
                print(f"  {split}: {count} entries, {img_count} images")

    print("Done.")


def _cmd_filter_refs(args: argparse.Namespace) -> None:
    """Pre-filter reference data by keywords."""
    ref_path = Path(args.ref_json)
    if not ref_path.exists():
        print(f"Error: {ref_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(ref_path) as f:
        data = json.load(f)

    keywords = [k.strip().lower() for k in args.keywords.split(",") if k.strip()]
    limit = args.limit

    results = []
    for r in data:
        text = " ".join(
            str(r.get(k, "")) for k in ("content", "visual_intent", "category", "caption")
        ).lower()
        score = sum(1 for k in keywords if k in text)
        if score >= 1:
            results.append(r)

    results = results[:limit]
    print(json.dumps(results, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="paperbanana-cc",
        description="PaperBanana CC — academic illustration CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- generate ---
    gen = sub.add_parser("generate", help="Generate an image via OpenAI or Gemini API")
    prompt_group = gen.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", "-p", type=str, help="Prompt text")
    prompt_group.add_argument("--prompt-file", "-f", type=str, help="Path to prompt file")
    gen.add_argument("--output", "-o", type=str, required=True, help="Output image path")
    gen.add_argument(
        "--provider", type=str, default="openai", choices=["openai", "gemini"],
        help="Image generation provider (default: openai)",
    )
    gen.add_argument("--ratio", type=str, default="1:1", help="Aspect ratio (default: 1:1)")

    # --- download ---
    dl = sub.add_parser("download", help="Download reference data from HuggingFace")
    dl.add_argument("--target", "-t", type=str, required=True, help="Target directory")
    dl.add_argument("--force", action="store_true", help="Force re-download")

    # --- filter-refs ---
    fr = sub.add_parser("filter-refs", help="Pre-filter references by keywords")
    fr.add_argument("--ref-json", type=str, required=True, help="Path to ref.json")
    fr.add_argument("--keywords", "-k", type=str, required=True, help="Comma-separated keywords")
    fr.add_argument("--limit", type=int, default=100, help="Max results (default: 100)")

    args = parser.parse_args()

    if args.command == "generate":
        _cmd_generate(args)
    elif args.command == "download":
        _cmd_download(args)
    elif args.command == "filter-refs":
        _cmd_filter_refs(args)


if __name__ == "__main__":
    main()
