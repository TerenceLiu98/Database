-- Database assignment Two --
-- Student Name: Terence Liu (刘骏杰) --
-- Student ID: 1630005038 --
-- Student department: Statistics --

-- create Database: BOOK_RATING_WEBSITE --
 CREATE DATABASE BOOK_RATING_WEBSITE;
USE BOOK_RATING_WEBSITE;

-- create tables --
CREATE TABLE Book (
  bID int,
  bname varchar(255),
  year  int,
  author varchar(255)
);

CREATE TABLE Reviewer (
  rID int,
  rname varchar(255)
);

CREATE TABLE Rating(
  rID int,
  bID int,
  stars int,
  rDate date
);

LOAD DATA LOCAL INFILE '~/Nutstore\ Files/Nutstore/Year\ Three\ Second\ Semester/Database/Assignment/Assignment_Two/Files/Nutstore/YeDocuments/Book.csv'
INTO TABLE Book
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE '~/Nutstore\ Files/Nutstore/Year\ Three\ Second\ Semester/Database/Assignment/Assignment_Two/Reviewer.csv'
INTO TABLE Reviewer
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '~/Nutstore\ Files/Nutstore/Year\ Three\ Second\ Semester/Database/Assignment/Assignment_Two/Rating.csv'
INTO TABLE Rating
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- CHANGE VALUES --
UPDATE  Rating SET rDate = NULL WHERE  rID = 3002 AND bID = 1006;
UPDATE  Rating SET rDate = NULL WHERE  rID = 3005 AND bID = 1008;


-- QUESTION ONE --
SELECT year FROM Book JOIN Rating ON Book.bID = Rating.bID
    WHERE Rating.stars = 2 OR Rating.stars = 3
    	ORDER BY Book.bname DESC;

-- QUESTION TWO --
SELECT rID FROM Rating JOIN Reviewer ON Reviewer.rID = Rating.rID
AND Rating.rDate = 'NULL';

-- QUESTION THREE --
SELECT DISTINCT * FROM Rating AS R1,
                       Rating AS R2, Book, Reviewer
WHERE Reviewer.rID = R1.rID AND
      Book.bID = R1.bID AND
      R1.rID = R2.rID AND
      R1.bID = R2.bID AND
      R1.stars>R2.stars AND
      R1.rDate>R2.rDate;

-- QUESTION FOUR --
-- SORTED BY NAME --
SELECT bname, AVG(stars)
FROM
     Rating AS Rating,
     Book AS Book
WHERE
      Book.bID = Rating.bID
GROUP BY
         Book.bname
ORDER BY
         bname ASC;
-- SORTED BY AVG star s --
SELECT bname, AVG(stars)
FROM
     Rating AS Rating,
     Book AS Book
WHERE Book.bID = Rating.bID
GROUP BY
         Book.bname
ORDER BY
         AVG(stars) DESC;

-- QUESTION FIVE --
SELECT rname
FROM
     Reviewer AS r1,
     Rating AS r2
WHERE
      r1.rID = r2.rID
HAVING COUNT(r1.rID) > 3;

-- QUESTION SIX --
SELECT rname, bname, AVG(stars), rDate
FROM Book, Reviewer, Rating
WHERE Book.bID = Rating.bID
AND Reviewer.rID = Rating.rID
ORDER BY rname ASC, bname ASC, AVG(stars), DESC;

-- QUESTION SEVEN --
SELECT bname, MAX(stars)
FROM Book, Rating
WHERE Book.bID = Rating.bID
GROUP BY bname;

-- QUESTION EIGHT --
SELECT DISTINCT bname, MAX(stars)-MIN(stars)
FROM Book, Rating
WHERE Book.bID = Rating.bID
GROUP BY Book.bname
HAVING MAX(stars)-MIN(stars) != 0
ORDER BY MAX(stars)-MIN(stars) DESC ,
bname ASC;
