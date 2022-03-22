# Lecture 6: User Interfaces

## Single Page Applications

```python
# urls.py

urlpatterns = [
    path("", views.index, name="index"),
    path("sections/<int:num>", views.section, name="section")
]
```

```python
# views.py

from django.http import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")

# The texts are much longer in reality, but have
# been shortened here to save space
texts = ["Text 1", "Text 2", "Text 3"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("No such section")
```

```html
<!-- index.html -->

{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Single Page</title>
        <style>
        </style>
        <script src="{% static 'singlepage/singlepage.js' %}"></script>
    </head>
    <body>
        <h1>Hello!</h1>
        <button data-section="1">Section 1</button>
        <button data-section="2">Section 2</button>
        <button data-section="3">Section 3</button>
        <div id="content">
        </div>
    </body>
</html>
```

### JavaScript History API

- Allows us to push information into our browser history and update the URL manually
- ```history.pushState``` function:
    Adds a new element to our browsing history based on 3 arguments
    1. Any data associated with the state
    2. A title parameter ignored by most browsers
    3. What should be displayed in the URL

```javascript
// singlepage.js

// When back arrow is clicked, show previous section
window.onpopstate = event => {
    console.log(event.state.section)
    showSection(event.state.section)
}

// Shows given section
let showSection = section => {
    
    // Find section text from server
    fetch(`/sections/${section}`)
    .then(response => response.text())
    .then(text => {
        // Log text and display on page
        console.log(text);
        document.querySelector('#content').innerHTML = text
    })
}

document.addEventListener('DOMContentLoaded', () => {
    // Add button functionality
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            const section = this.dataset.section

            // Add the current state to the history
            history.pushState({section: section}, "", `section${section}`)
            showSection(section)
        }
    })
})
```