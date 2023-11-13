Drop table if exists "cart";

create table if not exists "cart" (
	"cartID" serial,
	"userID" int,
	primary key ("cartID"),
	foreign key ("userID") references "user" ("userID") on update cascade
);

-- when a user is created we need to create/assign a cart to them
-- function that does that inside our flaskapp?

insert into "cart" values (0, 0);

select * from "cart"