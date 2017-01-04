from __future__ import print_function

import sys
import os
import time
import pickle

import numpy as np
import theano
import theano.tensor as T

import lasagne

def load_dataset(sample_data, sample_label):
	if sys.version_info[0] == 2:
		from urllib import urlretrieve
	else:
		from urllib.request import urlretrieve
	
	def download(filename, source='http://yann.lecun.com/exdb/mnist'):
		print("Downloading %s" % filename)
		urlretrieve(source + filename, filename)
	
	import gzip
	
	def load_test_images(filename):
		if not os.path.exists(filename):
			download(filename)
		with gzip.open(filename, 'rb') as f:
			data = np.frombuffer(f.read(), np.uint8, offset=16)
		
		data = data.reshape(-1,1,28,28)

		return data / np.float32(256)

	def load_test_labels(filename):
		if not os.path.exists(filename):
			download(filename)

		with gzip.open(filename, 'rb') as f:
                        data = np.frombuffer(f.read(), np.uint8, offset=8)
		return data

	X_test = load_test_images(sample_data)
	y_test = load_test_labels(sample_label)

	return X_test, y_test

def predict_label(sample, model='model.npz'):
	input_var = T.tensor4('sample')

        network = build_mlp(input_var)

	with np.load(model) as f:
		param_values = [f['arr_%d'%i] for i in range(len(f.files))]

	lasagne.layers.set_all_param_values(network, param_values)
	
	prediction = lasagne.layers.get_output(network, deterministic=True)

	result = T.argmax(prediction, axis=1)
	predict_fn = theano.function([input_var],result)

	return predict_fn(sample)

# ##################### Build the neural network model #######################
# This script supports three types of models. For each one, we define a
# function that takes a Theano variable representing the input and returns
# the output layer of a neural network model built in Lasagne.

def build_mlp(input_var=None):
    # This creates an MLP of two hidden layers of 800 units each, followed by
    # a softmax output layer of 10 units. It applies 20% dropout to the input
    # data and 50% dropout to the hidden layers.

    # Input layer, specifying the expected input shape of the network
    # (unspecified batchsize, 1 channel, 28 rows and 28 columns) and
    # linking it to the given Theano variable `input_var`, if any:
    l_in = lasagne.layers.InputLayer(shape=(None, 1, 28, 28),
                                     input_var=input_var)

    # Apply 20% dropout to the input data:
    l_in_drop = lasagne.layers.DropoutLayer(l_in, p=0.2)

    # Add a fully-connected layer of 800 units, using the linear rectifier, and
    # initializing weights with Glorot's scheme (which is the default anyway):
    l_hid1 = lasagne.layers.DenseLayer(
            l_in_drop, num_units=800,
            nonlinearity=lasagne.nonlinearities.rectify,
            W=lasagne.init.GlorotUniform())

    # We'll now add dropout of 50%:
    l_hid1_drop = lasagne.layers.DropoutLayer(l_hid1, p=0.5)

    # Another 800-unit layer:
    l_hid2 = lasagne.layers.DenseLayer(
            l_hid1_drop, num_units=800,
            nonlinearity=lasagne.nonlinearities.rectify)

    # 50% dropout again:
    l_hid2_drop = lasagne.layers.DropoutLayer(l_hid2, p=0.5)

    # Finally, we'll add the fully-connected output layer, of 10 softmax units:
    l_out = lasagne.layers.DenseLayer(
            l_hid2_drop, num_units=10,
            nonlinearity=lasagne.nonlinearities.softmax)

    # Each layer is linked to its incoming layer(s), so we only need to pass
    # the output layer to give access to a network in Lasagne:
    return l_out


def build_custom_mlp(input_var=None, depth=2, width=800, drop_input=.2,
                     drop_hidden=.5):
    # By default, this creates the same network as `build_mlp`, but it can be
    # customized with respect to the number and size of hidden layers. This
    # mostly showcases how creating a network in Python code can be a lot more
    # flexible than a configuration file. Note that to make the code easier,
    # all the layers are just called `network` -- there is no need to give them
    # different names if all we return is the last one we created anyway; we
    # just used different names above for clarity.

    # Input layer and dropout (with shortcut `dropout` for `DropoutLayer`):
    network = lasagne.layers.InputLayer(shape=(None, 1, 28, 28),
                                        input_var=input_var)
    if drop_input:
        network = lasagne.layers.dropout(network, p=drop_input)
    # Hidden layers and dropout:
    nonlin = lasagne.nonlinearities.rectify
    for _ in range(depth):
        network = lasagne.layers.DenseLayer(
                network, width, nonlinearity=nonlin)
        if drop_hidden:
            network = lasagne.layers.dropout(network, p=drop_hidden)
    # Output layer:
    softmax = lasagne.nonlinearities.softmax
    network = lasagne.layers.DenseLayer(network, 10, nonlinearity=softmax)
    return network


def build_cnn(input_var=None):
    # As a third model, we'll create a CNN of two convolution + pooling stages
    # and a fully-connected hidden layer in front of the output layer.

    # Input layer, as usual:
    network = lasagne.layers.InputLayer(shape=(None, 1, 28, 28),
                                        input_var=input_var)
    # This time we do not apply input dropout, as it tends to work less well
    # for convolutional layers.

    # Convolutional layer with 32 kernels of size 5x5. Strided and padded
    # convolutions are supported as well; see the docstring.
    network = lasagne.layers.Conv2DLayer(
            network, num_filters=32, filter_size=(5, 5),
            nonlinearity=lasagne.nonlinearities.rectify,
            W=lasagne.init.GlorotUniform())
    # Expert note: Lasagne provides alternative convolutional layers that
    # override Theano's choice of which implementation to use; for details
    # please see http://lasagne.readthedocs.org/en/latest/user/tutorial.html.

    # Max-pooling layer of factor 2 in both dimensions:
    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2, 2))

    # Another convolution with 32 5x5 kernels, and another 2x2 pooling:
    network = lasagne.layers.Conv2DLayer(
            network, num_filters=32, filter_size=(5, 5),
            nonlinearity=lasagne.nonlinearities.rectify)
    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2, 2))

    # A fully-connected layer of 256 units with 50% dropout on its inputs:
    network = lasagne.layers.DenseLayer(
            lasagne.layers.dropout(network, p=.5),
            num_units=256,
            nonlinearity=lasagne.nonlinearities.rectify)

    # And, finally, the 10-unit output layer with 50% dropout on its inputs:
    network = lasagne.layers.DenseLayer(
            lasagne.layers.dropout(network, p=.5),
            num_units=10,
            nonlinearity=lasagne.nonlinearities.softmax)

    return network

def main(model='mlp'):
	# load the test dataset
	print("Loading data...")
	
	sample_data = 't10k-images-idx3-ubyte.gz'
	sample_label = 't10k-labels-idx1-ubyte.gz'
	X_test, y_test = load_dataset(sample_data, sample_label)
	
	# print("build model ...")
	# network = build_mlp()	

	print("Evaluating ...")
	label = predict_label(X_test)
	
	# with open("predict_label.txt","w") as text_file:
	#	print(label, file = text_file)

	# with open("groundtruth_label.txt","w") as text_file:
        #        print(y_test, file = text_file)
	
	print("Saving result ...")
	out_predict = open('predict.pkl', 'w')
	pickle.dump(label, out_predict)
	
	thefile = open('predict.txt','w')
	for item in label:
		thefile.write('%s\n' % item)

	out_groundtruth = open('groundtruth.pkl', 'w')
	pickle.dump(y_test, out_groundtruth)

if __name__ == '__main__':
	print("This script will predict the lables based on the models leared via CNN, MLP")
	print("Reference: https://lasagne.readthedocs.io/en/latest/user/tutorial.html#run-the-mnist-example")
	
	kwargs = {}
	if len(sys.argv) > 1:
		kwargs['model'] = sys.argv[1]
	
	main(**kwargs)
