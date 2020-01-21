import numpy as np

def one_hot(labels):
    classes = np.unique(labels)
    size = classes.size
    alter_label = np.zeros(labels.shape + (size,))
    for c in classes:
        alter_label[labels == c, c] = 1
    return alter_label

def unhot(one_hot_labels):
    return np.argmax(one_hot_labels, axis=-1)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))


def relu(x):
    return np.maximum(0.0, x)


def tanh(x):
    return np.tanh(x)

def sigmoid_d(x):
    s = sigmoid(x)
    return s*(1-s)


def tanh_d(x):
    e = np.exp(2*x)
    return (e-1)/(e+1)

def relu_d(x):
    dx = np.zeros(x.shape)
    dx[x >= 0] = 1
    return dx

def gausian2D(x,y,sigma):
    return 1/(2*np.pi*np.square(sigma))*np.exp(-1*(np.square(x)+np.square(y))/(2*np.square(sigma)))

