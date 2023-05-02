"""Grayscale image manipulator."""
from __future__ import annotations
from typing import Iterable
import struct

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

    def lzw_compression(self, path: str) -> None:
        """Compress image using LZW algorithm.

        Args:
            path (str): path to compressed image file

        Raises:
            ValueError: LZW compression failed
        """
        lzw = LZW(self._pixels, None)
        lzw.compress()
        if lzw.compressed_data is None:
            raise ValueError("LZW compression failed.")
        with open(path, "wb") as file:
            file.write(lzw.compressed_data)

    @staticmethod
    def lzw_decompression(path: str) -> GrayscaleImage:
        """Decompress image using LZW algorithm.

        Args:
            path (str): path to compressed image file

        Returns:
            GrayscaleImage: decompressed image

        Raises:
            ValueError: LZW decompression failed
        """
        with open(path, "rb") as file:
            compressed_data = file.read()
        lzw = LZW(None, compressed_data)
        lzw.decompress()
        if lzw.raw_data is None:
            raise ValueError("LZW decompression failed.")
        return GrayscaleImage.from_matrix(lzw.to_matrix())

    @staticmethod
    def from_matrix(matrix: list[list[int]]) -> GrayscaleImage:
        """Create image from matrix.

        Args:
            matrix (list[list[int]]): matrix

        Returns:
            GrayscaleImage: grayscale image
        """
        nrows = len(matrix)
        ncols = len(matrix[0])
        image = GrayscaleImage(nrows, ncols)
        for row in range(nrows):
            for col in range(ncols):
                image[row, col] = matrix[row][col]
        return image


class LZW:
    """LZW algorithm implementation."""

    def __init__(
        self,
        raw_data: list[list[int]] | None = None,
        compressed_data: bytes | None = None,
    ) -> None:
        """Initialize LZW algorithm.

        Args:
            raw_data (list[list[int]] | list[int] | None): raw data
            compressed_data (bytes | None): compressed data
        """
        if raw_data is not None:
            self.height = len(raw_data)
            self.width = len(raw_data[0])
            self.raw_data = [pixel for row in raw_data for pixel in row]
        self.compressed_data = compressed_data
        self.max_dictionary_size = 2 ** 16

    def compress(self) -> None:
        """Compress data using LZW algorithm.

        Raises:
            ValueError: raw data is not set
        """
        if self.raw_data is None:
            raise ValueError("Raw data is not set.")
        compressed = []
        start_dictionary: list[int] = list(set(self.raw_data))
        dictionary = [[pixel] for pixel in start_dictionary]
        dict_size = len(dictionary)
        i = 0
        while i < len(self.raw_data):
            prefix_id = self._find_longest_prefix(
                dictionary, (self.raw_data[j] for j in range(i, len(self.raw_data)))
            )
            if prefix_id == -1:
                break
            prefix = dictionary[prefix_id]
            compressed.append(prefix_id)
            i += len(prefix)
            if i < len(self.raw_data) and dict_size < self.max_dictionary_size:
                dictionary.append(prefix + [self.raw_data[i]])
                dict_size += 1

        start_dict_bytes = bytes(start_dictionary)
        compressed_bytes = b""
        for i in compressed:
            compressed_bytes += struct.pack(">H", i)
        shape_header = struct.pack(">HH", self.height, self.width)
        start_dict_header = struct.pack(">H", len(start_dict_bytes))
        compressed_header = struct.pack(">I", len(compressed_bytes))
        self.compressed_data = (
            shape_header
            + start_dict_header
            + start_dict_bytes
            + compressed_header
            + compressed_bytes
        )

    def _find_longest_prefix(
        self, dictionary: list[list[int]], sequence: Iterable[int]
    ) -> int:
        """Find longest prefix in dictionary.

        Args:
            dictionary (list[list[int]]): dictionary
            sequence (Iterable[int]): sequence

        Returns:
            int: index of longest prefix in dictionary
        """
        prefix = []
        for char in sequence:
            prefix.append(char)
            if prefix in dictionary:
                continue
            return dictionary.index(prefix[:-1])
        return dictionary.index(prefix)

    def decompress(self) -> None:
        """Decompress data using LZW algorithm.

        Raises:
            ValueError: compressed data is not set
        """
        if self.compressed_data is None:
            raise ValueError("Compressed data is not set.")
        height = struct.unpack(">H", self.compressed_data[:2])[0]
        width = struct.unpack(">H", self.compressed_data[2:4])[0]
        start_dict_size = struct.unpack(">H", self.compressed_data[4:6])[0]
        start_dict = self.compressed_data[6 : 6 + start_dict_size]
        compressed_size = struct.unpack(
            ">I", self.compressed_data[6 + start_dict_size : 10 + start_dict_size]
        )[0]
        compressed = []
        for i in range(10 + start_dict_size, 10 + start_dict_size + compressed_size, 2):
            compressed.append(struct.unpack(">H", self.compressed_data[i : i + 2])[0])
        dictionary = [[pixel] for pixel in start_dict]
        dict_size = len(dictionary)
        decompressed = []
        prev_i = compressed[0]
        decompressed += dictionary[prev_i]
        for i in compressed[1:]:
            if i >= dict_size:
                entry = dictionary[prev_i] + [dictionary[prev_i][0]]
            else:
                entry = dictionary[i]
            decompressed += entry
            if dict_size < self.max_dictionary_size:
                dictionary.append(dictionary[prev_i] + [entry[0]])
                dict_size += 1
            prev_i = i
        self.height = height
        self.width = width
        self.raw_data = decompressed

    def to_matrix(self) -> list[list[int]]:
        """Convert decompressed data to matrix.

        Returns:
            list[list[int]]: matrix
        """
        return [
            self.raw_data[i : i + self.width]
            for i in range(0, len(self.raw_data), self.width)
        ]
