import PIL, sys
from PIL import Image
import glob
import numpy as np
import get_source
import locating
import time
sys.path.insert(0, 'toolbox/')
import image_process as ip


def k_val(s):
	return np.

time.sleep(2)
#image_cnt = get_source.load_image_count()
#X = np.zeros((image_cnt['im_count'],)+(384,)+(341,))
#cnt = 0
#for filename in glob.glob('pixels/*.png'):
#    im=Image.open(filename)
#    X[cnt] = np.asarray(im)
#    cnt += 1


im = ip.image_grab(locating.locate())
im = ip.rgb2gray(im)
im = ip.image_resizing(Image.fromarray((im).astype(np.uint8)),im.shape[1]/4,False)
#print(np.asarray(im))
ip.imshow(np.array(im))
#im = ip.im_linear_normalization(np.asarray(im))


