/*
    Purpose: Inserts 5 rows of sample data into the Bookmarks table
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



--UN: top_guy
--PW VerySecur3#
INSERT INTO users 
(user_name, display_name, password, privilege)
VALUES
('top_guy', 'Chief', 
'pbkdf2:sha256:260000$ZZB6QlNvCwTd7WNC$0f433ffe8d4bf92b00b25905f2ba61e5ff8ae573771bb537561dfb6d9b95cf16', 
'admin');

--UN 2nd_user
--PW LetMeIn
INSERT INTO users 
(user_name, display_name, password, privilege)
VALUES
('2nd_user', 'Second', 
'pbkdf2:sha256:260000$xrLiOOoG9y0q6c7U$60f271e2e34c2c513ceb926e717e7de9b86f0be61cd204ddca9e596816aedfcc', 
'user');

--UN 3rd_user
--PW LetMeIn
INSERT INTO users 
(user_name, display_name, password, privilege)
VALUES
('3rd_user', 'Third', 
'pbkdf2:sha256:260000$nVAJZhBh2rl4SLXg$e3f12d2805f91ec503d34ab75cb0b1ed363114bd3926bbbc7e8642dfee9bc747', 
'user');


