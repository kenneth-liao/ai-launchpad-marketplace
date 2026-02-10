#!/usr/bin/env python3
"""
Batch image generation using Nano Banana (Google Gemini).

Usage:
    python batch_generate.py "pixel art logo" -n 20 -d ./logos -p logo
    python batch_generate.py "product photo" -n 10 --ratio 1:1 --size 4K
    python batch_generate.py "landscape" -n 20 --parallel 5  # 5 concurrent requests
    python batch_generate.py "quick test" -n 5 --model flash
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

# Reliable import regardless of working directory
sys.path.insert(0, str(Path(__file__).parent))
from generate import generate_image, VALID_ASPECT_RATIOS, VALID_SIZES

# Thread-safe print lock
print_lock = Lock()


def _generate_single(args_tuple):
    """Worker function for parallel generation."""
    i, count, filepath, prompt, aspect_ratio, image_size, model, use_search, max_retries, verbose = args_tuple
    filename = filepath.name

    result = generate_image(
        prompt=prompt,
        output_path=str(filepath),
        aspect_ratio=aspect_ratio,
        image_size=image_size,
        model=model,
        use_search=use_search,
        max_retries=max_retries,
        verbose=False,
    )

    result["index"] = i
    result["filename"] = filename

    if verbose:
        with print_lock:
            status = "OK" if result["success"] else f"FAILED: {result['error']}"
            print(f"[{i}/{count}] {filename}: {status}")

    return result


def batch_generate(
    prompt: str,
    count: int = 10,
    output_dir: str = None,
    prefix: str = "image",
    aspect_ratio: str = None,
    image_size: str = None,
    model: str = "pro",
    use_search: bool = False,
    max_retries: int = 3,
    delay: float = 3.0,
    parallel: int = 1,
    verbose: bool = True,
    on_progress: callable = None,
) -> list[dict]:
    """
    Generate multiple images with sequential naming.

    Args:
        prompt: Text description for image generation
        count: Number of images to generate
        output_dir: Directory to save images
        prefix: Filename prefix
        aspect_ratio: Aspect ratio (1:1, 16:9, etc.)
        image_size: Resolution (1K, 2K, or 4K)
        model: Model shorthand ("pro", "flash") or full model ID
        use_search: Enable Google Search grounding
        max_retries: Max retries per image on rate limit errors
        delay: Seconds to wait between generations (ignored if parallel > 1)
        parallel: Number of concurrent requests (default: 1, max recommended: 5)
        verbose: Print progress
        on_progress: Optional callback(completed, total, result) after each image

    Returns:
        List of result dicts
    """
    if output_dir is None:
        output_dir = os.environ.get("IMAGE_OUTPUT_DIR", os.path.join(Path.home(), "Downloads"))
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Generating {count} images...")
        print(f"Prompt: {prompt}")
        print(f"Output: {output_dir}/{prefix}-XX.png")
        print(f"Model: {model}")
        if aspect_ratio:
            print(f"Aspect ratio: {aspect_ratio}")
        if image_size:
            print(f"Size: {image_size}")
        if use_search:
            print("Search grounding: enabled")
        if parallel > 1:
            print(f"Parallel workers: {parallel}")
        print()

    # Prepare tasks
    tasks = []
    for i in range(1, count + 1):
        filename = f"{prefix}-{str(i).zfill(2)}.png"
        filepath = output_path / filename
        tasks.append((i, count, filepath, prompt, aspect_ratio, image_size, model, use_search, max_retries, verbose))

    results = []
    completed = 0

    if parallel > 1:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = [executor.submit(_generate_single, task) for task in tasks]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                if on_progress:
                    on_progress(completed, count, result)
    else:
        # Sequential execution with delay
        for task in tasks:
            result = _generate_single(task)
            results.append(result)
            completed += 1
            if on_progress:
                on_progress(completed, count, result)
            # Delay between requests (except for last one)
            if task[0] < count and delay > 0:
                time.sleep(delay)

    # Sort results by index
    results.sort(key=lambda x: x["index"])

    success_count = sum(1 for r in results if r["success"])

    if verbose:
        print()
        print(f"Complete: {success_count}/{count} images generated")
        print(f"Saved to: {output_dir}/")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate images using Nano Banana",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "pixel art logo" -n 20 -d ./logos -p logo
  %(prog)s "product photo" -n 10 --ratio 1:1 --size 4K
  %(prog)s "landscape painting" -n 5 --ratio 16:9 --delay 5
  %(prog)s "quick test" -n 5 --model flash
        """
    )

    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("-n", "--count", type=int, default=10,
                       help="Number of images to generate (default: 10)")
    parser.add_argument("-d", "--dir", default=None,
                       help="Output directory (default: ~/Downloads)")
    parser.add_argument("-p", "--prefix", default="image",
                       help="Filename prefix (default: image)")
    parser.add_argument("-m", "--model", default="pro",
                       help="Model: 'pro' (default), 'flash', or full model ID")
    parser.add_argument("-r", "--ratio", choices=VALID_ASPECT_RATIOS,
                       help="Aspect ratio")
    parser.add_argument("-s", "--size", choices=["1K", "2K", "4K", "1k", "2k", "4k"],
                       help="Image size (1K, 2K, or 4K)")
    parser.add_argument("--search", action="store_true",
                       help="Enable Google Search grounding")
    parser.add_argument("--retries", type=int, default=3,
                       help="Max retries per image on rate limit (default: 3)")
    parser.add_argument("--delay", type=float, default=3.0,
                       help="Delay between generations in seconds (default: 3, ignored if --parallel > 1)")
    parser.add_argument("--parallel", type=int, default=1,
                       help="Number of concurrent requests (default: 1, max recommended: 5)")
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="Suppress progress output")

    args = parser.parse_args()

    results = batch_generate(
        prompt=args.prompt,
        count=args.count,
        output_dir=args.dir,
        prefix=args.prefix,
        aspect_ratio=args.ratio,
        image_size=args.size.upper() if args.size else None,
        model=args.model,
        use_search=args.search,
        max_retries=args.retries,
        delay=args.delay,
        parallel=args.parallel,
        verbose=not args.quiet,
    )

    # Exit with error if all failed
    success_count = sum(1 for r in results if r["success"])
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
