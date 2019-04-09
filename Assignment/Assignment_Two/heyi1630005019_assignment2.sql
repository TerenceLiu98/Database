/* 1630005019 heyi */

/* Delete the tables if already exist */
drop table if exists Book;
drop table if exists Reviewer;
drop table if exists Rating;

/* Create the schema */
create table Book(bID int, bname text, year int, author text);
create table Reviewer(rID int, rname text);
create table Rating(rID int, bID int, stars int, rDate date);

/* Populate the tables with data */
insert into Book values(1001, 'Journey to the West', 1925, 'Chengen Wu');
insert into Book values(1002, 'Wolf Totem', 2004, 'Rong Jiang');
insert into Book values(1003, 'Fortress Besieged', 1945, 'Zhongshu Qian');
insert into Book values(1004, 'Langya List', 2014, 'Yan Hai');
insert into Book values(1005, 'Historical Records', 2004, 'Sima Qian');
insert into Book values(1006, 'Ordinary World', 1989, 'Yao Lu');
insert into Book values(1007, 'Frontier City', 2005, 'Congwen Shen');
insert into Book values(1008, 'The Legend of Chu Liu Xiang', 1967, 'Long Gu');

insert into Reviewer values(3001, 'Leonard');
insert into Reviewer values(3002, 'Oscar');
insert into Reviewer values(3003, 'Spike');
insert into Reviewer values(3004, 'Jason');
insert into Reviewer values(3005, 'Ivan');
insert into Reviewer values(3006, 'Albert');
insert into Reviewer values(3007, 'Carl');
insert into Reviewer values(3008, 'Henry');

insert into Rating values(3001, 1001, 2, '2015-05-17');
insert into Rating values(3001, 1001, 4, '2015-05-03');
insert into Rating values(3002, 1006, 4, null);
insert into Rating values(3003, 1003, 2, '2015-05-19');
insert into Rating values(3003, 1008, 4, '2015-05-22');
insert into Rating values(3003, 1008, 2, '2015-05-06');
insert into Rating values(3004, 1001, 3, '2015-05-11');
insert into Rating values(3005, 1003, 3, '2015-05-09');
insert into Rating values(3005, 1004, 2, '2015-05-16');
insert into Rating values(3005, 1008, 4, null);
insert into Rating values(3006, 1007, 3, '2015-05-24');
insert into Rating values(3006, 1006, 5, '2015-05-31');
insert into Rating values(3007, 1007, 5, '2015-05-12');
insert into Rating values(3008, 1004, 3, '2015-05-08');

/* Ans for question 1 to 8 */
/* 1 */
SELECT DISTINCT Book.year, Rating.stars FROM Book, Rating WHERE Book.bID = Rating.bID and (Rating.stars = 2 OR Rating.stars = 3) ORDER BY year DESC;

/* 2 */
SELECT DISTINCT rname FROM Reviewer, Rating WHERE rDate IS NULL;

/* 3 */
SELECT DISTINCT * FROM Rating AS R1, Rating AS R2, Book, Reviewer WHERE Reviewer.rID = R1.rID AND Book.bID = R1.bID AND R1.rID = R2.rID AND R1.bID = R2.bID AND R1.stars>R2.stars AND R1.rDate>R2.rDate;

/* 4 */
SELECT DISTINCT bname, AVG(stars) FROM Book, Rating WHERE Book.bID = Rating.bID GROUP BY Book.bname ORDER BY AVG (stars) DESC, bname ASC;

/* 5 */
SELECT DISTINCT rname FROM Reviewer, Rating WHERE Rating.rID = Reviewer.rID GROUP BY Reviewer.rname HAVING COUNT(bID) >= 3;

/* 6 */
SELECT DISTINCT rname, bname, stars, rDate FROM Book, Reviewer, Rating WHERE Book.bID = Rating.bID AND Rating.rID = Reviewer.rID ORDER BY rname ASC, bname ASC, stars ASC;

/* 7 */
SELECT DISTINCT bname, MAX(stars) FROM Book, Rating WHERE Book.bID = Rating.bID GROUP BY Book.bname ORDER BY bname ASC;

/* 8 */
SELECT DISTINCT bname, MAX(stars)-MIN(stars) FROM Book, Rating WHERE Book.bID = Rating.bID GROUP BY Book.bname HAVING MAX(stars)-MIN(stars) != 0 ORDER BY MAX(stars)-MIN(stars) DESC ,bname ASC;