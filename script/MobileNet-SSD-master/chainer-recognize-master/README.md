# Image Recognizer with Chainer

## Requirement

* [Chainer](http://chainer.org/)
* [Pillow](https://pillow.readthedocs.org/en/3.0.x/)
* Caffe Model  
  Download *.caffemodel from:
    * [VGG_ILSVRC_19_layers](https://gist.github.com/ksimonyan/3785162f95cd2d5fee77)
    * [bvlc_googlenet](https://github.com/BVLC/caffe/tree/master/models/bvlc_googlenet)
    * [Network in Network Imagenet Model](https://gist.github.com/mavenlin/d802a5849de39225bcc6)
* Some image files

## Example

```py
from model import GoogleNet
m = GoogleNet()
m.load("bvlc_googlenet.caffemodel")
m.load_label("labels.txt")
m.print_prediction("image.png")
```

## License

MIT
