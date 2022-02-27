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

### Link views function to app url

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

### Flexible Routes (based on url arguments)

```python
# views.py in app directory

from django.http import HttpResponse

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")
```

```python
# urls.py in app directory

path("<str:name>", views.greet, name = "greet")
```

## Templates

1. Create a templates folder in app directory
2. Within the templates folder, create a \<app name> folder
3. Put template html files in \<app name> folder within templates folder

```python
# views.py in app directory

from django.shortcuts import render

def index(request):
    return render(request, "hello/index.html") # render(request, "<app name>/<html template file>")
```

### Django Templating Language

- Context (third argument in render) allows you to pass information to your HTML template files
```python
# views.py in app directory

from django.shortcuts import render

def greet(request, name):
    return render(request, "hello/index.html", {"name": name.capitalize()}) # {"<variable name>": <value>}
    # render(request, "<app name>/<html template file>", <context:Dict>)
```

```html
<!-- hello/index.html in templates directory -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello, {{ name }}!</h1>
    </body>
</html>
```

### Conditionals

- ```{%``` and ```%}``` are used as opening and closing tags around logical statements in django templating language.

```html
<!-- Code snippet on the use of if else in django templating language-->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Is it New Year's?</title>
    </head>
    <body>
        {% if newyear %}
            <h1>YES</h1>
        {% else %}
            <h1>NO</h1>
        {% endif %}
    </body>
</html>
```