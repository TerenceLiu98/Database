# <center>Database Lecture One</center> 

<center><I>15-445/645 Intro to Database Systems (Fall 2018)</I></center>

**DATABASE** is 

* Organized collection of inter-related data that models some aspect of the real-world
* Databases are core the component of most computer applications 
* 

**EARLY DBMS**

* Database applications were difficult to build and maintain 

* Tight coupling between logical and physical layers
* You have to (roughly) know what queires your app would execute before you deployed the database 

**DATA MODELS**

* a <u>data model</u> is collection of concepts for describing the data in a database 
* a <u>schema</u> is a description of a particular coolection of data, using a given data model

Most DBMs: Relational

NoSQL: Key/Value; Graph, Document, Column-family

Machine Learning: Array / Matrix 

Obsolete: Hierarchical, Network

### RELATIONAL MODEL 

* Structure: The definition of relations and their contents;
* Integrity: Ensure the database's contents satisfy constraints 
* Manipulation: how to access and model database's contents

A <u>relation</u> is unordered set that contain the relationship of attributes that represent entities

A <u>tuple</u> is a set of attribute values (also known as its <u>domain</u>) in the relation. 

* Values are (normally) atomic/scalar;
* The special value **NULL** is a member of every domain
* n-ary relation is a tables with n-columns 

**Example**

<font color="red"><b>Artist</b>(name, year, country)</font>

| name          | year | country | <font color = "red">ID</font> |
| ------------- | ---- | ------- | ----------------------------- |
| Wu Tang Clan  | 1992 | USA     | <font color="red">123</font>  |
| Notorious BIG | 1992 | USA     | <font color="red">456</font>  |
| Ice Cube      | 1989 | USA     | <font color="red">789</font>  |

#### PRIMARY KEYS

A relation's <u>primary key</u> uniquely identifies a single tuple: *you don't know if there is another one called Ice Cube in the **Table: Artist*** , to locate the specific tuple, you need a primary key like the red ID above. 

Some DBMSs automatically crate an internal primary key if you don't define one. 

Auto-generation of unique integer primary keys: 

* SEQUENCE (SQL: 2003)
* AUTO_INCREMENT(MySQL)

#### FOREIGN KEYS

A <u>foreign key</u> specifies that an attribute from one relation has to map to a tuple in another relation 

We use a <u>foreign key</u> to link a table to another table.

#### DATA MANIPULATION LANGUAGES (DML)

Hot to storage retrieve information from a database

**Procedural**

* The query specifies the (high-level)strategy the DBMS should use to find the desired result.[<font color="red">**Relational** Algebra </font>]

**Non-Procedural**

* The query specifies only what data is wanted and not how to find it [<font color="red">**Relational** Calculus</font>]

### RELATIONAL ALGEBRA 

Fundamental operations to retrieve and manipulate tuples in a relation. *Based on set algebra*

Each operator takes one ore more relations as its inputs and outputs a new relation.

* We can "chain" operators together to create more complex operations 

#### SELECT 

Choose a subset of the tuples from a relation that satisfies a selection predicate. 

* Predicate acts as a filter to retain only tuples that fulfill its qualifying requirement. 
* Can combine multiple predicates using conjunctions / disjunctions. 

**Syntax**: $\sigma_{\text{predicate}}(R)$

| a_id | b_id |
| :--: | :--: |
| a_1  | 101  |
| a_2  | 102  |
| a_2  | 103  |
| a_3  | 104  |

<center><b>Table: </b>R(a_id, b_id)</center>

| a_id | b_id |
| :--: | :--: |
| a_2  | 102  |
| a_2  | 103  |

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    extensions: ["tex2jax.js"],
    jax: ["input/TeX", "output/HTML-CSS"],
    tex2jax: {
      <!--$表示行内元素，$$表示块状元素 -->
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { availableFonts: ["TeX"] }
  });
</script>
<script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js">
</script>
<center><b>Table: </b>$$\sgima_{\text{a_id = 'a2'}R$$</center>

```{SQL}
SELECT * FROM R 
WHERE a_id = 'a2';
```



<center><b>Table: </b>R(a_id, b_id)</center>

| a_id | b_id |
| :--: | :--: |
| a_2  | 103  |



<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    extensions: ["tex2jax.js"],
    jax: ["input/TeX", "output/HTML-CSS"],
    tex2jax: {
      <!--$表示行内元素，$$表示块状元素 -->
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { availableFonts: ["TeX"] }
  });
</script>
<script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js">
</script>
<center><b>Table: </b>$\sgima_{\text{a_id = 'a2' \cap b_id > 102}R$</center>

```{SQL}
SELECT * FROM R 
WHERE a_id = 'a2' AND b_id > 102; 
```

#### PROJECTION 

Generate a relation with tuples that **contains only the specified attributes**.

* Can rearrange attributes' ordering. 
* Can manipulate the values 

**Syntax**: $\pi_{A_1, A_2, \dots, A_n} (R)$

| b_id | a_id |
| :--: | :--: |
|  2   | a_2  |
|  2   | a_2  |

Table: $\pi_{b\_id - 100, a_id}(\sigma_{a\_id = 'a2'}(R))​$

*In this example, we rearrange the attributes' ordering (a_id & b_id) and manipulate the b_ids' values 

```{SQL}
SELECT b_id-100, a_id
FROM R
WHERE a_id = 'a_2';
```

#### UNION

Generate a relation that contains all tuples that appear in either only one or both of the input relations. 

**Syntax**: $(R \cup S)$

| a_id | b_id |
| :--: | :--: |
| a_1  | 101  |
| a_2  | 102  |
| a_3  | 103  |

Table: $R(a\_id, b\_id)​$

| a_id | b_id |
| :--: | :--: |
| a_3  | 103  |
| a_4  | 104  |
| a_5  | 105  |

Table: $S(a\_id, b\_id)​$

| a_id | b_id |
| :--: | :--: |
| a_1  | 101  |
| a_2  | 102  |
| a_3  | 103  |
| a_3  | 103  |
| a_4  | 104  |
| a_5  | 105  |

Table: $R(a\_id, \cup \ b\_id)$

```{SQL}
(SELECT * FROM R ) 
UNION 
(SELECT * FROM S)  
```

#### INTERSECTION 

Generated a relation that contains only the tuples that appears in both of the input relations 

**Syntax**: $(R \cap S)​$ 

| a_id | b_id |
| :--: | :--: |
| a_1  | 101  |
| a_2  | 102  |
| a_3  | 103  |

Table: $R(a\_id, b\_id)$

| a_id | b_id |
| :--: | :--: |
| a_3  | 103  |
| a_4  | 104  |
| a_5  | 105  |

Table: $S(a\_id, b\_id)​$

| a_id | b_id |
| :--: | :--: |
| a_3  | 103  |

Table: $R(a\_id, \cap \ b\_id)$

```{SQL}
(SELECT * FROM R)
INTERSECT 
(SELECT * FROM S)
```



#### DIFFERENCE 

Generate a relation that contains only the tuples that appear in the frist and not the second of the input relations 

**Syntax**: $(R - S)$

*In `MySQL` there is no `INTERSECT or `EXCEPT`, nevertheless, we can use other command to execute this operation:* 

```{SQL}
--- Intersection ---
SELECT DISTINCT * FROM R,S

--- Difference ---
SELECT * FROM R WHERE  NOT IN (SELECT * FROM S) 
```

#### PRODUCT 

Generate a relation that **contains all possible combinations** of tuples from the input relation

**Syntax** $(R \times S)$

| a_id | b_id |
| :--: | :--: |
| a_1  | 101  |
| a_2  | 102  |
| a_3  | 103  |

Table: $R(a\_id, b\_id)$

| a_id | b_id |
| :--: | :--: |
| a_3  | 103  |
| a_4  | 104  |
| a_5  | 105  |

Table: $S(a\_id, b\_id)​$

| R.a_id | R.b_id | S.a_id | S.b_id |
| ------ | ------ | ------ | ------ |
| a1     | 101    | a3     | 103    |
| a1     | 101    | a4     | 104    |
| a1     | 101    | a5     | 105    |
| a2     | 102    | a3     | 103    |
| a2     | 102    | a4     | 104    |
| a2     | 102    | a5     | 105    |
| a3     | 103    | a3     | 103    |
| a3     | 103    | a4     | 104    |
| a3     | 103    | a5     | 105    |

```{SQL}
SELECT * FROM R CROSS JOIN S; 
SELECT * FROM R , S; 
```

*There is a two column at $R$ and two at $S$, after the `PRODECT`, **THERE ARE FOUR COLUMN*** . It can get all the combination of two table (or multiple table).

#### JOIN 

Generate a relation that contains all tuples that are a combination of two tuples (one from each input relation) with a common values(s) for one or more attributes. Which means, we have to check if there are the every attribute has sample things as the sample value. 

**Syntax**: $(R \bowtie S)$ 

$

| a_id | b_id |
| :--: | :--: |
| a_1  | 101  |
| a_2  | 102  |
| a_3  | 103  |

Table: $R(a\_id, b\_id)$

| a_id | b_id |
| :--: | :--: |
| a_3  | 103  |
| a_4  | 104  |
| a_5  | 105  |

Table: $S(a\_id, b\_id)​$

| a_id | b_id |
| ---- | ---- |
| a3   | 103  |

```{SQL}
SELECT * FROM R NATURAL JOIN S
```

**What is the difference with NATURAL JOIN and INTERSECT ?**

### EXTRA OPERATOERS 

* Rename($\rho​$)
* Assignment ($R \leftarrow S$)
* Duplicate Elimination ($\delta$)
* Aggregation ($\gamma$)
* Sorting ($\tau$)
* Division ($R \div S$)

### OBSERVATION

**Relation algebra still defines the high-level steps of how to compute a query**

$\Rightarrow​$ $\sigma_{b\_id = 102}(R \bowtie S)​$ vs. $(R \bowtie (\sigma_{b\_id = 102}(S)))​$

This have difference expression has the same answer but **different run time performance**. (*This depends on the data size*)

A better approach is just state the high-level query you want! 

$\Rightarrow$ Retrieve the joined tuples from $R$ and $S$ where $b\_{id}$ equals to $102$

#### QUERIES 

The relational model is independent of any query language implementation. 

**SQL** is the de facto standard. 

## Advanced SQL 

### RELATIONAL LANGUAGES

User only needs to specify the answer that they want, not how to compute it. 

The DBMS is responsible for efficient evaluation of the query. 

$\rightarrow$ Query optimizer: re-orders operations and generates query plan 

SQL is not technically a language, it just like a collection: 

- Data Manipulation Languages (DML) 
- Data Definition Languages (DDL)
- Data Control Language (DCL)

It also includes: 

- View definition 
- Integrity & Referential Constraints 
- Transactions 

<font color="red">Important:</font> SQL is based on **bags**(duplicates) not **sets**(non-duplicates)

### SQL HISTORY

Originally "SEQUEL" from IBM's **System R** prototype 

- <u>S</u>tructured <u>E</u>nglish <u>Q</u>uery <u>L</u>anguage
- Adopted by Oracle in the 1970s.

IBM release DB2 in 1983 

ANSI Standard in 1986. ISO in 1987 $\Rightarrow$ <u>S</u>tructured <u>Q</u>uery <u>L</u>anguage



[![Screenshot 2019-04-02 at 01.01.25.png](https://i.loli.net/2019/04/02/5ca243e8b9f01.png)](https://i.loli.net/2019/04/02/5ca243e8b9f01.png)

### RELATIONAL LANGUAGE (Cont.)

#### AGGREGATES 

Functions that return a single value from a bag of tuples: 

* <font color="red">AVG(col)</font> $\rightarrow$ Return the average col value;
* <font color="red">Min(col)</font> $\rightarrow$ Return the minimum col value;
* <font color="red">MAX(col)</font> $\rightarrow$ Return the maximum col value;
* <font color="red">SUM(col)</font> $\rightarrow$ Return the sum of values in col;
* <font color="red">COUNT(col)</font> $\rightarrow$ Return # of values for col

**Aggregate functions can only be used in the <font color="red">SELECT</font> output list.**

*Get # of students with a "@cs" login:*

```{SQL}
SELECT COUNT(login) AS cnt
FROM student WHERE login LIKE '%@cs';
```

However I can also investigate the quantity of login with a "@cs": 

```{SQL}
SELECT s_name, COUNT(1) 
FROM student WHERE login LIKE '%@cs' GROUP BY s_name;
```

As  `COUNT(1)` add $1​$ for each loop

**We can also use MULTIPLE AGGREGATES / DISTINCT AGGREGATES** 

*Get the number of students and their average GPA that have a "@cs" login* 

```{SQL}
SELECT AVG(gpa), COUNT(sid)
FROM student WHERE login LIKE '%@cs';
```

*Get the number of **unique** students have an "@cs" login* 

```{SQL}
SELECT COUNT (DISTINCT login) 
FROM student WHERE login LIKE '%@cs'
```

 *(COUNT, SUM, AVG support DISTINCT)*

Output of other columns outside of an aggregate is undefined. 

**GROUP BY**

Project tuples into subsets and calculate aggregates against each subset.

*Get the average GPA of students enrolled in each course* 

```{SQL}
SELECT AVG(s.gpa). e.cid 
FROM enrolled AS e, student AS s WHERE e.sid = s.sid
GROUP BY e.cid
```

[![Screenshot 2019-04-02 at 02.20.20.png](https://i.loli.net/2019/04/02/5ca2566a32186.png)](https://i.loli.net/2019/04/02/5ca2566a32186.png)

[![Screenshot 2019-04-02 at 02.20.30.png](https://i.loli.net/2019/04/02/5ca2567210f70.png)](https://i.loli.net/2019/04/02/5ca2567210f70.png)

**HAVING** 

Filters results based on aggregation computation. Like a WHERE clause for a GROUP BY 

**You need to FIRST sort the data set out , then add the condition.** 

```{SQL}
SELECT AVG(s.gpa) as avg_gpa, e.cid 
FROM enrolled AS e, student AS s
WEHRE e.sid = s.sid 
GROUP BY e.cid
HAVING avg_gpa > 3.9  
```

### STRING OPERATIONS

![Screenshot 2019-04-06 at 12.35.05.png](https://i.loli.net/2019/04/06/5ca82c8121cfd.png)

<font color='red'>LIKE</font> is used for string matching. String-matching operators 

* "%" Matches any substring ( including empty strings). 
* "_" Match any one character 

```{SQL}
SELECT * FROM enrolled AS e 
WHERE e.cid LIKE '15-%'
```

```{SQL}
SELECT * FROM student AS s 
WHERE s.login LIKE '%@c_'
```

SQL-92 defines string functions $\rightarrow$ Many DBMs also have their own unique functions, can be used in either output and predicates

Also, SQL standard says to use $||$ operator to concatenate (link) two or more strings together.

```mysql
SELECT name FROM student 
WHERE login = CONCAT(LOWER (name), '@cs');
```

**DATE/TIME OPERATION** 

Operations to manipulate and modify <font color='red'>DATA/TIME</font> attributes. 

Can be used in either output and predicates. Support/syntax varies wildly $\dots$ 

**DEMO: Get the # of days since the beginning of the year.**

```mysql
SELECT DATEDIFF('2018-01-01','2019-01-01') AS Days;
```

**OUTPUT REDIRECTION**

Store query results in another **new** table:

* table must not already be defined
* Table will have the same # fo columns with the same types as the input 

```mysql
CREATE TABLE CourseIds( 
  SELECT DISTINCT cid FROM enrolled);
```

Inserts tuple from query into another table: 

* **Innver SELECT must generate the same columns** as the target table 
* DBMSs ahve different options/syntax on what to do with duplicates 



**OUTPUT CONTAL**

ORDER BY <column*> [ASC|DESC]

* Order the output tuples by the values in one or more of their columns

```mysql
SELECT sid, grede FROM enrolled 
WHERE cid = '15-721'
ORDER BY grade DESC, sid ASC;
```

