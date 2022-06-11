# Lecture 7: Testing, CI/CD

## Testing

### Assert
- Can use ```assert``` in Python to run tests on expression
- If expression is ```True```, nothing will happen; if ```False```, an exception will be raised

```python
# correct function
def square(x):
    return x*x

assert square(10) == 100 # No output returned since expression is True

# incorrect function
def square(x):
    return x + x

assert square(10) == 100 # Assertion Error is raised
```

### Test-Driven Development (TDD)
- How this works is that each time we fix a bug, we add a test to check for that bug to a growing set of tests that are run each time changes are made.
- Ensures that new changes made do not break existing features

```python
# prime.py
from math import sqrt

# buggy function
def is_prime(n: int) -> bool:

    # Numbers < 2 are not prime
    if n < 2:
        return False

    # Checking factors up to sqrt(n)
    for i in range(2, int(sqrt(n))):

        # If i is a factor, return False
        if n % i == 0:
            return False

    # If no factors are found, return True
    return True


# correct function
def is_prime(n: int) -> bool:

    # Numbers < 2 are not prime
    if n < 2:
        return False

    # Checking factors up to sqrt(n)
    for i in range(2, int(sqrt(n)) + 1):

        # If i is a factor, return False
        if n % i == 0:
            return False

    # If no factors are found, return True
    return True
```

```python
# tests.py
from prime import is_prime

def test_prime(n, expected: bool):
    if is_prime(n) != expected:
        raise ValueError(f'Expected {expected} from is_prime({n}) but got {is_prime(n)} instead')

test_prime(5, True)
test_prime(10, False)
test_prime(25, False)
```

- We can create a ```shell script``` with ```.sh``` extension to automate our testing.
- Each of the lines below consists of
    1. A ```python3``` to specify which Python version we are running
    2. A ```-c``` to indcate that we wish to run a command
    3. A command to run in string format
- Run ```./tests.sh``` in the terminal to execute the ```shell script```

```shell
# tests.sh
python3 -c "from tests import test_prime; test_prime(1, False)"
python3 -c "from tests import test_prime; test_prime(2, True)"
python3 -c "from tests import test_prime; test_prime(8, False)"
python3 -c "from tests import test_prime; test_prime(11, True)"
python3 -c "from tests import test_prime; test_prime(25, False)"
python3 -c "from tests import test_prime; test_prime(28, False)"
```

### Unit Testing

- Name of the class methods have to begin with ```test_``` in order for the methods to be run automatically in ```unittest.main()```
- First line of each method contains a <b>docstring</b> which is displayed as a description of the test if it fails

```python
import unittest
from prime import is_prime

# Class containing all our tests
class Tests(unittest.TestCase):

    def test_1(self):
        """Check that 1 is not prime"""
        self.assertFalse(is_prime(1))

    def test_2(self):
        """Check that 2 is prime"""
        self.assertTrue(is_prime(2))

    def test_8(self):
        """Check that 8 is not prime."""
        self.assertFalse(is_prime(8))

    def test_11(self):
        """Check that 11 is prime."""
        self.assertTrue(is_prime(11))

    def test_25(self):
        """Check that 25 is not prime."""
        self.assertFalse(is_prime(25))

    def test_28(self):
        """Check that 28 is not prime."""
        self.assertFalse(is_prime(28))


if __name__ == '__main__':
    unittest.main()
```

### Django Testing

```python
# models.py

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

    def is_valid_flight(self):
        return self.origin != self.destination and self.duration > 0
```

- ```TestCase``` module from ```django.test``` is used to test our database models
- One advantage of using it is that when we run our tests, an entirely new database will be created for testing purposes only. Our actual database will not be touched

```python
# tests.py
from django.test import TestCase
from .models import Flight, Airport, Passenger

class FlightTestCase(TestCase):
    
    # setUp function is run at the start of the testing process
    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())
```

- Run the command ```python manage.py test``` to run the tests

### Client Testing

- ```Client``` object allows us to make requests to check whether our web pages load as intended

```python
from django.test import Client, TestCase
from django.db.models import Max

class FlightTestCase(TestCase):

    # Some code here

    # test index page view    
    def test_index(self):

        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("/flights/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure three flights are returned in the context
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
```

### Selenium

- Framework that allows us to simulate a user opening a web browser, navigating to our page and interacting with it

```html
<!-- counter.html -->
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Counter</title>
        <script>
            
            // Wait for page to load
            document.addEventListener('DOMContentLoaded', () => {

                // Initialize variable to 0
                let counter = 0;

                // If increase button clicked, increase counter and change inner html
                document.querySelector('#increase').onclick = () => {
                    counter ++;
                    document.querySelector('h1').innerHTML = counter;
                }

                // If decrease button clicked, decrease counter and change inner html
                document.querySelector('#decrease').onclick = () => {
                    counter --;
                    document.querySelector('h1').innerHTML = counter;
                }
            })
        </script>
    </head>
    <body>
        <h1>0</h1>
        <button id="increase">+</button>
        <button id="decrease">-</button>
    </body>
</html>
```

- Run the command ```pip install selenium chromedriver-py``` to install the required libraries

```python
# tests.py

import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path

# Finds the Uniform Resourse Identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Sets up web driver using Google chrome
service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object)

# Standard outline of testing class
class WebpageTests(unittest.TestCase):

    def test_title(self):
        """Make sure title is correct"""
        # Find the URI of our file
        uri = file_uri("counter.html")

        # Use the URI to open the web page
        driver.get(uri)

        # Access the title of the current page
        title = driver.title

        # driver.page_source allows us to access the source code of the page

        self.assertEqual(title, "Counter")

    def test_increase(self):
        """Make sure header updated to 1 after 1 click of increase button"""
        driver.get(file_uri("counter.html"))

        # Find and store increase button
        increase = driver.find_element(By.ID, "increase")

        # Simulate the user clicking on increase button
        increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "1")

    def test_decrease(self):
        """Make sure header updated to -1 after 1 click of decrease button"""
        driver.get(file_uri("counter.html"))

        # Find and store decrease button
        decrease = driver.find_element(By.ID,"decrease")

        # Simulate the user clicking on decrease button
        decrease.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "-1")

    def test_multiple_increase(self):
        """Make sure header updated to 3 after 3 clicks of increase button"""
        driver.get(file_uri("counter.html"))
        increase = driver.find_element_by_id("increase")

        # We can even include clicks within other Python constructs
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "3")

if __name__ == "__main__":
    unittest.main()
```

### CI/CD

- Stands for Continuous Integration and Continuous Delivery
- Continuous Integration
    - Frequent merges to the main branch
    - Automated unit testing with each merge

- Continuous Delivery
    - Short release schedules; new versions of an application are released frequently

### Github Actions

- Allows us to create workflows where we can specify certain actions (i.e. unit tests) to be performed every time someone pushes to a git repository
- <b>YAML</b> file (takes on the form ```filename.yml``` or ```filename.yaml```) is used to set up Gihub Action
- Refer [here](https://github.com/AddChew/github-actions.git) for a toy repository with github actions set up

#### Steps to set up Github Actions
1.  Create a ```.github``` directory in your repo
2.  Create a ```workflows``` directory inside the ```.github``` directory
3.  Within the ```workflows``` directory, create a ```filename.yml``` file

```yaml
# Sample YML file
# ci.yml

name: Testing # Name of our workflow
on: push # Specify when the workflow should run; in our case, we wish to run the workflow each time a push is made to the repo

jobs: # Indicates which jobs should be run at every push
  test_project: # Name of job that we want to run; can have multiple jobs, but in our case, we only have one. Every job must define two components: runs-on and steps.
    runs-on: ubuntu-latest # Specify which of Github's virtual machines we would like to run our code on
    steps: # Specify the actions that should occur when the job is run
    - uses: actions/checkout@v2 # Specify which Github Action we wish to use
    - name: Run Django unit tests # Description of the action that we are taking
      run: | # Commands that we wish to run on Github's server; in our case, we wish to install Django and then run the testing file
        pip3 install --user django
        python3 manage.py test
```

4. Navigate to <b>Actions</b> tab on Github to view the logs of the actions that have taken place after each push

### Docker

- Allows everyone that is working on a project to use the same environment
- Containerization software which creates an isolated environment within your computer that can be standardized among many collaborators and the server on which your application is run
- Differs from <b>Virtual Machine</b>:
    - Virtual machine: effectively an entire virtual computer with its own operating system, meaning it ends up taking a lot of space wherever it is running
    - Docker: works by setting up a container within an existing computer, therefore taking up less space

#### Steps to set up Docker
1. Create a <b>Docker File</b> named ```Dockerfile```. Inside this file, we will provide instructions on how to create a <b>Docker Image</b> which describes the libraries and binaries we wish to include in our container
2. Refer [here](https://github.com/AddChew/docker-testing.git) for a toy repository with docker set up

- For production, SQLite is almost never used as it is not scalable. To set up a separate server for our database, we can simply add another Docker container and run them together using a feature called <b>Docker Compose</b>. This feature allows two different servers to run in separate containers but also be able to communicate with one another. 

#### Steps to set up Docker Compose
1. Create a YAML file called ```docker-compose.yml```
2. Refer [here](https://github.com/AddChew/docker-compose.git) for a toy repository with docker compose set up