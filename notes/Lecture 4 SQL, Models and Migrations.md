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