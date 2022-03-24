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

Allows us to push information into our browser history and update the URL manually

#### history.pushState
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
        console.log(text)
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

## Scroll

### window

- Represents what is currently visible to the user
- ```window.innerWidth```: width of the window in pixels
- ```window.innerHeight```: height of window in pixels
- ```window.scrollY```: how many pixels we have scrolled from the top of the page
- ```document.body.offsetHeight```: height of the entire document in pixels
- Can use ```window.scrollY + window.innerHeight >= document.body.offsetHeight``` to determine if a user has scrolled to the end of the page

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Scroll</title>
        <script>

            // Event listener for scrolling
            window.onscroll = () => {
                // Check if we're at the bottom
                if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {

                    // Change color to green
                    document.querySelector('body').style.background = 'green'
                } else {

                    // Change color to white
                    document.querySelector('body').style.background = 'white'
                }
            }

        </script>
    </head>
    <body>
        <p>1</p>
        <p>2</p>
        <!-- More paragraphs left out to save space -->
        <p>99</p>
        <p>100</p>
    </body>
</html>
```

### Infinite Scroll

```python
# urls.py

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.posts, name="posts")
]
```

```python
# views.py

import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "posts/index.html")

def posts(request):

    # Get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    # Generate list of posts
    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    # Artificially delay speed of response
    time.sleep(1)

    # Return list of posts
    return JsonResponse({
        "posts": data
    })
```

- ```posts``` view takes in two arguments, start and end
- Can test out the API by visiting ```localhost:8000/posts?start=10&end=15``` which returns the following JSON:
```python
{
    "posts": [
        "Post #10",
        "Post #11", 
        "Post #12", 
        "Post #13", 
        "Post #14", 
        "Post #15"
    ]
}
```

```html
<!-- posts/index.html -->

{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <title>My Webpage</title>
        <style>
            .post {
                background-color: #77dd11;
                padding: 20px;
                margin: 10px;
            }

            body {
                padding-bottom: 50px;
            }
        </style>
        <script src="{% static 'posts/script.js' %}"></script>
    </head>
    <body>
        <div id="posts">
        </div>
    </body>
</html>
```

```javascript
// posts/script.js

// Start with first post
let counter = 1

// Load posts 20 at a time
const quantity = 20

// When DOM loads, render the first 20 posts
document.addEventListener('DOMContentLoaded', load)

// If scrolled to bottom, load the next 20 posts
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load()
    }
}

// Load next set of posts
function load() {

    // Set start and end post numbers, and update counter
    const start = counter
    const end = start + quantity - 1
    counter = end + 1

    // Get new posts and add posts
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post)
    })
}

// Add a new post with given contents to DOM
function add_post(contents) {

    // Create new post
    const post = document.createElement('div')
    post.className = 'post'
    post.innerHTML = contents

    // Add post to DOM
    document.querySelector('#posts').append(post)
}
```