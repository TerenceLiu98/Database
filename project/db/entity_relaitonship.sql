DROP TABLE "Book";
DROP TABLE "BuyOrDrop";
DROP TABLE "InterestGroup";
DROP TABLE "User";
DROP TABLE "User_Book";
DROP TABLE "User_Group";

CREATE TABLE "Book" (
"BookId" INTEGER NOT NULL,
"Book" TEXT,
"ISSN" INTEGER,
"Auth" TEXT,
"Category" TEXT,
"Publisher" TEXT,
"PublishTime" DATE,
"isBorrowed" INTEGER,
"location" TEXT,
PRIMARY KEY ("BookId") ,
CONSTRAINT "fk_Book" FOREIGN KEY ("BookId") REFERENCES "BuyOrDrop" ("BookId") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE "BuyOrDrop" (
"BookId" INTEGER NOT NULL,
"Time" DATE,
"BuyOrDrop" BIT,
"Number" INTEGER,
PRIMARY KEY ("BookId") 
);
CREATE TABLE "InterestGroup" (
"GroupId" INTEGER NOT NULL,
"GroupName" TEXT,
"GroupSize" REAL,
PRIMARY KEY ("GroupId") ,
CONSTRAINT "fk_InterestGroup" FOREIGN KEY ("GroupId") REFERENCES "User_Group" ("StudentId", "GroupId", "State") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE "User" (
"StudentId" INTEGER NOT NULL,
"Name" TEXT,
"Password" TEXT,
"IsAdmin" BIT,
"TimesBorrowed" TEXT,
"NumBorrowed" INTEGER,
"Group_Quantity" INTEGER,
PRIMARY KEY ("StudentId") 
);
CREATE TABLE "User_Book" (
"StudentId" INTEGER NOT NULL,
"BookId" INTEGER,
"BorrowTime" DATE,
"ReturnTime" DATE,
"BorrowState" BIT,
PRIMARY KEY ("StudentId") ,
CONSTRAINT "fk_User_Book" FOREIGN KEY ("BookId") REFERENCES "BuyOrDrop" () ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT "fk_User_Book_1" FOREIGN KEY ("StudentId", "BookId", "BorrowTime", "ReturnTime", "BorrowState") REFERENCES "User" ("StudentId", "Name", "Password", "IsAdmin", "TimesBorrowed", "NumBorrowed", "Group_Quantity") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE "User_Group" (
"StudentId" INTEGER NOT NULL,
"GroupId" INTEGER,
"State" TEXT,
PRIMARY KEY ("StudentId") ,
CONSTRAINT "fk_User_Group" FOREIGN KEY ("StudentId") REFERENCES "User" () ON DELETE CASCADE ON UPDATE CASCADE
);
