# Grayscale Image manipulator
## Description
A module to:
- Convert images to grayscale
- Manipulate them
- Compress and decompress using lzw

It was tested on png and jpg images.

## Usage
```python
from grayscale_manipulator import GrayscaleImage


# Create a GrayscaleImage object from a path(it automatically converts it to grayscale)
img = GrayscaleImage.from_path('path/to/image')

# Save this image
img.to_file('path/to/save')

# Compress to a file, using lzw
img.lzw_compression('path/to/save')

# Decompress from a file, using lzw
img = GrayscaleImage.lzw_decompression('path/to/compressed')
```

## Requirements
- pillow
- numpy

## Compression quality
This module uses custom lzw compression

The benchmarks were done using `quality.py` on 2 images:
1. *Chess* image:
    - Colourful
    - 721x722 pixels
    - 107.4 KiB
2. *Mountain* image:
    - Already grayscale
    - 1921x1081 pixels
    - 319.9 KiB

### Results
|                      | Chess     | Mountain   |
| ---                  | ---       | ---        |
| Original size        | 107.4 KiB | 319.9 KiB  |
| Grayscale png size   | 49.2 KiB  | 732.1 KiB  |
| Raw size             | 66006 KiB | 31115 KiB  |
| Compressed size      | 76.2 KiB  | 1752.2 KiB |
| Compressed/Grayscale | 155%      | 239%       |
| Compressed/Raw       | 0.12%     | 5.63%      |

As we can see, the compression is working and does pretty well, compared to storing the entire matrix of values

However, the existing jpg and png formats are still more effective

Moreover, they take far less time, compared to lzw:

| Time(s)       | Chess | Mountain |
| Compression   | 39.5  | 937.1    |
| Decompression | 0.1   | 0.7      |

As we can see, the existing formats are a bit more effective and a lot faster

Nevertheless, it was still a nice experience to implement this compression algorithm
