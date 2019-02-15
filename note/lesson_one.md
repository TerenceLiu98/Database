# Introduction

## Course assessment 
* Chapter One: Introduction 
* Chapter Two: Relational Model 
* Chapter Three: SQL 
* Chapter Four: Advanced SQL
* Midterm
* Chapter Six: ER model 
* Chapter Seven: Database Design
* Chapter Ten: XML Database 
* Final 

## Introduction of Database Management System (DBMS)
* Database Applications 
  * Banking: transactions 
  * Airlines: reservations, schedules
  * Universities: registration, grades
  * **And so on**
* Database can be very large
* Database touch all aspects of our lives. 

## Why we need database: **University Database Example**
* Course Management
  * Add students, instructors, and courses 
  * Register students for courses, and generate class rosters 
  * Assign grades to students, compute grade point averages(GPA) and generate transcripts
* Provide basic features necessary for data access 
  * Shared access by a community of uses
  * Well-defined schema for data access 
  * Support query language
* In the early days, applications were built directly on top of file systems.

## Drawbacks of using file system to store data

* Data redundancy(冗余) and inconsistency(矛盾)
  * Multiple file formats, duplication of information in different files 
* Difficulty in accessing data 
  * Need to write a new programme to carry out each new task 
* Data isolation 
  * Multiple files and formats
* Integrity problems 
  * Integrity constraints (e.g. account balaence $\geq$ 0) become buried in program code rather than being stated explicitly 
  * Hard to add new constraints or change existing ones.
* Atomicity of updates 
  * Failures may leave database in an inconsistent state with partial updates carried out.
  * Example: Transfer of funds from on account to another should either complete or not happen at all. 
* Concurrent access by multiple users 
  * Concurrent access needed for performance 
  * Uncontrolled concurrent accesses can lead to inconsistencies 
    * Example: Two students want to choose the same course that has only one vacancy left. 
* Security problems 
  * Hard to provide user access to some, but not all, data

Database system offer solutions to all the above problems. 

## Database Managements Systems (DBMS) provides...
* Efficient
* Reliable 
* Convenient
* Safe 
* Multi-user ( Storage of and access to)
* Massive amounts of persistent data

## Key concepts
* Data modeling 
* Schema vs. Data instances 
* Data definition language (DDL) 
* Data manipulation or query language (DML)
* DBMS implementer 
* DBMS designer 
* Database application developer (USER) 
* Database administrator

## History of Database Systems 
*Omit* 


