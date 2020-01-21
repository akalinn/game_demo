import PIL, sys, glob
from PIL import Image
import numpy as np

sys.path.insert(0, '../toolbox/')
sys.path.insert(1, '../')
import image_process as ip


def pooling_avg(matrix,sz,stride):
	row,col = matrix.shape
	x, y = sz

	row = int((row-x)/stride+1);
	col = int((col-y)/stride+1)
	new_matrix = np.zeros((row,)+(col,))

	a = 0
	for i in range(0,row):
		b = 0
		for j in range(0,col):
			new_matrix[i,j] = np.mean(matrix[a:a+x,b:b+y])

			b += stride
		a += stride

	return new_matrix


def pooling_max(matrix,sz,stride):
	row,col = matrix.shape
	x, y = sz

	row = int((row-x)/stride+1);
	col = int((col-y)/stride+1)
	new_matrix = np.zeros((row,)+(col,))

	a = 0
	for i in range(0,row):
		b = 0
		for j in range(0,col):
			new_matrix[i,j] = np.max(matrix[a:a+x,b:b+y])

			b += stride
		a += stride

	return new_matrix

def sampling(matrix,stride,feature):
	row,col = matrix.shape
	x,y = feature.shape

	x = int(feature.shape[0]/2)
	y = int(feature.shape[1]/2)
	#rap zeros for image
	new_matrix = np.zeros((row+2*x,)+(col+2*y,))
	new_matrix[x:row+x,y:col+y] = matrix

	output_matrix = np.zeros((int((row-1)/stride+1),)+(int((col-1)/stride+1),))

	a = 0
	for i in range(x,row+x,stride):
		b = 0
		for j in range(y,col+y,stride):
			output_matrix[a][b] = np.sum(np.multiply(new_matrix[i-x:i+x+1,j-y:j+y+1],feature))
			b += 1
		a += 1

	return output_matrix


sample = []
for filename in glob.glob('../im_resource/*.png'):
    im=Image.open(filename)
    im = np.asarray(im).astype(np.float32)
    #im = ip.im_linear_normalization(im)
    sample.append(im)

sample = np.array(sample)

ip.imshow(sample[0])
x = sampling(sample[0],1,np.asarray([[.2,.2,.2],[.4,.4,.4],[.05,.05,.05]]))
ip.imshow(x)