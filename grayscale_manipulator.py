"""Grayscale image manipulator."""


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
