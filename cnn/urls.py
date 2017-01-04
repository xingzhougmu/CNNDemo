from django.conf.urls import url
from cnn import views
from cnn.views import digit_recog

urlpatterns = [
	url(r'^digit_recog/$', digit_recog, name='DigitRecognition'),
]
