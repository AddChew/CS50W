# Lecture 4: SQL, Models and Migrations

## SQL

### Column Types

- ```TEXT```: For strings of text
- ```NUMERIC```: For general numeric data (i.e. dates or boolean)
- ```INTEGER```: For integer data
- ```REAL```: For real number data
- ```BLOB```(Binary Large Object): For any other binary data that we might wish to store in our database (i.e. images)

### Tables
```sql
CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```