#!/usr/bin/env python3
"""
Nano Banana - AI Image Generation using Google Gemini

Supports both Pro (high quality) and Flash (fast/cheap) models.

Usage:
    python generate.py "a cute robot" -o robot.png
    python generate.py "make it blue" -i input.jpg -o output.png
    python generate.py "landscape" --ratio 16:9 --size 4K -o landscape.png
    python generate.py "quick sketch" --model flash -o sketch.png
    python generate.py "combine styles" -i ref1.png ref2.png -o combined.png
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///

import argparse
import base64
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Run this script with: uv run generate.py <args>")
    print("Or install manually: pip install google-genai")
    sys.exit(1)

MODEL_PRO = "gemini-3-pro-image-preview"
MODEL_FLASH = "gemini-2.5-flash-image"
VALID_MODELS = {"pro": MODEL_PRO, "flash": MODEL_FLASH}

# Backward compatibility alias
MODEL_NAME = MODEL_PRO

VALID_ASPECT_RATIOS = [
    "1:1", "2:3", "3:2", "3:4", "4:3",
    "4:5", "5:4", "9:16", "16:9", "21:9"
]

VALID_SIZES = ["1K", "2K", "4K"]


def get_api_key() -> str:
    """Get Gemini API key from environment.

    Raises:
        ValueError: If GEMINI_API_KEY is not set.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set. "
            "Get your API key from: https://aistudio.google.com/apikey"
        )
    return api_key


def load_image_bytes(path: str) -> tuple[bytes, str]:
    """Load image file and return raw bytes and mime type."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    ext = path.suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }

    mime_type = mime_types.get(ext, "image/jpeg")

    with open(path, "rb") as f:
        data = f.read()

    return data, mime_type


def load_image_as_base64(path: str) -> tuple[str, str]:
    """Load image file and return base64 data and mime type.

    Deprecated: Use load_image_bytes() instead.
    """
    data, mime_type = load_image_bytes(path)
    return base64.standard_b64encode(data).decode("utf-8"), mime_type


def generate_output_path(output_dir: str = None) -> str:
    """Generate a unique output filename."""
    if output_dir is None:
        output_dir = os.environ.get("IMAGE_OUTPUT_DIR", os.path.join(Path.home(), "Downloads"))

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(Path(output_dir) / f"nanobanana_{timestamp}.png")


def _resolve_model(model: str) -> str:
    """Resolve model shorthand to full model ID."""
    if model in VALID_MODELS:
        return VALID_MODELS[model]
    # Allow passing full model ID directly
    return model


def _retry_with_backoff(fn, max_retries: int = 3, base_delay: float = 2.0):
    """Call fn() with exponential backoff on rate limit errors."""
    last_error = None
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()
            is_retryable = (
                "quota" in error_msg
                or "rate" in error_msg
                or "429" in error_msg
                or "resource_exhausted" in error_msg
            )
            if is_retryable and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                raise
    raise last_error


def generate_image(
    prompt: str,
    output_path: str = None,
    input_path: str = None,
    input_paths: list[str] = None,
    aspect_ratio: str = None,
    image_size: str = None,
    use_search: bool = False,
    model: str = "pro",
    max_retries: int = 3,
    verbose: bool = False,
) -> dict:
    """
    Generate or edit an image using Gemini API.

    Args:
        prompt: Text description or editing instruction
        output_path: Where to save the generated image
        input_path: Single input image for editing (backward compat)
        input_paths: List of input images for multi-reference editing
        aspect_ratio: Aspect ratio (1:1, 16:9, etc.)
        image_size: Resolution (1K, 2K, or 4K)
        use_search: Enable Google Search grounding
        model: Model shorthand ("pro", "flash") or full model ID
        max_retries: Max retries on rate limit errors (default 3)
        verbose: Print detailed output

    Returns:
        dict with 'success', 'path', 'error', 'metadata'
    """
    resolved_model = _resolve_model(model)

    # Base metadata available even on failure
    metadata = {
        "model": resolved_model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "image_size": image_size,
        "use_search": use_search,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

        if output_path is None:
            output_path = generate_output_path()

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Merge input_path and input_paths into a single list
        all_inputs = []
        if input_path:
            all_inputs.append(input_path)
        if input_paths:
            all_inputs.extend(input_paths)

        metadata["input_images"] = all_inputs or None

        # Build contents
        contents = []

        for img_path in all_inputs:
            image_data, mime_type = load_image_bytes(img_path)
            contents.append(
                types.Part.from_bytes(data=image_data, mime_type=mime_type)
            )
            if verbose:
                print(f"Input image: {img_path}")

        contents.append(prompt)

        # Build config kwargs
        config_kwargs = {
            "response_modalities": ["IMAGE", "TEXT"],
        }

        # Image config (aspect ratio + size)
        image_config_dict = {}
        if aspect_ratio:
            if aspect_ratio not in VALID_ASPECT_RATIOS:
                print(f"Warning: Invalid aspect ratio '{aspect_ratio}'. Valid options: {VALID_ASPECT_RATIOS}")
            else:
                image_config_dict["aspect_ratio"] = aspect_ratio
        if image_size:
            size_upper = image_size.upper()
            if size_upper not in VALID_SIZES:
                print(f"Warning: Invalid size '{image_size}'. Valid options: {VALID_SIZES}")
            else:
                image_config_dict["image_size"] = size_upper

        if image_config_dict:
            config_kwargs["image_config"] = types.ImageConfig(**image_config_dict)

        # Google Search grounding
        if use_search:
            config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]

        generate_config = types.GenerateContentConfig(**config_kwargs)

        if verbose:
            print(f"Model: {resolved_model}")
            print(f"Prompt: {prompt}")
            if aspect_ratio:
                print(f"Aspect ratio: {aspect_ratio}")
            if image_size:
                print(f"Size: {image_size}")
            if use_search:
                print("Search grounding: enabled")
            print("Generating...")

        def _api_call():
            return client.models.generate_content(
                model=resolved_model,
                contents=contents,
                config=generate_config,
            )

        response = _retry_with_backoff(_api_call, max_retries=max_retries)

        # Extract image, text, and thinking from response
        image_data = None
        text_response = None
        thinking = None

        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type
            elif hasattr(part, "thought") and part.thought:
                thinking = part.text
            elif part.text:
                text_response = part.text

        metadata["text_response"] = text_response
        metadata["thinking"] = thinking

        if not image_data:
            error_msg = text_response or "No image generated"
            return {
                "success": False,
                "error": error_msg,
                "path": None,
                "metadata": metadata,
            }

        # Save image
        with open(output_path, "wb") as f:
            f.write(image_data)

        if verbose:
            print(f"Saved: {output_path}")
            if text_response:
                print(f"Model response: {text_response}")

        metadata["timestamp"] = datetime.now().isoformat()

        return {
            "success": True,
            "path": output_path,
            "error": None,
            "metadata": metadata,
        }

    except Exception as e:
        error_msg = str(e)
        if "safety" in error_msg.lower():
            error_msg = "Content blocked by safety filters. Try rephrasing your prompt."
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            error_msg = f"Rate limit exceeded after {max_retries} retries. Wait and try again."

        return {
            "success": False,
            "error": error_msg,
            "path": None,
            "metadata": metadata,
        }


def edit_image(
    prompt: str,
    input_path: str,
    output_path: str = None,
    model: str = "pro",
    verbose: bool = False,
) -> dict:
    """Convenience function for image editing."""
    return generate_image(
        prompt=prompt,
        output_path=output_path,
        input_path=input_path,
        model=model,
        verbose=verbose,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google Gemini (Nano Banana)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "a cute robot mascot" -o robot.png
  %(prog)s "make the sky purple" -i photo.jpg -o edited.png
  %(prog)s "cinematic landscape" --ratio 21:9 --size 4K -o landscape.png
  %(prog)s "quick sketch" --model flash -o sketch.png
  %(prog)s "combine styles" -i ref1.png ref2.png -o combined.png
        """
    )

    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-i", "--input", nargs="+",
                       help="Input image(s) for editing / reference (up to 14)")
    parser.add_argument("-m", "--model", default="pro",
                       help="Model: 'pro' (default), 'flash', or full model ID")
    parser.add_argument("-r", "--ratio", choices=VALID_ASPECT_RATIOS,
                       help="Aspect ratio (default: 1:1)")
    parser.add_argument("-s", "--size", choices=["1K", "2K", "4K", "1k", "2k", "4k"],
                       help="Image size (1K, 2K, or 4K)")
    parser.add_argument("--search", action="store_true",
                       help="Enable Google Search grounding")
    parser.add_argument("--retries", type=int, default=3,
                       help="Max retries on rate limit (default: 3)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Show detailed output")

    args = parser.parse_args()

    # Split input list into input_paths for multi-image support
    input_paths = args.input if args.input else None

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        input_paths=input_paths,
        aspect_ratio=args.ratio,
        image_size=args.size.upper() if args.size else None,
        use_search=args.search,
        model=args.model,
        max_retries=args.retries,
        verbose=args.verbose or (args.output is None),
    )

    if result["success"]:
        print(result["path"])
        sys.exit(0)
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
