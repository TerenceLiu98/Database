# Introduction to SQL 

*From Phil Spector (Statistical Computing Facility UCB)*

## What is SQL 

* > <font color="red">**S**</font>tructured <font color="red">**Q**</font>uery <font color="red">**L**</font>anguage

* Usually "talk" to a database server 

* Used as front end to many databases (mysql, postgresql, oracle, sybase)

* Three Subsystems: data description, data access and privileges 

* Optimized for certain data arrangements 

* The language is case-sensitive, but I use upper case for keywords 

## When do you need a Database 

* Multiple simultaneous changes to data (concurrency)
* Data changes on a regular basis
* Large data sets where you only need some observations/variables 
* Share huge data set among many people
* Rapid queries with no analysis
* Web interfaces to data, especially dynamic data

## Uses of Databases 

Traditional Uses: 

* Live queries 
* Report Generation 
* Normalization, foreign keys, joins, etc. 

Newer uses: 

* Storage - data is extracted and analyzed in another application 
* Backends to websites 
* Traditional rules may not be as important

## Ways to Use SQL

* console command 

  ```{SQL}
  mysql -u user -p passwd
  ```

* GUI interfaces are often available 

* Interfaces to many programming languages: `R`, `python`, etc.

* SQLite - use SQL without a database server 

* `PROC SQL` in SAS

## Some Relational Database Concepts 

* A database server can contain many databases 
* Databases are collections of tables 
* Tables are two-dimensional with rows (observations) and columns (varibles) 
* Limited mathematical and summary operations available
* Very good at combining information from several tables











SQL Exercise Plus

SELECT person_name, city FROM employee, works, company

​	WHERE (employee.person_name = works.person_name) AND (company.city = employee.city);



SELECT * FROM  employee, company

​	WHERE employee.person_name, employee.city in (select employee.person_name)

SELECT * FROM employee, works, company

​	WHERE works.city = 'Hong Kong' AND SELECT COUNT()



SELECT * FROM  works, company

​	WHERE works.salary <= 100,000;	



<http://www.rdatamining.com/>













