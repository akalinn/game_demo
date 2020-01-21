from PIL import Image
import numpy as np
import chainer
from chainer import cuda
import chainer.functions as F
from chainer.functions import caffe

class NNModel(object):
    def __init__(self):
        self.image_shape = self._image_shape()
        self.mean_image = self._mean_image()
        self.func = None
        self.categories = None

    def load(self, path):
        self.func = caffe.CaffeFunction(path)

    def load_label(self, path):
        self.categories = np.loadtxt(path, str, delimiter="\n")

    def print_prediction(self, image_path, rank=10):
        prediction = self.predict(image_path, rank)
        for i, (score, label) in enumerate(prediction[:rank]):
            print '{:>3d} {:>6.2f}% {}'.format(i + 1, score * 100, label)

    def predict(self, image_path, rank=10):
        x = chainer.Variable(self.load_image(image_path), volatile=True)
        y = self._predict_class(x)
        result = zip(y.data.reshape((y.data.size,)), self.categories)
        return sorted(result, reverse=True)

    def load_image(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image_w, image_h = self.image_shape
        w, h = image.size
        if w > h:
            shape = (image_w * w / h, image_h)
        else:
            shape = (image_w, image_h * h / w)
        x = (shape[0] - image_w) / 2
        y = (shape[1] - image_h) / 2
        pixels = np.asarray(image.resize(shape).crop((x, y, x + image_w, y + image_h))).astype(np.float32)
        pixels = pixels[:,:,::-1].transpose(2,0,1)
        pixels -= self.mean_image
        return pixels.reshape((1,) + pixels.shape)

    def _image_shape(self):
        raise NotImplementedError

    def _mean_image(self):
        raise NotImplementedError

    def _predict_class(x):
        raise NotImplementedError

class GoogleNet(NNModel):
    def __init__(self):
        NNModel.__init__(self)

    def _image_shape(self):
        return (224, 224)

    def _mean_image(self):
        mean_image = np.ndarray((3, 224, 224), dtype=np.float32)
        mean_image[0] = 103.939
        mean_image[1] = 116.779
        mean_image[2] = 123.68
        return mean_image

    def _predict_class(self, x):
        y, = self.func(inputs={'data': x}, outputs=['loss3/classifier'], disable=['loss1/ave_pool', 'loss2/ave_pool'], train=False)
        return F.softmax(y)

class VGG19(NNModel):
    def __init__(self):
        NNModel.__init__(self)

    def _image_shape(self):
        return (224, 224)

    def _mean_image(self):
        mean_image = np.ndarray((3, 224, 224), dtype=np.float32)
        mean_image[0] = 103.939
        mean_image[1] = 116.779
        mean_image[2] = 123.68
        return mean_image

    def _predict_class(self, x):
        y, = self.func(inputs={'data': x}, outputs=['fc8'], train=False)
        return F.softmax(y)

class NIN(NNModel):
    def __init__(self):
        NNModel.__init__(self)

    def _image_shape(self):
        return (224, 224)

    def _mean_image(self):
        mean_image = np.ndarray((3, 224, 224), dtype=np.float32)
        mean_image[0] = 103.939
        mean_image[1] = 116.779
        mean_image[2] = 123.68
        return mean_image

    def _predict_class(self, x):
        y, = self.func(inputs={'data': x}, outputs=['pool4'], train=False)
        return F.softmax(y)
