Drop table if exists "cartItems";

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
 
 select * from "cartItems";