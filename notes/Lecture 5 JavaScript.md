# Lecture 5: JavaScript

### Equality

- ```===``` enforces strict equality, two objects are considered equal if and only if they have the same values and types

- ```==``` enforces weaker equality, two objects are considered equal if they have the same values

### Autofocus

Indicates that the cursor should be set inside the specified input as soon as the page is loaded.

```html
<!-- Cursor will be set inside this text input field once the page is loaded -->
<input autofocus id="name" placeholder="Name" type="text">
```

### Data Attributes
```data-SOMETHING``` attribute is used to assign data to a HTML element.This data can be accessed in JavaScript using the element's ```dataset``` property.

```html
<!DOCTYPE html>
<html lang="en">
<head>
     <title>Colors</title>
     <script>
         document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('button').forEach(function(button) {
                button.onclick = function() {
                    document.querySelector("#hello").style.color = button.dataset.color; // Access data-color attribute of buttons
                }
            });
         });
     </script>
</head>
<body>
    <h1 id="hello">Hello</h1>
    <!-- Set data-color attribute of buttons -->
    <button data-color="red">Red</button> 
    <button data-color="blue">Blue</button>
    <button data-color="green">Green</button>
</body>
</html>
```

### This
In JavaScript, ```this``` is a keyword that changes based on the context in which it is used. In the case of event handler, ```this``` refers to the object that triggered the event.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Colors</title>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                document.querySelector('select').onchange = function() {
                    document.querySelector('#hello').style.color = this.value; // this here refers to document.querySelector('select') element
                }
            });
        </script>
    </head>
    <body>
        <h1 id="hello">Hello</h1>
        <select>
            <option value="black">Black</option>
            <option value="red">Red</option>
            <option value="blue">Blue</option>
            <option value="green">Green</option>
        </select>

    </body>
</html>
```

### Other Events

- ```onclick```
- ```onmouseover```
- ```onkeydown```
- ```onkeyup```
- ```onload```
- ```onblur```
- ...

### TODO List

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Tasks</title>
        <script src="tasks.js"></script>
    </head>
    <body>
        <h1>Tasks</h1>
        <ul id="tasks"></ul>
        <form>
            <input id="task" placeholder = "New Task" type="text">
            <input id="submit" type="submit">
        </form>
    </body>
</html>
```

```javascript
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Select the submit button and input to be used later
    const submit = document.querySelector('#submit');
    const newTask = document.querySelector('#task');

    // Disable submit button by default:
    submit.disabled = true;

    // Listen for input to be typed into the input field
    newTask.onkeyup = () => {
        if (newTask.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    // Listen for submission of form
    document.querySelector('form').onsubmit = () => {

        // Find the task the user just submitted
        const task = newTask.value;

        // Create a list item for the new task and add the task to it
        const li = document.createElement('li');
        li.innerHTML = task;

        // Add new element to our unordered list:
        document.querySelector('#tasks').append(li);

        // Clear out input field:
        newTask.value = '';

        // Disable the submit button again:
        submit.disabled = true;

        // Stop form from submitting
        return false;
    }
});
```

Notes:
- Can enable or disable a button by setting its ```disabled``` attribute to ```false```/```true```
- In JavaScript, we use ```.length``` to find the length of objects such as strings and arrays
- We add ```return false``` at the end of the script to prevent the default submission of the form which involves either reloading the current page or redirecting to a new one
- We can create HTML elements using ```createElement``` function. This elements can be added to the DOM using ```append``` function

### Intervals

```javascript
let counter = 0;
            
function count() {
    counter++;
    document.querySelector('h1').innerHTML = counter;
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').onclick = count;

    setInterval(count, 1000); // Set counter to increment every second; setInterval function takes as arguments a function to be run and a time (in milliseconds) between function runs
});
```

## Local Storage

## APIs

### JSON

### Currency Exchange