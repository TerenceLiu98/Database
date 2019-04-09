# <center>Database Management Systems</center> 

# <center>Assignment Two</center> 

### Question 1 

A publisher named Jimmy, want to create a Chinese book rating website. And he has done some related surveys and collected data on readers of various books from douban website. The follows is the schema: 

- *Book(bID,bname,year, author)*
- *Reviewer(rID, rname)*
- *Rating(rID, bID, stars, rDate)* **stars is an integer(1 to 5)**

| bID  |            bname            | year |    author     |
| :--: | :-------------------------: | :--: | :-----------: |
| 1001 |     Journey to the West     | 1925 |   Cengen WU   |
| 1002 |         Wolf Totem          | 2004 |  Rong Jiang   |
| 1003 |      Fortress Besieged      | 1945 | Zhongshu Qian |
| 1004 |         Langya List         | 2014 |    Yan Hai    |
| 1005 |     Historical Records      | 2004 |   Sima Qian   |
| 1006 |       Ordinary World        | 1989 |    Yao Lu     |
| 1007 |        Frontier City        | 2005 | Congwen Shen  |
| 1008 | The Legend of Chu Liu Xiang | 1967 |    Long Gu    |

<center>T<b>able 1: Book</b></center>

|      |         |
| :--: | :-----: |
| rID  |  rname  |
| 3001 | Leonard |
| 3002 |  Oscar  |
| 3003 |  Spike  |
| 3004 |  Jason  |
| 3005 |  Ivan   |
| 3006 | Albert  |
| 3007 |  Carl   |
| 3008 |  Henry  |

<center><b>Table 2: Reviewer</b></center>

| rID  | bID  | stars |   rDate    |
| :--: | :--: | :---: | :--------: |
| 3001 | 1001 |   2   | 2015-05-17 |
| 3001 | 1001 |   4   | 2015-05-03 |
| 3002 | 1006 |   4   |    NULL    |
| 3003 | 1003 |   2   | 2015-05-19 |
| 3003 | 1008 |   4   | 2015-05-22 |
| 3003 | 1008 |   2   | 2015-05-06 |
| 3004 | 1001 |   3   | 2015-05-11 |
| 3005 | 1003 |   3   | 2015-05-09 |
| 3005 | 1004 |   2   | 2015-05-16 |
| 3005 | 1008 |   4   |    NULL    |
| 3006 | 1007 |   3   | 2015-05-24 |
| 3006 | 1006 |   5   | 2015-05-31 |
| 3007 | 1007 |   5   | 2015-05-12 |
| 3008 | 1004 |   5   | 2015-05-08 |

<center><b>Rating</b></center>

**Q1**: Find all years that have a book that got a rating of 2 or 3, and sort then in decreasing order

<font color = "red">**Answer**</font>

```{SQL}
SELECT year FROM Book JOIN Rating ON Book.bID = Rating.bID 
    WHERE Rating.stars = 2 OR Rating.stars = 3
    	ORDER BY Book.bname DESC;
```

**Q2**: Find the names of all reviewers who have rating with NULL value for the date. 

<font color="red">**Answer**</font>

```{SQL}
SELECT rID 
FROM Rating 
JOIN Reviewer ON Reviewer.rID = Rating.rID 
AND Rating.rDate = 'NULL';
```

**Q3**: For all cases where the same reviewer rated the same books twice and gave it a higher rating  the second time, return the reviewer's name and the name of the book. 

```{SQL}
SELECT * 
FROM Rating JOIN Reviewer
ON Reviewer.rID = Rating.rID 
(SELECT MAX(stars) FROM Reviewer); 
WHERE Reviewer.rID 
ORDER BY Reviewer.rname ASC;
```

**Q4** List book names and average ratings, from highest -rated to lowest-rated. If two or more books have the same average rating, list them in alphabetical order. 

```SQL
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
```

**Q5** Find the names of all reviewers who have contributed three or more ratings

```{SQL}
SELECT rname
FROM
     Reviewer AS r1,
     Rating AS r2
WHERE
      r1.rID = r2.rID
HAVING COUNT(r1.rID) > 3;
```

**Q6** Write a query to return the rating data in a more readable format: reviewer name. book name. stars and rating Date. Also, sort the data, first by reviewer name. then by book name, and lastly by number of stars. 

```{SQL}

SELECT rname, bname, AVG(stars), rDate 
FROM Book, Reviewer, Rating
WHERE Book.bID = Rating.bID 
AND Reviewer.rID = Rating.rID 
ORDER BY rname ASC, bname ASC, AVG(stars), DESC; 
```

**Q7** For each book that has at least one rating, find the highest number of stars that book received. Return the book name and number of stars. Sort by book name.

```{SQL}
SELECT bname, MAX(stars) 
FROM Book, Rating 
WHERE Book.bID = Rating.bID
GROUP BY bname;
```

**Q8** For each book, return the name and the ’rating spread’, that is, the difference between highest
and lowest ratings given to that book. Sort by rating spread from highest to lowest, then by book
name.

```{SQL}
SELECT DISTINCT bname, MAX(stars)-MIN(stars) 
FROM Book, Rating 
WHERE Book.bID = Rating.bID 
GROUP BY Book.bname 
HAVING MAX(stars)-MIN(stars) != 0 
ORDER BY MAX(stars)-MIN(stars) DESC ,
bname ASC;
```

