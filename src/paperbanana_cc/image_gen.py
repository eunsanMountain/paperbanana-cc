"""Unified image generation module supporting OpenAI and Gemini providers."""

from __future__ import annotations

import base64
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TEXT_GARBLING_PREVENTION = (
    "CRITICAL: All text labels must be rendered in clear, readable English."
)

# OpenAI size mapping
_OPENAI_SIZE_MAP: dict[str, str] = {
    "1:1": "1024x1024",
    "3:2": "1536x1024",
    "2:3": "1024x1536",
}

# Gemini supported ratios
_GEMINI_RATIOS: set[str] = {
    "1:1",
    "3:4",
    "4:3",
    "9:16",
    "16:9",
    "3:2",
    "2:3",
    "21:9",
}


def _build_prompt(prompt: str) -> str:
    """Append text garbling prevention instruction to prompt."""
    return f"{prompt}\n\n{TEXT_GARBLING_PREVENTION}"


async def generate_image(
    prompt: str,
    output_path: str,
    provider: str = "openai",
    ratio: str = "1:1",
    prompt_file: str | None = None,
) -> Path:
    """Generate an image from a prompt and save it to output_path.

    Args:
        prompt: Text prompt describing the image to generate.
        output_path: Destination file path for the generated image.
        provider: Image generation provider — "openai" or "gemini".
        ratio: Aspect ratio string (e.g. "1:1", "3:2", "2:3").
        prompt_file: Optional path to a file containing the prompt (overrides prompt).

    Returns:
        Path to the saved image file.
    """
    if prompt_file is not None:
        prompt = Path(prompt_file).read_text(encoding="utf-8")

    full_prompt = _build_prompt(prompt)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if provider == "openai":
        return await _generate_openai(full_prompt, out, ratio)
    elif provider == "gemini":
        return await _generate_gemini(full_prompt, out, ratio)
    else:
        raise ValueError(f"Unknown provider: {provider!r}. Choose 'openai' or 'gemini'.")


async def _generate_openai(prompt: str, output_path: Path, ratio: str) -> Path:
    """Generate an image using the OpenAI gpt-image-1 model."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file or environment."
        )

    size = _OPENAI_SIZE_MAP.get(ratio)
    if size is None:
        supported = ", ".join(sorted(_OPENAI_SIZE_MAP.keys()))
        raise ValueError(
            f"OpenAI provider does not support ratio {ratio!r}. "
            f"Supported ratios: {supported}"
        )

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    response = await client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,  # type: ignore[arg-type]
        n=1,
    )

    image_data = response.data[0]

    # gpt-image-1 returns b64_json
    if image_data.b64_json:
        image_bytes = base64.b64decode(image_data.b64_json)
        output_path.write_bytes(image_bytes)
    elif image_data.url:
        import urllib.request

        urllib.request.urlretrieve(image_data.url, str(output_path))  # noqa: S310
    else:
        raise RuntimeError("OpenAI response contained neither b64_json nor url.")

    return output_path


async def _generate_gemini(prompt: str, output_path: Path, ratio: str) -> Path:
    """Generate an image using Google Imagen 3 via the Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. Add it to your .env file or environment."
        )

    if ratio not in _GEMINI_RATIOS:
        supported = ", ".join(sorted(_GEMINI_RATIOS))
        raise ValueError(
            f"Gemini provider does not support ratio {ratio!r}. "
            f"Supported ratios: {supported}"
        )

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    response = await client.aio.models.generate_images(
        model="imagen-3.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=ratio,
        ),
    )

    image_bytes = response.generated_images[0].image.image_bytes
    output_path.write_bytes(image_bytes)
    return output_path
