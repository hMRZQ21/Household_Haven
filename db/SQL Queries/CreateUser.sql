-- Drop table if exists "user";

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

Select * from "user";