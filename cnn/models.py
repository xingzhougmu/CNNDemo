from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Document(models.Model):
	digit = models.TextField(blank=True, default = 'Failed to detect! Make sure image size is larger than 28*28')
	# imgFile = models.TextField(blank = True, default = '')
	imgFile = models.FileField(upload_to = 'uploads/')
	class Meta:
		ordering = ('digit',)
