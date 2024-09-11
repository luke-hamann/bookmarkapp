/*
	Title: Schema
	Purpose: Create the Bookmarks table
*/

CREATE TABLE "bookmarks" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"blurb"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
