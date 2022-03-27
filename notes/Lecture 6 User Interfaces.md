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

## Animation

- To create an animation in CSS, we use the format below, where the animation specifics can include starting and ending styles (```to``` and ```from```) or styles at difference stages in the duration (anywhere from ```0%``` to ```100%```)

```css
@keyframes animation_name {
    from {
        /* Some styling for the start */
    }

    to {
        /* Some styling for the end */
    }
}
```

or:

```css
@keyframes animation_name {
    0% {
        /* Some styling for the start */
    }

    75% {
        /* Some styling after 3/4 of animation */
    }

    100% {
        /* Some styling for the end */
    }
}
```

- To apply an animation to an element, we include the ```animation-name```, the ```animation-duration``` (in seconds) and the ```animation-fill-mode``` (typically ```forwards```)

```html
<!-- Example of page where a title grows when we first enter the page: -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Animate</title>
        <style>
            @keyframes grow {
                from {
                    font-size: 20px;
                }
                to {
                    font-size: 100px;
                }
            }

            h1 {
                animation-name: grow;
                animation-duration: 2s;
                animation-fill-mode: forwards;
            }
        </style>
    </head>
    <body>
        <h1>Welcome!</h1>
    </body>
</html>
```

```html
<!-- Example of page where a title changes position when we first enter the page: -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Animate</title>
        <style>
            @keyframes move {
                from {
                    left: 0%;
                }
                to {
                    left: 50%;
                }
            }

            h1 {
                position: relative;
                animation-name: move;
                animation-duration: 2s;
                animation-fill-mode: forwards;
            }
        </style>
    </head>
    <body>
        <h1>Welcome!</h1>
    </body>
</html>
```

```css
/* Intermediate CSS properties; specify the style at any percentage of the way through an animation */

/* Move title from left to right and then back to left */

@keyframes move {
    0% {
        left: 0%;
    }
    50% {
        left: 50%;
    }
    100% {
        left: 0%;
    }
}
```

- If we want to repeat an animation multiple times, we can change the ```animation-iteration-count``` to a number greater than 1 (or even ```infinite``` for endless animation)

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Animate</title>
        <style>
            @keyframes move {
                0% {
                    left: 0%;
                }
                50% {
                    left: 50%;
                }
                100% {
                    left: 0%;
                }
            }

            h1 {
                position: relative;
                animation-name: move;
                animation-duration: 2s;
                animation-iteration-count: infinite;
                animation-fill-mode: forwards;
            }
        </style>
    </head>
    <body>
        <button>Click Here!</button>
        <h1>Welcome!</h1>
    </body>
</html>
```

```javascript
document.addEventListener('DOMContentLoaded', function() {

    // Find heading
    const h1 = document.querySelector('h1');

    // Pause Animation by default
    h1.style.animationPlayState = 'paused';

    // Wait for button to be clicked
    document.querySelector('button').onclick = () => {

        // If animation is currently paused, begin playing it
        if (h1.style.animationPlayState == 'paused') {
            h1.style.animationPlayState = 'running';
        }

        // Otherwise, pause the animation
        else {
            h1.style.animationPlayState = 'paused';
        }
    }
})
```

- Apply animations to posts page

```javascript
// posts/script.js

// Add a new post with given contents to DOM
function add_post(contents) {

    // Create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = `${contents} <button class="hide">Hide</button>`;

    // Add post to DOM
    document.querySelector('#posts').append(post);
};


// If hide button is clicked, delete the post
document.addEventListener('click', event => {

    // Find what was clicked on
    const element = event.target;

    // Check if the user clicked on a hide button
    if (element.className === 'hide') {
        element.parentElement.style.animationPlayState = 'running';
        element.parentElement.addEventListener('animationend', () => {
            element.parentElement.remove();
        });
    }
    
});
```

- Add animation to have the post fade away and shrink before we remove it
- Animation will spend 75% of its time changing the opacity from 1 to 0 (post fade out slowly)
- Animation will then spend the remaining 25% of its time changing its ```height```-related attributes to 0 (shrink the page to nothing)

```html
<!-- posts/index.html -->

{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <title>My Webpage</title>
        <style>
            @keyframes hide {
                0% {
                    opacity: 1;
                    height: 100%;
                    line-height: 100%;
                    padding: 20px;
                    margin-bottom: 10px;
                }
                75% {
                    opacity: 0;
                    height: 100%;
                    line-height: 100%;
                    padding: 20px;
                    margin-bottom: 10px;
                }
                100% {
                    opacity: 0;
                    height: 0px;
                    line-height: 0px;
                    padding: 0px;
                    margin-bottom: 0px;
                }
            }

            .post {
                background-color: #77dd11;
                padding: 20px;
                margin-bottom: 10px;
                animation-name: hide;
                animation-duration: 2s;
                animation-fill-mode: forwards;
                animation-play-state: paused; /* post will not be hidden by default */
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

## React

- ```Imperative Programming```: have to write code to tell the computer both _what_ and _how_ we wish to display
- ```Declarative Programming```: allows us to simply write code explaining _what_ we wish to display and not worry about _how_ we are displaying it
- Have to import these 3 JavaScript packages to use React in a HTML file:
    - ```React```
    - ```ReactDOM```
    - ```Babel```