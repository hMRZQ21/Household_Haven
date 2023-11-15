drop table if exists "payment";

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

select * from "payment";