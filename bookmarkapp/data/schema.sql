/*
	Title: Schema
	Authors: Malachi Harris & Luke Hamann
	Date: 2024-08-31
	Updated: 2024-09-13
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
