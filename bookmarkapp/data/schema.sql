CREATE TABLE "bookmarks" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"blurb"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);



CREATE TABLE "users" (
	"id"	INTEGER,
	"user_name"	TEXT NOT NULL UNIQUE,
	"display_name"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"privilege"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
