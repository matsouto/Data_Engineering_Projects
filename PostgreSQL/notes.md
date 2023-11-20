# Notes taken during PostgreSQL course

## Commands in SQL:

### Create a table command:
CREATE TABLE tablename (
  id SERIAL,
  att1 VARCHAR(128) UNIQUE,  -- The number is the size of the variable
  att2 INTEGER,
  PRIMARY KEY(id)
);

### Insert values do a table:
INSERT INTO tablename (att1, att2) VALUES ('value1', value2);

### Deleting a row:
DELETE FROM tablename WHERE att1='blabla';

### Updating:
UPDATE tablename SET att1='blabla' WHERE att2=1;

### Retrieve:
SELECT * FROM tablename WHERE att1='blabla';
SELECT * FROM tablename ORDER BY att1;
SELECT * FROM tablename WHERE att1 LIKE '%e%'; -- Wildcard

### LIMIT/OFFSET:
SELECT * FROM tablename ORDER BY att1 DESC LIMIT 2; -- First page of 2 items
SELECT * FROM tablename ORDER BY att1 OFFSET 1 LIMIT 2; -- Next page

### Counting:
SELECT COUNT(*) FROM tablename WHERE att1='blabla';

## Data Types in SQL:

### String Fields:
CHAR(n) -- For when length is known, alocates the entire space
VARRCHAR(n) -- Alocates a variable amount of space, depending on the data length
TEXT -- Varying length, paragraphs, html pages, etc... NOT generally used for indexing (WHERE, ORDER BY)

## Graded Apps:

### Music dataset
wget https://www.pg4e.com/tools/sql/library.csv

CREATE TABLE track_raw
 (title TEXT, artist TEXT, album TEXT,
  count INTEGER, rating INTEGER, len INTEGER);

\copy track_raw(title,artist,album,count,rating,len) FROM 'library.csv' WITH DELIMITER ',' CSV;

SELECT title, album FROM track_raw ORDER BY title LIMIT 3;

### Get table data:
\d table_name -- PostgreSQL

-- Or using SQL:
select column_name, data_type, character_maximum_length
    from INFORMATION_SCHEMA.COLUMNS 
    where table_name = 'table_name';
