import PIL, sys, glob
from PIL import Image
import numpy as np

sys.path.insert(0, 'toolbox/')
import image_process as ip




sample = []
for filename in glob.glob('../im_resource/*.png'):
    im=Image.open(filename)
    im = np.asarray(im).astype(np.float32)
    im = ip.im_linear_normalization(im)
    sample.append(im)

sample = np.array(sample)


import tensorflow 

mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)
