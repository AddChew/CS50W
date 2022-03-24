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

### Negation

```!``` is the negation operator in JavaScript (analogous to not operator in Python)

```javascript
flag = false

// !flag === !false === true
if (!flag){
    // do something
}
```

## Local Storage

- Allows us to store information on the user's web browser that we can access later
- Information is stored as key-value pairs
- ```localStorage.getItem(key)```: This function searches for an entry in local storage with a given key, and returns the value associated with that key
- ```localStorage.setItem(key, value)```: This function sets an entry in local storage, associating the key with a new value

```javascript
// Check if there is already a value in local storage
if (!localStorage.getItem('counter')) {

    // If not, set the counter to 0 in local storage
    localStorage.setItem('counter', 0);
}
            
function count() {
    // Retrieve counter value from local storage
    let counter = localStorage.getItem('counter');

    // update counter
    counter++;
    document.querySelector('h1').innerHTML = counter;

    // Store counter in local storage
    localStorage.setItem('counter', counter);
}

document.addEventListener('DOMContentLoaded', function() {
    // Set heading to the current value inside local storage
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    document.querySelector('button').onclick = count;
});
```

### How to access local storage in browser

Right click > Inspect > Application (Click on >> to access it) > Local Storage

## APIs

### JSON

```javascript
// Not necessary to put quotation marks for the keys
let person = {
    first : "Harry",
    last : "Potter",
}

person.first // out: "Harry"
person["first"] // out: "Harry"
```

### Currency Exchange

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Currency Exchange</title>
        <script src="currency.js"></script>
    </head>
    <body>
        <form>
            <input id="currency" placeholder="Currency" type="text">
            <input type="submit" value="Convert">
        </form>
        <div id="result"></div>
    </body>
</html>
```

```javascript
// currency.js

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = function() {

        // Send a GET request to the URL
        fetch('https://api.exchangeratesapi.io/latest?base=USD')
        // Put response into json form
        .then(response => response.json()) // The argument of then is always a function
        .then(data => {  // The argument of then is always a function
            // Get currency from user input and convert to upper case
            const currency = document.querySelector('#currency').value.toUpperCase();

            // Get rate from data
            const rate = data.rates[currency];

            // Check if currency is valid:
            if (rate !== undefined) {
                // Display exchange on the screen
                document.querySelector('#result').innerHTML = `1 USD is equal to ${rate.toFixed(3)} ${currency}.`;
            }
            else {
                // Display error on the screen
                document.querySelector('#result').innerHTML = 'Invalid Currency.';
            }
        })
        // Catch any errors and log them to the console
        .catch(error => {
            console.log('Error:', error);
        });
        // Prevent default submission
        return false;
    }
});
```