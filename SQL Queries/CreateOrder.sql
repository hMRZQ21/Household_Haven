DROP table if exists "order";

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

select * from "order";