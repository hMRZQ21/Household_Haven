Create table if not exists "user" (
	"userID" SERIAL,
	"name" VARCHAR(100) NOT NULL,
	"email" VARCHAR(100) NOT NULL,
	"password" VARCHAR(100) NOT NULL,
	"address" VARCHAR(100) NOT NULL,
	"city" VARCHAR(50) NOT NULL,
	"state" VARCHAR(2) NOT NULL,
	"zipcode" INT NOT NULL,
	"usertype" INT NOT NULL DEFAULT 0,
	PRIMARY KEY ("userID")
);

INSERT INTO "user" VALUES (0, '"HI"', '"SOething"', '"123"', '"12345"', '"sad"', 'ny', 10001, 0);
INSERT INTO "user" VALUES (1, '"bye"', '"SOething"', '"123"', '"12345"', '"sad"', 'ny', 10001, 0);

create table if not exists "order"(
	"orderID" serial,
	"userID" int,
	"orderDate" date NOT NULL default current_date,
	"status" varchar(15),
	"totalAmount" numeric(6,2),
	primary key ("orderID"),
	foreign key ("userID") references "user" ("userID") on Update cascade
);

insert into "order" ("orderID", "userID", "status", "totalAmount") values (0, 1, 'Processing' , 420.69);

CREATE table if not exists "product" (
	"productID" serial,
	"sellerID" INT NOT NULL,
	"itemName" varchar(100) NOT NULL,
	"itemDesc" varchar(300),
	"price" numeric(6,2) NOT NULL,
	"stock" int,
	Primary Key ("productID"),
	Foreign Key ("sellerID") References "user" ("userID") ON update CASCADE);
	
Insert into "product" values (0,0,'ur mom', 'big chungus', 69.69, 420);
Insert into "product" values (1,0,'ur dad', 'smol chungus', 12.12, 69);

create table if not exists "review" (
	"reviewID" serial,
	"userID" INT not NULL,
	"productID" int NOT NULL,
	"date" date NOT NULL DEFAULT current_date,
	"rating" numeric(2,1) NOT NULL,
	"comment" varchar(250),
	Primary Key ("reviewID"),
	Foreign Key ("userID") References "user" ("userID") on UPDATE caScade,
	Foreign Key ("productID") References "product" ("productID") on update casCAde
);

insert into "review" ("reviewID", "userID", "productID", "rating", "comment" ) vaLUes (0, 0, 0, 1.2,'she ate all my carrots');

create table if not exists "payment" (
	"transactionID" serial,
	"orderID" int,
	"paymentMethod" varchar(100) not null,
	"amount" numeric (6,2) not null,
	"status" varchar (100) not null,
	primary key ("transactionID"),
	foreign key ("orderID") references "order" ("orderID") on update cascade
);

insert into "payment" values(0,0, 'MasterCard', 420.69, 'Fulfilled');

create table if not exists "orderItem"(
	"orderItemID" serial,
	"orderID" int,
	"productID" int,
	"quantity" int not null default 1,
	primary key ("orderItemID"),
	foreign key ("orderID") references "order" ("orderID") on update cascade,
	foreign key ("productID") references "product" ("productID") on update cascade
);

insert into "orderItem" values (0, 0, 1, 300);

create table if not exists "cart" (
	"cartID" serial,
	"userID" int,
	primary key ("cartID"),
	foreign key ("userID") references "user" ("userID") on update cascade
);

insert into "cart" values (0, 0);

create table if not exists "cartItems" (
	"cartItemID" serial,
	"cartID" int,
	"productID" int,
	"quantity" int not NULL,
	primary key ("cartItemID"),
	foreign key ("cartID")references "cart" ("cartID") on update cascade,
	foreign key ("productID") references "product" ("productID") on update cascade
 );
 
 
 insert into "cartItems" values (0,0,0,99);
 insert into "cartItems" values (1,0,1,5);

CREATE table if not exists "category"(
	"categoryID" serial,
	"parentCategoryID" INT NOT NULL,
	"name" varchar(100) NOT NULL,
	"desc" varchar(300),
	Primary Key ("categoryID"),
	Foreign Key ("parentCategoryID") References "category" ("categoryID")
);

INSERT INTO "category" values (0, 0, 'chairs', 'something to sit on');
INSERT INTO "category" values (1, 0, 'stools', 'a chair with no backrest');
INSERT INTO "category" values (2, 2, 'table', 'somewhere to place goods');
