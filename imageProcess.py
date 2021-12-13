"""
============================
Read .png images into Numpy Array and process
============================
"""

# load and display an image with Matplotlib
import numpy as np
from PIL import Image
from pathlib import Path
from numpy import asarray
import os
import glob

# TODO include coordinates for cutting and cropping into config file
# TODO integrate compound image cutting from matlab into script, cut only center image

# folder with images to be processed
current_dir = Path('./converted').resolve()
# output folder for processed images
out_dir = Path('./processed').resolve()
out_dir_grey = Path('./processed/greyscale').resolve()
out_dir_np_trim = Path('./processed/numpyTrim').resolve()
out_dir_grey_trim = Path('./processed/greyTrim').resolve()

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    os.mkdir(out_dir_grey)
    os.mkdir(out_dir_np_trim)
    os.mkdir(out_dir_grey_trim)

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





