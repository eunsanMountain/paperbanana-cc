"""Download PaperBananaBench reference data (~300MB) from HuggingFace."""

import json
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

try:
    from rich.console import Console
    from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn, TransferSpeedColumn
except ImportError:
    print("Error: rich package not installed. Run: uv pip install rich")
    sys.exit(1)

DATASET_URL = (
    "https://huggingface.co/datasets/dwzhu/PaperBananaBench"
    "/resolve/main/PaperBananaBench.zip"
)

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data" / "references"

console = Console()


def _already_exists() -> bool:
    """Return True if both diagram and plot data exist."""
    for split in ("diagram", "plot"):
        ref_json = DATA_DIR / split / "ref.json"
        images_dir = DATA_DIR / split / "images"
        if not ref_json.exists():
            return False
        if not images_dir.exists() or not any(images_dir.iterdir()):
            return False
    return True


def _download_with_progress(url: str, dest: Path) -> None:
    """Download url to dest, showing a rich progress bar."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    with Progress(
        TextColumn("[bold blue]Downloading"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        console=console,
    ) as progress:
        response = urllib.request.urlopen(url)  # noqa: S310
        total = int(response.headers.get("Content-Length", 0))
        task = progress.add_task("downloading", total=total or None)

        with dest.open("wb") as f:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                f.write(chunk)
                progress.update(task, advance=len(chunk))


def _find_bench_dir(tmp_dir: Path) -> Path:
    """Find PaperBananaBench directory inside extracted archive."""
    candidate = tmp_dir / "PaperBananaBench"
    if candidate.exists():
        return candidate
    # Sometimes nested one level deeper
    candidates = list(tmp_dir.glob("*/PaperBananaBench"))
    if candidates:
        return candidates[0]
    raise RuntimeError("Could not find PaperBananaBench directory in extracted archive.")


def _install_split(bench_dir: Path, split: str) -> int:
    """Move one split (diagram/plot) from extracted archive to data/references/."""
    src = bench_dir / split
    if not src.exists():
        console.print(f"[yellow]Warning[/yellow]: {split}/ not found in archive, skipping")
        return 0

    dest = DATA_DIR / split
    dest.mkdir(parents=True, exist_ok=True)

    # Copy ref.json
    src_ref = src / "ref.json"
    if src_ref.exists():
        shutil.copy2(src_ref, dest / "ref.json")

    # Copy images directory
    src_images = src / "images"
    dest_images = dest / "images"
    if src_images.exists():
        if dest_images.exists():
            shutil.rmtree(dest_images)
        shutil.copytree(src_images, dest_images)

    # Count entries
    ref_json = dest / "ref.json"
    if ref_json.exists():
        data = json.loads(ref_json.read_text())
        count = len(data) if isinstance(data, list) else len(data.get("examples", []))
        image_count = sum(1 for _ in dest_images.iterdir()) if dest_images.exists() else 0
        console.print(
            f"  [green]{split}[/green]: {count} entries, {image_count} images"
        )
        return count
    return 0


def main() -> None:
    console.print("[bold]PaperBanana CC — Reference Data Downloader[/bold]")
    console.print(f"Source: {DATASET_URL}")
    console.print(f"Target: {DATA_DIR}\n")

    if _already_exists():
        console.print("[yellow]Data already exists. Use --force to re-download.[/yellow]")
        if "--force" not in sys.argv:
            return

    with tempfile.TemporaryDirectory(prefix="paperbanana_") as tmp:
        tmp_dir = Path(tmp)
        zip_path = tmp_dir / "PaperBananaBench.zip"

        # Download
        try:
            _download_with_progress(DATASET_URL, zip_path)
        except urllib.error.URLError as e:
            console.print(f"[bold red]Download failed[/bold red]: {e}")
            sys.exit(1)

        # Extract
        console.print("[bold green]Extracting...[/bold green]")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)

        # Find and install
        bench_dir = _find_bench_dir(tmp_dir)
        console.print("[bold green]Installing reference data...[/bold green]")
        diagram_count = _install_split(bench_dir, "diagram")
        plot_count = _install_split(bench_dir, "plot")

    console.print(
        f"\n[bold green]Done.[/bold green] "
        f"{diagram_count + plot_count} total references installed."
    )


if __name__ == "__main__":
    main()
