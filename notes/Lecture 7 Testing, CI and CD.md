# Lecture 7: Testing, CI/CD

## Testing

### Assert
- Can use ```assert``` in Python to run tests on expression
- If expression is ```True```, nothing will happen; if ```False```, an exception will be raised

```python
# Correct Function
def square(x):
    return x*x

assert square(10) == 100 # No output returned since expression is True

# Incorrect Function
def square(x):
    return x + x

assert square(10) == 100 # Assertion Error is raised
```

### Test-Driven Development