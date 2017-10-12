
drop table if exists Items;
drop table if exists Categories;
drop table if exists Bids;
drop table if exists Users;
drop table if exists CurrentTime;

create table CurrentTime(
  CurTime text
);
INSERT into CurrentTime values('2001-12-20 00:00:01');
SELECT * from CurrentTime;

CREATE TABLE Bids (
  ItemID INT,
  UserID text,
  Amount double,
  Time   text,
  PRIMARY KEY (ItemID, Time),
  FOREIGN KEY (ItemID)
     REFERENCES Items,
  FOREIGN KEY (UserID)
     REFERENCES Users
);

create table Items (
  ItemID INT PRIMARY KEY,
  UserID text,
  Name text,
  Buy_Price double,
  First_Bid double,
  Currently double,
  Number_of_Bids INT,
  Started text,
  Ends text check(Ends > Started),
  Description text,
  FOREIGN KEY (UserID)
     REFERENCES Users(UserID)
);

CREATE TABLE Categories(
  ItemID INT,
  Category text,
  PRIMARY KEY (ItemID, Category),
  FOREIGN KEY (ItemID)
     REFERENCES Items
);

CREATE TABLE Users (
  UserID text PRIMARY KEY,
  Rating INT,
  Location text,
  Country text
);
