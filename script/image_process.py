#def getpixel(x,y):
#    return gdi.GetPixel(windll.user32.GetDC(0),x,y)

from PIL import ImageGrab
from PIL import Image
import numpy as np
import cv2
import gc

def image_grab(region):
    if region != [] or len(region) != 4:
        im=ImageGrab.grab(bbox=region)
    else:
        im = ImageGrab.grab()
    
    im = np.asarray(im)
    return im

def image_convert(region):
    pass

def LoG(im):
    return cv2.Laplacian(im,cv2.CV_64F)

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def imshow(im):
    img = Image.fromarray(im)
    img.show()

def garbage_collect():
    gc.collect()

def image_resizing(im,basewidth,squre):

    if not squre:
        wpercent = (basewidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
    else: 
        hsize = basewidth
    
    im_resize = im.resize((basewidth, hsize))

    return im_resize

def im_linear_normalization(im):
    minn = np.min(im)
    maxx = np.max(im)

    return (im - minn) / (maxx - minn)

def gausian2D(x,y,sigma):
    return 1/(2*np.pi*np.square(sigma))*np.exp(-1*(np.square(x)+np.square(y))/(2*np.square(sigma)))

