# Lecture 3: Django

## Django 

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

## Routes

### Code snippet on how to associate function with app url
1. Create a urls.py file in our app directory; same level as views.py

```python
# urls.py in app directory

from django.urls import path
from . import views # . means same level in directory

urlpatterns = [
    path("", views.index, name = "index"), # path(<url_path>, <view_function>, <url name>)
]
```

2. Edit urls.py file in main project directory

```python
# urls.py in main project directory

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include("hello.urls")), # path("<app_name>/", include("<app name>.urls"))
]
```