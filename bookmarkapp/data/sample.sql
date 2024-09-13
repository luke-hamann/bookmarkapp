/*
    Title: Sample Data
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-13
    Purpose: Insert 5 rows of sample data into the Bookmarks table
*/

INSERT INTO bookmarks (title, url, blurb, description)
VALUES (
'Southeast Technical College',
'https://www.southeasttech.edu/',
'College in southeastern South Dakota',
'They teach computer programming.'
);

INSERT INTO bookmarks (title, url, blurb, description)
VALUES (
'sqlite3 -- DB-API 2.0 interface for SQLite databases',
'https://docs.python.org/3/library/sqlite3.html',
'Python standard library documentation on sqlite3',
'The tutorial is straightforward.'
);

INSERT INTO bookmarks (title, url, blurb, description)
VALUES (
'Welcome to Flask -- Flask Documentation (3.0.x)',
'https://flask.palletsprojects.com/en/3.0.x/',
'Web microframework for Python',
'The interfaces are good as an introduction to web development with Python.'
);

INSERT INTO bookmarks (title, url, blurb, description)
VALUES (
'Template Designer Documentation -- Jinja Documentation (3.1.x)',
'https://jinja.palletsprojects.com/en/3.1.x/templates/',
'Text templating engine for Python',
'Jinja templates have many useful features, including:

* Variables
* Loops
* Inheritance
'
);

INSERT INTO bookmarks (title, url, blurb, description)
VALUES (
'Git - Basic Branching and Merging',
'https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging',
'A brief introduction to branching and merging with git',
'This article covers the basic usage of a few git commands, including:

* git checkout
* git branch
* git merge
'
);
