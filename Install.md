# Installation Instructions:
The instructions shown below is illustrating how to run the demo in an Azure Linux Virtual Machine.

1. Create an Azure Linux VM. You need an Azure subscription to achieve this. Not have one? You can start with a [free one][3].
2. Remote to Azure VM - Putty
2. Add local repository to git reprository. About how to, please check [this link][2].
3. Python 2.7.12 is coming out of box with Ubuntu 16.04LTS
4. Create a virtual env for all the stuff:
  1. sudo apt install virtualenv
  2. virtualenv cnn-django  
  Life is tough. You cannot simply achieve all at a time.
  ```
  Error encountered:
		ReadTimeoutError: HTTPSConnectionPool(host='pypi.python.org', port=443): Read timed out.
		OSError: Command /home/xingzhou/cnn-django/bin/python2 - setuptools pkg_resources pip wheel failed with error code 2
  ```
	You can check [this link][1] for more on this issue. I simpliy switch from Azure China to Azure Global to avoid network issue. 
	3. source cnn-django/bin/activate
5. Install Django
6. install Lasagne
	Prerequisite:
		a. pip install numpy
		b. pip install scipy
	pip install -r https://raw.githubusercontent.com/Lasagne/Lasagne/v0.1/requirements.txt
	
7. create django project: django-admin.py startproject cnntutorial
8. create django app: python manage.py startapp cnn
9. Migrate APP files from test server to production
10. Sync DB
		a. python manage.py makemigrations cnn
		b. python manage.py migrate
11. When running "python manage.py runserver", received a warning:

  ```
  g++ not detected theano will be unable to execute optimized c-implementations
	```
	sudo apt-get install g++
	However, encounter another compilation error.	
	Need to install: [python-dev][6]
12. Then all set. However, I cannot access the web app via internet. Because the webapp is running on 127.0.0.1, which will not accept internet request.
  
  For details check [this page][5]. I run the following code to start the web server.
  ```python
  python manager.py runserver 0.0.0.0:8000
  ```  
13. Still have **allowed_host** issue
Edit [settings.py][4] to allow all hosts although it will put you in risk.
  
  
[1]: http://m.blog.csdn.net/article/details?id=51775896
[2]: https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/
[3]: https://azure.microsoft.com/en-us/free/
[4]: /cnntutorial/settings.py
[5]: https://docs.djangoproject.com/en/1.10/ref/django-admin/
[6]: http://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory
