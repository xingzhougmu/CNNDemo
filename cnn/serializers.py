from rest_framework import serializers
from cnn.models import Document

class CNNSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('digit','imgFile')
