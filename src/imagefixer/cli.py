"""Command line interface for imagefixer."""

import argparse
import sys

from .core import ImageProcessor


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="imagefixer",
        description="Resize images and create thumbnails",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  imagefixer image.jpg                    # Process single image
  imagefixer /path/to/images/             # Process directory
  imagefixer image.jpg -o /output/        # Specify output directory
  imagefixer /images/ -q 95 -t 80         # Custom quality settings
        """.strip(),
    )

    parser.add_argument(
        "path", help="Path to image file or directory containing images"
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Output directory (default: same as input)",
        default=None,
    )

    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=85,
        help="JPEG quality for resized images (1-100, default: 85)",
    )

    parser.add_argument(
        "-t",
        "--thumbnail-quality",
        type=int,
        default=70,
        help="JPEG quality for thumbnails (1-100, default: 70)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate command line arguments."""
    if not 1 <= args.quality <= 100:
        raise ValueError("Quality must be between 1 and 100")

    if not 1 <= args.thumbnail_quality <= 100:
        raise ValueError("Thumbnail quality must be between 1 and 100")


def main(argv: list | None = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        validate_args(args)

        processor = ImageProcessor(
            quality=args.quality, thumbnail_quality=args.thumbnail_quality
        )

        processor.process_path(args.path, args.output)

        print(f"✅ Successfully processed: {args.path}")
        return 0

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
