"""Check the quality of the lzw compression."""
from grayscale_manipulator import GrayscaleImage
import timeit
import os


def check_quality():
    """Check the quality of the lzw compression."""
    print("Chess image:")
    original_size = os.path.getsize("chess.png") / 1024
    print("    Original size:", original_size, "KiB")
    chess_img = GrayscaleImage.from_file("chess.png")

    start = timeit.default_timer()
    chess_img.lzw_compression("chess_compressed")
    stop = timeit.default_timer()
    print("    Compression time: ", stop - start)
    compressed_size = os.path.getsize("chess_compressed") / 1024
    print(f"    Compressed size: {compressed_size} KiB")

    start = timeit.default_timer()
    chess_img = chess_img.lzw_decompression("chess_grayscale.png")
    stop = timeit.default_timer()
    print("    Decompression time: ", stop - start)

    chess_img.lzw.save_pickle("chess_raw.pickle")
    print("    Raw size: ", os.path.getsize("chess_raw.pickle") / 1024, "KiB")

    print()
    print("Mountain image:")
    original_size = os.path.getsize("mountain.jpg") / 1024
    print("    Original size:", original_size, "KiB")
    mountain_img = GrayscaleImage.from_file("mountain.jpg")

    start = timeit.default_timer()
    mountain_img.lzw_compression("mountain_compressed")
    stop = timeit.default_timer()
    print("    Compression time: ", stop - start)
    compressed_size = os.path.getsize("mountain_compressed") / 1024
    print(f"    Compressed size: {compressed_size} KiB")

    start = timeit.default_timer()
    mountain_img = mountain_img.lzw_decompression("mountain_grayscale.png")
    stop = timeit.default_timer()
    print("    Decompression time: ", stop - start)

    mountain_img.lzw.save_pickle("mountain_raw.pickle")
    print("    Raw size: ", os.path.getsize("mountain_raw.pickle") / 1024, "KiB")


if __name__ == "__main__":
    check_quality()
