Drop table if exists "product";

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

select * from "product"