/*
	Title: Schema
	Authors: Malachi Harris & Luke Hamann
	Date: 2024-08-31
	Updated: 2024-09-13
	Purpose: Create the Bookmarks and Users tables
*/

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
