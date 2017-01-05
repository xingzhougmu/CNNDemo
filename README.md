# CNNDemo: Handwritten Digits Recognition
This demo is showing how to recognize handwritten digits via Convolutional Nueral Network(CNN) model.
## The whole framework consists of:
1. Host Server: Ubuntu VM hosted on [Microsoft Azure](https://azure.microsoft.com/)
1. Web Server Framework: [Django 1.10](https://www.djangoproject.com/)
1. Neural Network framework: [Lasagne and Theano](https://lasagne.readthedocs.io/)
1. Working Dataset: [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
1. Programming Language: [Python](https://www.python.org/)

## How the recognition works?
1. Train the model offline
  - This model contains two convoluton and two pooling layers, a fully-connected hidden layer and a fully-connected output layer.
  - The convolution layer contains 32 filters of size 5x5.
  - Max-pooling layer takes factor 2.
1. Load pre-trained mode online to recognize the digit within the uploaded image

## Discussion:
The trained model is quite sensitive to the training data set.
- The training dataset's background is black. If the test sample is with white background, the test result is bad.
- The prediction rate also depends on the thickness of the handwritten digits.
This is another example where the learned model cannot be easily applied to other scenarios. In other words, it is difficult to come up with a generic model.

## Reference:
1. [CS231n Convolutional Neural Networks for Visual Recognition](http://cs231n.github.io/)
1. [Lasagne MNIST Example](https://lasagne.readthedocs.io/en/latest/user/tutorial.html#run-the-mnist-example)
1. [Django REST Framework](http://django-rest-framework.org/tutorial/quickstart/)

<p align="center">
<img src="cnn/static/lasagne.jpg" alt="Lasagne" height="100"/>
<img src="cnn/static/theano.png"  alt="Theano" height="100"/>
</p>
<p align="center">
<img src="cnn/static/Azure.png" alt="Microsoft Azure" height="100"/>
<img src="cnn/static/django.png" alt="Django" height="100"/>
<img src="cnn/static/python.jpeg"  alt="Python" height="100"/>
</p>
