"""Matplotlib code execution module with subprocess isolation and timeout."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def execute_plot_code(code: str, output_path: str, timeout: int = 30) -> Path:
    """Execute matplotlib Python code and save the resulting plot.

    The code is expected to save a figure to the path bound to the
    ``OUTPUT_PATH`` variable, which is injected automatically before execution.

    Args:
        code: Python source code that produces a matplotlib figure.
        output_path: Destination path for the generated plot image.
        timeout: Maximum execution time in seconds (default 30).

    Returns:
        Path to the saved plot image.

    Raises:
        RuntimeError: If the subprocess exits with a non-zero return code.
        TimeoutError: If execution exceeds the timeout.
        FileNotFoundError: If the output file was not created after execution.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Inject OUTPUT_PATH so that generated code can reference it
    injected_code = f'OUTPUT_PATH = "{out.as_posix()}"\n{code}'

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(injected_code)
        temp_path = Path(f.name)

    try:
        result = subprocess.run(
            [sys.executable, str(temp_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        temp_path.unlink(missing_ok=True)
        raise TimeoutError(
            f"Plot code execution timed out after {timeout}s."
        ) from exc
    finally:
        temp_path.unlink(missing_ok=True)

    if result.returncode != 0:
        stderr_excerpt = result.stderr[:1000] if result.stderr else "(no stderr)"
        raise RuntimeError(
            f"Plot code exited with code {result.returncode}.\n"
            f"stderr:\n{stderr_excerpt}"
        )

    if not out.exists():
        raise FileNotFoundError(
            f"Plot code executed successfully but output file was not created: {out}"
        )

    return out
