# Lecture 4: SQL, Models and Migrations

## SQL

### SQLite Data Types

- ```TEXT```: For strings of text
- ```NUMERIC```: For generic numeric data (i.e. dates or boolean)
- ```INTEGER```: For integer data
- ```REAL```: For real number data
- ```BLOB```(Binary Large Object): For any other binary data that we might wish to store in our database (i.e. images and audio files)

### CREATE

```sql
-- Sample code snippet on how to create a new table with SQL
-- CREATE TABLE <table name>(<field1> <field1 type> <field1 contraints>, ...);

CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- AUTOINCREMENT: Do not need to provide an id each time we add to the table; this is done automatically
    origin TEXT NOT NULL, -- NOT NULL: Field cannot be empty; it must have a value
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```

### Constraints

- ```CHECK```: Makes sure certain constraints are met before allowing a row to be added/modified
- ```DEFAULT```: Provides a default value if no value is given
- ```UNIQUE```: Ensures that no two rows have the same value in that column

### INSERT
```sql
-- Sample code snippet on how to insert into a table with SQL
-- INSERT INTO <table name> (<field1>, ...) VALUES (<field1 value>, ...);

INSERT INTO flights
    (origin, destination, duration)
    VALUES ("New York", "London", 415); -- Must make sure that the VALUES come in the same order as the corresponding list of columns
```

### SELECT

```sql
-- Sample code snippet on the use of 'IN' keyword
-- 'IN' keyword allows you to filter for entries where field value is in list

SELECT * FROM flights WHERE origin IN ("New York", "Lima");
```

```sql
-- Sample code snippet on the use of 'LIKE' keyword
-- 'LIKE' keyword, when combined with regular expressions allows you to search for words more broadly
-- '%' represents a wildcard character, i.e. 0 or more characters

SELECT * FROM flights WHERE origin LIKE "%a%";
```

### Functions

- AVERAGE
- COUNT
- MAX
- MIN
- SUM
- ...

### Update

```sql
-- Sample code snippet on how to update data rows in table
-- UPDATE <table name> SET <field> = <value> WHERE <condition1, condition2, ...>;

UPDATE flights
    SET duration = 430
    WHERE origin = "New York"
    AND destination = "London";
```

### DELETE

```sql
-- Sample code snippet on how to delete data rows in table
-- DELETE FROM <table name> WHERE <condition1, condition2, ...>;

DELETE FROM flights WHERE destination = "Tokyo";
```

### Clauses

- ```LIMIT```: Limits the number of results returned by query
- ```ORDER BY```: Order results based on specific column(s)
- ```GROUP BY```: Group results by specific column(s)
- ```HAVING```: Add additional constraints on results

### JOIN

```sql
-- Sample code snippet on how to join tables
-- SELECT <field1>, <field2>... FROM <table1> JOIN <table2> ON <table 1.field1> = <table2.field2>;
-- Other types of joins: INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN

SELECT first, origin, destination
FROM flights JOIN passengers
ON passengers.flight_id = flights.id;
```

### Indexing

- Allows you to speed up your queries

```sql
-- Sample code snippet on the creation of index
-- CREATE INDEX <index name> ON <table name> (<field name>);

CREATE INDEX name_index ON passengers (last);
```

## Django Models

### Database Models

```python
# models.py in app directory
# Sample code snippet on how to define database models

from django.db import models

class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

    # Method provides instructions on how to show a Flight object as a string
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```

### Migrations

- Terminal command to create Python files that will create or edit our database to be able to store what we have in our models
```
python manage.py makemigrations
```

- Terminal command to apply migrations to database
```
python manage.py migrate
```

### Shell

- Terminal command to enter Django shell
```
python manage.py shell
```

```python
# Sample code snippets on the use of ORM models

from flights.models import Flight

# Create a new flight
f = Flight(origin = "New York", destination = "London", duration = 415)

# Insert flight into database
f.save()

# Query for all flights stored in database and stored it into a variable
flights = Flight.objects.all()
flights
# Out: <QuerySet [<Flight: 1: New York to London>]>

# Find just the first flight
flight = flights.first()
flight
# Out: <Flight: 1: New York to London>

# Display flight id
flight.id
# Out: 1

# Display flight origin
flight.origin
# Out: "New York"

# Display flight destination
flight.destination
# Out: "London"

# Display flight duration
flight.duration
# Out: 415
```

### Normalize Database Models

```python
# models.py in app directory

from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    # What related_name does is that it provides a way for us to search for all flights with a given airport as their origin or departure
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```

- Each time changes are made to models.py, we have to make migrations and then migrate

```
python manage.py makemigrations
```

```
python manage.py migrate
```

```python
# Sample code snippets on the use of ORM models

from flights.models import *

# Create new airports
jfk = Airport(code="JFK", city="New York")
lhr = Airport(code="LHR", city="London")
cdg = Airport(code="CDG", city="Paris")
nrt = Airport(code="NRT", city="Tokyo")

# Save airports to database
jfk.save()
lhr.save()
cdg.save()
nrt.save()

# Add flight and save to database
f = Flight(origin=jfk, destination=lhr, duration=414)
f.save()

# Display some info about flight
f
# Out: <Flight: 1: New York (JFK) to London (LHR)>
f.origin
# Out: <Airport: New York (JFK)>

# Use related name to query by airport of arrival
lhr.arrivals.all()
# Out: <QuerySet [<Flight: 1: New York (JFK) to London (LHR)>]>
```

### Start our application

```python
# urls.py in app directory

urlpatterns = [
    path('', views.index, name="index"),
]
```

```python
# views.py in app directory

from django.shortcuts import render
from .models import Flight, Airport

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })
```

```html
<!-- layout.html -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Flights</title>
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
```

```html
<!-- index.html -->

{% extends "flights/layout.html" %}

{% block body %}
    <h1>Flights:</h1>
    <ul>
        {% for flight in flights %}
            <li>Flight {{ flight.id }}: {{ flight.origin }} to {{ flight.destination }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

```python
# Sample code snippets on the use of ORM models

# Use filter command to find all airports based in New York
Airport.objects.filter(city="New York")
# Out: <QuerySet [<Airport: New York (JFK)>]>

# Use get command to get only one airport in New York
Airport.objects.get(city="New York")
# Out: <Airport: New York (JFK)>

# Assign airports to variables
jfk = Airport.objects.get(city="New York")
cdg = Airport.objects.get(city="Paris")

# Create and save a new flight
f = Flight(origin=jfk, destination=cdg, duration=435)
f.save()
```

## Django Admin