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
def is_prime(n: int):

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
def is_prime(n): int:

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

### Client Testing