"""Check the quality of the lzw compression."""
from grayscale_manipulator import GrayscaleImage


def check_quality():
    """Check the quality of the lzw compression."""
    chess_img = GrayscaleImage.from_file('chess.png')
    chess_img.lzw_compression('chess_compressed')
    chess_img = chess_img.lzw_decompression('chess_grayscale.png')
    chess_img.lzw.save_pickle('chess_raw.pickle')

    mountain_img = GrayscaleImage.from_file('mountain.png')
    mountain_img.lzw_compression('mountain_compressed')
    mountain_img = mountain_img.lzw_decompression('mountain_grayscale.png')
    mountain_img.lzw.save_pickle('mountain_raw.pickle')
