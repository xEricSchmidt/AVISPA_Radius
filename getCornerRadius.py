"""
=====================================================
Determine corner radius of a cutting insert based on a K-Lens topdown-image
for CNGA inserts
=====================================================
"""

import glob
import os
import numpy as np
from numpy import asarray
from PIL import Image
from pathlib import Path
from scipy import ndimage as nd


# Requires the Coordinates of the center image of a K-Lens compound image to be passed
def get_corner_radius(im_path):
    """Detect the corner radius of a CNGA-Insert from a K-Lens Image"""
    print("Image processing started.")

    current_dir = Path('.').resolve()
    filename, file_extension = os.path.splitext(im_path)

    if file_extension == ".bmp":
        Image.open(im_path).save(str(current_dir / f'{filename}.png'))
        file_extension = '.png'
        im_path = str(filename + file_extension )

    image = Image.open(im_path).convert('L')  # load image as greyscale
    data = asarray(image)  # convert image to numpy array

    x_min_trim = 222  # measure coordinates close to insert edges for center image of K-Lens-Compound image
    x_max_trim = 777
    y_min_trim = 1100
    y_max_trim = 1570

    data_trimmed = data[x_min_trim:x_max_trim, y_min_trim:y_max_trim]  # trim numpy array (coordinates from GIMP, width 1100-1570, height 222-777)

    data_trimmed[data_trimmed < 150] = 0  # all pixels with brightness below 150 are set to black
    data_trimmed[data_trimmed >= 150] = 255  # all pixels with brightness above 150 are set to white

    data_rotated = nd.rotate(data_trimmed, 50)  # rotate image 50 deg ccw (CNGA edge-angle is 80 deg)
    Image.fromarray(data_rotated).save(str(current_dir / f'{filename}_rotated.png'))  # save image to measure corner positions

    cutoff_08_12 = 55  # measure coordinates for leftmost edge in rotated image (leave some space for fluctuation)
    cutoff_12_16 = 70

    firsts = first_nonzero(data_rotated, axis=1, invalid_val=300) # get index of first nonzero element in each row, set zeroes to 300
    x_corner = min(firsts)  # leftmost nonzero point represents corner coordinate in pixel
    if x_corner <= cutoff_08_12:
        rad = '0.8 mm'
    elif cutoff_12_16 >= x_corner > cutoff_08_12:
        rad = '1.2 mm'
    else:
        rad = '1.6 mm'

    print("Image processing finished.")
    return rad, filename


def first_nonzero(arr, axis, invalid_val=-1):
    """Find first nonzero Element in each column (0) or row (1) of a numpy array"""
    mask = arr != 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def main():
    file_name = 'CNGA RADIO 1.2mm.bmp_sub5.bmp'  # file in same folder as script
    radius, filename = get_corner_radius(file_name)
    out_str = str(filename + ' has a corner radius of ' + radius)
    print(out_str)


if __name__ == "__main__":
    main()
