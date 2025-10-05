"""Core image processing functionality."""

import os
from pathlib import Path

from PIL import Image


class ImageProcessor:
    """Main class for image processing operations."""

    def __init__(self, quality: int = 85, thumbnail_quality: int = 70):
        """Initialize ImageProcessor with quality settings.

        Args:
            quality: JPEG quality for resized images (1-100)
            thumbnail_quality: JPEG quality for thumbnails (1-100)
        """
        self.quality = quality
        self.thumbnail_quality = thumbnail_quality

    @staticmethod
    def scale_size(size: tuple[int, int], factor: int) -> tuple[int, int]:
        """Scale a size tuple by a factor.

        Args:
            size: (width, height) tuple
            factor: scaling factor

        Returns:
            Scaled (width, height) tuple
        """
        return (size[0] // factor, size[1] // factor)

    def save_image(
        self,
        img: Image.Image,
        filename: str,
        outfile: str,
        quality: int | None = None,
    ) -> None:
        """Save image to specified location.

        Args:
            img: PIL Image object
            filename: output filename
            outfile: output directory
            quality: JPEG quality override
        """
        if quality is None:
            quality = self.quality

        path = os.path.join(outfile, filename)
        img.save(path, quality=quality)

    def make_resized(self, img: Image.Image) -> Image.Image:
        """Create a resized version of the image.

        Args:
            img: PIL Image object

        Returns:
            Resized PIL Image object
        """
        size = img.size
        factor = 2

        if size[0] > 1000:
            factor = size[0] // 1000

        new_size = self.scale_size(size, factor)
        return img.resize(new_size)

    def make_thumbnail(self, img: Image.Image) -> Image.Image:
        """Create a square thumbnail from the image.

        Args:
            img: PIL Image object

        Returns:
            Square thumbnail PIL Image object
        """
        factor = 2
        if img.size[0] > 1000:
            factor = img.size[0] // 1000

        # Reduce size by factor * 2
        size = self.scale_size(img.size, factor * 2)
        resized_img = img.resize(size)

        # Create square crop from center
        start_x = (size[0] - size[1]) // 2
        box = (start_x, 0, start_x + size[1], size[1])
        return resized_img.crop(box)

    def process_image(self, imgfile: str, outfile: str) -> None:
        """Process a single image file.

        Args:
            imgfile: path to input image
            outfile: path to output directory
        """
        # Read the image
        img = Image.open(imgfile)

        # Extract filename without extension
        pieces = os.path.split(imgfile)
        filename = os.path.splitext(pieces[1])[0]

        # Save resized image
        self.save_image(self.make_resized(img), f"{filename}_md.jpg", outfile)

        # Save thumbnail
        self.save_image(
            self.make_thumbnail(img),
            f"{filename}_sq_thumb.jpg",
            outfile,
            self.thumbnail_quality,
        )

    def process_directory(self, directory: str, outfile: str) -> None:
        """Process all JPEG images in a directory.

        Args:
            directory: path to input directory
            outfile: path to output directory
        """
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            if (
                os.path.isfile(file_path)
                and os.path.splitext(file_path)[1].lower() == ".jpg"
            ):
                self.process_image(file_path, outfile)

    def process_path(self, input_path: str, output_path: str | None = None) -> None:
        """Process a file or directory of images.

        Args:
            input_path: path to input file or directory
            output_path: path to output directory (optional)

        Raises:
            FileNotFoundError: if input_path doesn't exist
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Path doesn't exist: {input_path}")

        # Determine output path if not provided
        if not output_path or not os.path.isdir(output_path):
            if os.path.isfile(input_path):
                output_path = os.path.split(input_path)[0]
            elif os.path.isdir(input_path):
                output_path = input_path

        # Ensure output directory exists
        Path(output_path).mkdir(parents=True, exist_ok=True)

        # Process based on input type
        if os.path.isfile(input_path):
            self.process_image(input_path, output_path)
        elif os.path.isdir(input_path):
            self.process_directory(input_path, output_path)
