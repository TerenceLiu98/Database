CREATE TABLE User (
  StudentId     CHAR(10) UNIQUE NOT NULL,
  Name          VARCHAR(20),
  Password      CHAR(32)        NOT NULL,
  IsAdmin       BIT DEFAULT 0,
  TimesBorrowed INT DEFAULT 0,
  NumBorrowed   INT DEFAULT 0
);

CREATE TABLE Book (
  BookName     VARCHAR(30) NOT NULL,
  BookId       CHAR(6)     NOT NULL,
  Auth         VARCHAR(20) NOT NULL,
  Category     VARCHAR(10) DEFAULT NULL,
  Publisher    VARCHAR(30) DEFAULT NULL,
  PublishTime  DATE,
  NumStorage   INT         DEFAULT 0,
  NumCanBorrow INT         DEFAULT 0,
  NumBorrowed  INT         DEFAULT 0
);

CREATE TABLE User_Book (
  StudentId   CHAR(10) UNIQUE NOT NULL,
  BookId      CHAR(6)         NOT NULL,
  BorrowTime  DATE,
  ReturnTime  DATE,
  BorrowState BIT DEFAULT 0
);

CREATE TABLE BuyOrDrop (
  BookId    CHAR(6) NOT NULL,
  Time      DATE,
  BuyOrDrop BIT DEFAULT 0,
  Number    INT DEFAULT 0
);

INSERT INTO User VALUES ('0000000000', '管理员', 'f9687b82c237c8868a92ffa548c0a16a', 1, 0, 0);
