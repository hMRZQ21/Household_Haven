DROP table if exists "review";

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

select * from "review";