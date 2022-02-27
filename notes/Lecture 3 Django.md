# Lecture 3: Django

### Command to start a new django project
```
django-admin startproject <project name>
```

### Command to launch VS Code
```
code
```

### Command to start django project server
```
python manage.py runserver
```

### Command to create a new app in project
```
python manage.py startapp <app name>
```
- Navigate to settings.py and add \<app name> to INSTALLED_APPS to install the app

### Code snippet on how to associate function with url
- Create a urls.py file in our app directory; same level as views.py
```python
# urls.py

from django.urls import path
from . import views # . means same level in directory

urlpatterns = [
    path("", views.index, name = "index"), # path(<url_path>, <view_function>, <url name>)
]
```