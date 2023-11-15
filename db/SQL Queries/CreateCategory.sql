DROP table if exists"category";

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

select * from "category";