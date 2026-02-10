---
name: nanobanana
description: Generate and edit images using Google Gemini (Nano Banana). Supports Pro and Flash models, multi-image references, text-to-image, image editing, 1K/2K/4K resolution, and Google Search grounding.
triggers:
  - "generate image"
  - "create image"
  - "nano banana"
  - "nanobanana"
  - "gemini image"
  - "AI image"
  - "image generation"
---

# Nano Banana - AI Image Generation

Generate and edit images using Google Gemini models. Supports two models:
- **Pro** (`gemini-3-pro-image-preview`) — High quality, complex prompts, thinking mode
- **Flash** (`gemini-2.5-flash-image`) — Fast, cheap, good for iteration

## Prerequisites

**Required:**
- `GEMINI_API_KEY` — Get from [Google AI Studio](https://aistudio.google.com/apikey)
- [`uv`](https://docs.astral.sh/uv/) (recommended) or Python 3.10+ with `google-genai` installed

**With `uv` (recommended — zero setup):**
Dependencies are declared inline via PEP 723 and auto-installed on first run. Just use `uv run` instead of `python3`.

**With pip (fallback):**
```bash
pip install -r <skill_dir>/requirements.txt
```

## Quick Start

### Generate an image:
```bash
uv run <skill_dir>/scripts/generate.py "a cute robot mascot, pixel art style" -o robot.png
```

### Edit an existing image:
```bash
uv run <skill_dir>/scripts/generate.py "make the background blue" -i input.jpg -o output.png
```

### Use Flash model for fast iteration:
```bash
uv run <skill_dir>/scripts/generate.py "quick sketch of a cat" --model flash -o sketch.png
```

### Multi-image reference (style + subject):
```bash
uv run <skill_dir>/scripts/generate.py "apply the style of the first image to the second" \
  -i style_ref.png subject.jpg -o styled.png
```

### Generate with specific aspect ratio and resolution:
```bash
uv run <skill_dir>/scripts/generate.py "cinematic landscape" --ratio 21:9 --size 4K -o landscape.png
```

## Model Selection Guide

| | Pro (default) | Flash |
|---|---|---|
| **Speed** | Slower | ~2-3x faster |
| **Cost** | Higher | Lower |
| **Text rendering** | Good | Unreliable |
| **Complex scenes** | Excellent | Adequate |
| **Thinking mode** | Yes | No |
| **Best for** | Final production images | Exploration, drafts, batch |

**Rule of thumb:** Use Flash for exploration and batch generation, Pro for final output.

## Script Reference

### `scripts/generate.py`

Main image generation script.

```
Usage: generate.py [OPTIONS] PROMPT

Arguments:
  PROMPT                Text prompt for image generation

Options:
  -o, --output PATH     Output file path (default: ~/Downloads/nanobanana_<timestamp>.png)
  -i, --input PATH...   Input image(s) for editing / reference (up to 14)
  -m, --model MODEL     Model: 'pro' (default), 'flash', or full model ID
  -r, --ratio RATIO     Aspect ratio (1:1, 16:9, 9:16, 21:9, etc.)
  -s, --size SIZE       Image size: 1K, 2K, or 4K (default: standard)
  --search              Enable Google Search grounding for accuracy
  --retries N           Max retries on rate limit (default: 3)
  -v, --verbose         Show detailed output
```

**Supported aspect ratios:**
- `1:1` — Square (default)
- `2:3`, `3:2` — Portrait/Landscape
- `3:4`, `4:3` — Standard
- `4:5`, `5:4` — Photo
- `9:16`, `16:9` — Widescreen
- `21:9` — Ultra-wide/Cinematic

**Image sizes:**
- `1K` — Fast, lower detail
- `2K` — Enhanced detail (2048px)
- `4K` — Maximum quality (3840px), best for text rendering

### `scripts/batch_generate.py`

Generate multiple images with sequential naming.

```
Usage: batch_generate.py [OPTIONS] PROMPT

Arguments:
  PROMPT                Text prompt for image generation

Options:
  -n, --count N         Number of images to generate (default: 10)
  -d, --dir PATH        Output directory (default: ~/Downloads)
  -p, --prefix STR      Filename prefix (default: "image")
  -m, --model MODEL     Model: 'pro' (default), 'flash', or full model ID
  -r, --ratio RATIO     Aspect ratio
  -s, --size SIZE       Image size (1K/2K/4K)
  --search              Enable Google Search grounding
  --retries N           Max retries per image on rate limit (default: 3)
  --delay SECONDS       Delay between generations (default: 3)
  --parallel N          Concurrent requests (default: 1, max recommended: 5)
  -q, --quiet           Suppress progress output
```

**Example:**
```bash
uv run <skill_dir>/scripts/batch_generate.py "pixel art logo" -n 20 --model flash -d ./logos -p logo
```

## Python API

### Direct import (from another skill's script):

> **Note:** When importing as a Python module, `google-genai` must be available in the calling script's environment. If using `uv run`, add a PEP 723 `dependencies` block to your own script (see example in Pattern 2 below).

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill_dir>/scripts")))
from generate import generate_image, edit_image, batch_generate

# Generate image
result = generate_image(
    prompt="a futuristic city at night",
    output_path="city.png",
    aspect_ratio="16:9",
    image_size="4K",
    model="pro",
)

# Edit existing image
result = edit_image(
    prompt="add flying cars to the sky",
    input_path="city.png",
    output_path="city_edited.png",
)

# Multi-image reference
result = generate_image(
    prompt="combine the color palette of the first with the composition of the second",
    input_paths=["palette_ref.png", "composition_ref.png"],
    output_path="combined.png",
)
```

### Return structure (always present):

```python
{
    "success": True,       # or False
    "path": "/path/to/output.png",  # or None on failure
    "error": None,         # or error message string
    "metadata": {
        "model": "gemini-3-pro-image-preview",
        "prompt": "...",
        "aspect_ratio": "16:9",
        "image_size": "4K",
        "use_search": False,
        "input_images": None,        # or list of paths
        "text_response": "...",      # optional text from model
        "thinking": "...",           # Pro model reasoning (when available)
        "timestamp": "2025-01-26T...",
    }
}
```

## Downstream Skill Integration Guide

### Pattern 1: CLI wrapper (recommended for simple use)

```bash
# In your skill's script:
uv run <nanobanana_dir>/scripts/generate.py "{prompt}" --model flash --ratio 16:9 -o output.png
```

### Pattern 2: Python import with custom defaults

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///

import sys
from pathlib import Path

NANOBANANA_DIR = Path("<nanobanana_dir>/scripts")
sys.path.insert(0, str(NANOBANANA_DIR))
from generate import generate_image

def generate_thumbnail(prompt: str, output_path: str) -> dict:
    """Generate a YouTube thumbnail with project defaults."""
    return generate_image(
        prompt=prompt,
        output_path=output_path,
        aspect_ratio="16:9",
        image_size="2K",
        model="flash",
        max_retries=3,
    )
```

### Pattern 3: Batch with progress tracking

```python
from batch_generate import batch_generate

def on_progress(completed, total, result):
    print(f"Progress: {completed}/{total}")

results = batch_generate(
    prompt="logo concept",
    count=20,
    output_dir="./logos",
    prefix="logo",
    model="flash",
    aspect_ratio="1:1",
    on_progress=on_progress,
)

successful = [r for r in results if r["success"]]
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `IMAGE_OUTPUT_DIR` | Default output directory | `~/Downloads` |

## Features

### Text-to-Image Generation
Create images from text descriptions. Both models excel at:
- Photorealistic images
- Artistic styles (pixel art, illustration, etc.)
- Product photography
- Landscapes and scenes

### Image Editing
Transform existing images with natural language:
- Style transfer
- Object addition/removal
- Background changes
- Color adjustments

### Multi-Image Reference
Provide up to 14 reference images for:
- Style consistency across a series
- Subject consistency (same character, different poses)
- Brand-consistent generation
- Style + subject combination

### High-Resolution Output
- **1K** — Fast generation, good for drafts
- **2K** — Enhanced detail (2048px)
- **4K** — Maximum quality (3840px), best for text rendering

### Google Search Grounding
Enable `--search` for factually accurate images involving:
- Real people, places, landmarks
- Current events
- Specific products or brands

### Automatic Retry
Rate limit errors are automatically retried with exponential backoff (default: 3 retries). No action needed from callers.

### SynthID Watermark Notice
All images generated by Gemini contain an invisible SynthID digital watermark. This is automatic, cannot be disabled, and survives common transformations (resize, crop, compression). Be aware of this for any use case requiring watermark-free output.

## Best Practices

### Prompt Writing

**Good prompts include:**
- Subject description
- Style/aesthetic
- Lighting and mood
- Composition details
- Color palette

See [references/prompts.md](./references/prompts.md) for detailed prompt templates by category and model-specific tips.

### Batch Generation Tips

1. Use `--model flash` for exploration batches (faster, cheaper)
2. Generate 10-20 variations to explore options
3. Default 3-second delay between sequential requests avoids rate limits
4. Review results and iterate on best candidates with Pro model

## Rate Limits

- Gemini API has usage quotas (~10 RPM free tier)
- Automatic retry with exponential backoff handles transient rate limits
- For large batches, use `--delay 5` or `--parallel` with modest concurrency
- Check your quota at [Google AI Studio](https://aistudio.google.com/)

## Troubleshooting

**"uv: command not found"**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`

**"Error: google-genai package not installed"**
- Use `uv run` instead of `python3` to auto-install dependencies
- Or install manually: `pip install -r <skill_dir>/requirements.txt`

**"GEMINI_API_KEY environment variable not set"**
- Set `GEMINI_API_KEY` in your environment before running

**"No image in response"**
- Prompt may have triggered safety filters
- Try rephrasing to avoid sensitive content

**"Rate limit exceeded after N retries"**
- Wait 30-60 seconds and try again
- Reduce batch parallelism or add longer delays
- Check your API quota

**Import errors in batch_generate.py**
- The script handles its own path setup; run from any directory

## Future Capabilities

**Multi-turn conversational editing** — The Gemini API supports stateful chat sessions for iterative image editing (e.g., "make it bluer" → "now add a hat" → "zoom out"). This requires fundamentally different stateful architecture and is not currently implemented. No downstream skill currently needs this.

## References

- [references/prompts.md](./references/prompts.md) — Prompt examples, model-specific tips, multi-reference patterns
- [references/gemini-api.md](./references/gemini-api.md) — Curated API reference for agent context
