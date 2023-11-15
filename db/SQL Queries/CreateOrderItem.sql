drop table if exists "orderItem";

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

select * from "orderItem";