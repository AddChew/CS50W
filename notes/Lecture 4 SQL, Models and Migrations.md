# Lecture 4: SQL, Models and Migrations

## SQL

### SQLite Data Types

- ```TEXT```: For strings of text
- ```NUMERIC```: For generic numeric data (i.e. dates or boolean)
- ```INTEGER```: For integer data
- ```REAL```: For real number data
- ```BLOB```(Binary Large Object): For any other binary data that we might wish to store in our database (i.e. images and audio files)

### Tables

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

#### Other constraints

- ```CHECK```: Makes sure certain constraints are met before allowing a row to be added/modified
- ```DEFAULT```: Provides a default value if no value is given
- ```UNIQUE```: Ensures that no two rows have the same value in that column

```sql
-- Sample code snippet on how to insert into a table with SQL
-- INSERT INTO <table name> (<field1>, ...) VALUES (<field1 value>, ...);

INSERT INTO flights
    (origin, destination, duration)
    VALUES ("New York", "London", 415); -- Must make sure that the VALUES come in the same order as the corresponding list of columns
```