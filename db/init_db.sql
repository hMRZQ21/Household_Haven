
-- DROP table if exists "user";
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

-- INSERT INTO "user" ("name", "email", "password", "address", "city", "state", "zipcode", "usertype")
-- VALUES ('hi', 'something@example.com', '123', 'WEIRD ST', 'NYC', 'NY', 10001, 0);

-- SELECT * FROM "user"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "order";
create table if not exists "order"(
	"orderID" serial,
	"userID" int,
	"orderDate" date NOT NULL default current_date,
	"status" varchar(15),
	"totalAmount" numeric(6,2),
	primary key ("orderID"),
	foreign key ("userID") references "user" ("userID") on Update cascade
);

-- insert into "order" ("userID", "status", "totalAmount") 
-- values (1, 'Processing', 420.69);
-- SELECT * FROM "order"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "product";
CREATE table if not exists "product" (
	"productID" serial,
	"sellerID" INT NOT NULL,
	"itemName" varchar(100) NOT NULL,
	"itemDesc" varchar(300),
	"price" numeric(6,2) NOT NULL,
	"stock" int,
	Primary Key ("productID"),
	Foreign Key ("sellerID") References "user" ("userID") ON update CASCADE);
	
-- Insert into "product" ("sellerID", "itemName", "itemDesc", "price", "stock")
-- values (1, 'ur mom', 'big chungus', 69.69, 420),
-- 	   (1, 'ur dad', 'smol chungus', 12.12, 69);
-- SELECT * FROM "product"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "review";
create table if not exists "review" (
	"reviewID" serial,
	"userID" INT not NULL,
	"productID" int NOT NULL,
	"date" date NOT NULL DEFAULT current_date,
	"rating" numeric(2,1) NOT NULL,
	"comment" varchar(250),
	Primary Key ("reviewID"),
	Foreign Key ("userID") References "user" ("userID") on UPDATE cascade,
	Foreign Key ("productID") References "product" ("productID") on UPDATE cascade
);

-- insert into "review" ("userID", "productID", "rating", "comment") 
-- values (1, 1, 1.2, 'she ate all my carrots');
-- SELECT * FROM "review"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "payment";
create table if not exists "payment" (
	"transactionID" serial,
	"orderID" int,
	"paymentMethod" varchar(100) not null,
	"amount" numeric (6,2) not null,
	"status" varchar (100) not null,
	primary key ("transactionID"),
	foreign key ("orderID") references "order" ("orderID") on update cascade
);

-- insert into "payment" ("orderID", "paymentMethod", "amount", "status")
-- values(1, 'MasterCard', 420.69, 'Fulfilled');
-- SELECT * FROM "payment"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "orderItem";
create table if not exists "orderItem"(
	"orderItemID" serial,
	"orderID" int,
	"productID" int,
	"quantity" int not null default 1,
	primary key ("orderItemID"),
	foreign key ("orderID") references "order" ("orderID") on update cascade,
	foreign key ("productID") references "product" ("productID") on update cascade
);

-- insert into "orderItem" ("orderID", "productID", "quantity")
-- values (1, 1, 300);
-- SELECT * FROM "orderItem"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "cart";
create table if not exists "cart" (
	"cartID" serial,
	"userID" int,
	primary key ("cartID"),
	foreign key ("userID") references "user" ("userID") on update cascade
);

-- insert into "cart" ("userID") values (1);
-- insert into "cart" ("userID") values (1);
-- SELECT * FROM "cart"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "cartItems";
create table if not exists "cartItems" (
	"cartItemID" serial,
	"cartID" int,
	"productID" int,
	"quantity" int not NULL default 1,
	primary key ("cartItemID"),
	foreign key ("cartID")references "cart" ("cartID") on update cascade,
	foreign key ("productID") references "product" ("productID") on update cascade
 );
 
 
--  insert into "cartItems" ("cartID", "productID", "quantity")
--  values (1, 1, 99), (1, 1, 5);
-- SELECT * FROM "cartItems"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- DROP table if exists "category";
CREATE table if not exists "category"(
	"categoryID" serial,
	"parentCategoryID" INT NOT NULL,
	"name" varchar(100) NOT NULL,
	"desc" varchar(300),
	Primary Key ("categoryID"),
	Foreign Key ("parentCategoryID") References "category" ("categoryID")
);

-- INSERT INTO "category" ("parentCategoryID", "name", "desc") 
-- values (1, 'chairs', 'something to sit on'),
-- 	   (1, 'stools', 'a chair with no backrest'),
-- 	   (2, 'table', 'somewhere to place goods');
-- SELECT * FROM "category"
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 