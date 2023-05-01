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
