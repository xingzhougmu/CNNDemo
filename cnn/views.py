# from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cnn.models import Document
from cnn.serializers import CNNSerializer
from cnn.forms import UploadForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings

from predict import predict_label, build_mlp, build_custom_mlp, build_cnn
from scipy.misc import imread, imresize
import numpy as np

# Create your views here.
# @api_view(['POST', 'GET'])
def digit_recog(request):
	"""
	Recognize the digit number in the image sent in request body
	"""
	"""
	if request.method == 'GET':
		test_sample = request.data
		# label = predict_label(test_sample)
		label = "9"
		serializer = CNNSerializer(CNN(digit=label))
		return Response(serializer.data)
	"""

	if request.method == 'POST':
		"""
		serializer = CNNSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.erros, status = status.HTTP_400_BAD_REQUEST)
		"""

		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			Document.objects.all().delete()
			newdoc = Document(imgFile=request.FILES['imgFile'])
			newdoc.save()
			# CNN Digit Recognition happens here
			imgFullPath = '%s/%s' % (settings.MEDIA_ROOT, newdoc.imgFile.name)
			imgData = imread(imgFullPath, 'L')
				
			# validate image size
			if min(imgData.shape) >= 28:
				imgData = imresize(imgData, (28,28))
				# predict_lable's arg: (1,1,28,28)
				inputData = np.zeros((1,1,28,28))
				inputData[0,0,:,:] = imgData
				predict_result = predict_label(inputData)
				newdoc.digit = predict_result
				newdoc.save()
			
			# imData = imread(Documents.objects.filter(imgFile.name=newdoc.imgFile.name).imgFile.url)

			# redirect to the document list after POST
			return HttpResponseRedirect(reverse('DigitRecognition'))
	else:
		form = UploadForm() # A empty, unbound form
		# clear the DB
        	# Document.objects.all().delete()

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render(
		request,
		'list.html',
		{'documents': documents, 'form': form}
		# context_instance=RequestContext(request)
	)
