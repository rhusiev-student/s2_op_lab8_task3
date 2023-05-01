"""Grayscale image manipulator."""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageOps


class GrayscaleImage:
    """Grayscale image manipulator class."""

    def __init__(self, nrows: int, ncols: int) -> None:
        """Initialize grayscale image.

        Args:
            nrows (int): number of rows
            ncols (int): number of columns
        """
        self._nrows = nrows
        self._ncols = ncols
        self._pixels = [[0 for _ in range(ncols)] for _ in range(nrows)]

    def width(self) -> int:
        """Return image width.

        Returns:
            int: image width
        """
        return self._ncols

    def height(self) -> int:
        """Return image height.

        Returns:
            int: image height
        """
        return self._nrows

    def clear(self, value: int = 0) -> None:
        """Clear image.

        Args:
            value (int, optional): pixel value to clear image with. Defaults to 0.
        """
        self._pixels = [[value for _ in range(self._ncols)] for _ in range(self._nrows)]

    def __getitem__(self, index: tuple) -> int:
        """Return pixel value at given coordinates.

        Args:
            index (tuple): coordinates

        Returns:
            int: pixel value
        """
        return self._pixels[index[0]][index[1]]

    def __setitem__(self, index: tuple, value: int) -> None:
        """Set pixel value at given coordinates.

        Args:
            index (tuple): coordinates
            value (int): pixel value
        """
        self._pixels[index[0]][index[1]] = value

    def __str__(self) -> str:
        """Return string representation of image.

        Returns:
            str: string representation of image
        """
        return "\n".join(
            [" ".join([str(pixel) for pixel in row]) for row in self._pixels]
        )

    @staticmethod
    def from_file(path: str) -> GrayscaleImage:
        """Read image from file in png or jpeg format.

        Args:
            path (str): path to image file

        Returns:
            GrayscaleImage: grayscale image
        """
        image = np.array(ImageOps.grayscale(Image.open(path)))
        nrows, ncols = image.shape
        grayscale_image = GrayscaleImage(nrows, ncols)
        for row in range(nrows):
            for col in range(ncols):
                grayscale_image[row, col] = image[row, col]
        return grayscale_image

    def to_file(self, path: str) -> None:
        """Write image to file in png format.

        Args:
            path (str): path to image file
        """
        image = np.array(self._pixels, dtype=np.uint8)
        Image.fromarray(image).save(path)
