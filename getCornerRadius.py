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
        return im_path, file_extension

    # load images in folder as greyscale
    for img in glob.glob(str(current_dir / "*.png")):
        filename = Path(img).stem
        # load image as greyscale
        image = Image.open(img).convert('L')
        # save greyscale image as a copy
        image.save(str(out_dir_grey / f'{filename}_grey.png'))
        # convert image to numpy array
        data = asarray(image)
        # trim numpy array (coordinates from GIMP, width 1100-1570, height 222-777)
        dataTrim = data[222:777, 1100:1570]
        # save trimmed numpy array as binary
        np.save(str(out_dir_np_trim / f'{filename}_grey_trim.npy'), dataTrim)
        # convert trimmed numpy array to .png and save
        Image.fromarray(dataTrim).save(str(out_dir_grey_trim / f'{filename}_grey_trim.png'))

    def first_nonzero(arr, axis, invalid_val=-1):
        mask = arr != 0
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
        Image.fromarray(rotateArr).save(str(current_dir / f'{filename}_rotate.png'))
        # get index of first nonzero element in each row, set others to 300 (above white to allow for minimum)
        firsts = first_nonzero(rotateArr, axis=1, invalid_val=300)
        # find minimum x-index along all rows and return it

        xCorner = min(firsts)
        if xCorner <= 55:
            rad = '0.8 mm'
        elif 70 >= xCorner > 55:
            rad = '1.2 mm'
        else:
            rad = '1.6 mm'
        print(str(filename) + ' has a corner radius of ' + rad)




    print("Image processing finished.")
    return cornerRadius


def main():
    message = "Running as Script"
    get_corner_radius('CNGA RADIO 1.2mm.bmp_sub5.bmp')
    print(message)


if __name__ == "__main__":
    main()
