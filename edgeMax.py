# load and display an image with Matplotlib
import numpy as np

from PIL import Image
from pathlib import Path
from scipy import ndimage as nd
from numpy import ma as ma
import os
import glob

# folder with images to be processed
current_dir = Path('./processed/numpyTrim').resolve()


def first_nonzero(arr, axis, invalid_val=-1):
    mask = arr!=0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


# load images in folder as greyscale
for arr in glob.glob(str(current_dir / "*.npy")):
    filename = Path(arr).stem
    image = np.load(arr)
    # all pixels with brightness below 150 are set to black
    image[image < 150] = 0
    image[image >= 150] = 255
    # rotate image 50 deg ccw (CNGA edge-angle is 80 deg, the edge is now fully horizontal)
    rotateArr = nd.rotate(image, 50)
    Image.fromarray(rotateArr).save(str(current_dir/ f'{filename}_rotate.png'))
    # get index of first nonzero element in each row, set others to 300 (above white to allow for minimum)
    firsts = first_nonzero(rotateArr, axis=1, invalid_val=300)
    # find minimum x-index along all rows and return it
    # TODO get thresholds for different edge-radii from GIMP and implement classification
    # TODO double check final images for non zero/255 pixels
    xCorner = min(firsts)
    if xCorner <= 55:
        rad = '0.8 mm'
    elif 70 >= xCorner > 55:
        rad = '1.2 mm'
    else:
        rad = '1.6 mm'
    print(str(filename) + ' has a corner radius of ' + rad)
