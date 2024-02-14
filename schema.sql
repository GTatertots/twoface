CREATE TABLE users (
	user_id INTEGER PRIMARY KEY,
	email_address TEXT NOT NULL UNIQUE,
);

CREATE TABLE accounts (
	account_id INT PRIMARY KEY,
	email_address TEXT NOT NULL,
	username TEXT NOT NULL UNIQUE
);

CREATE TABLE followers (
	follower_id INT NOT NULL,
	followed_id INT NOT NULL,
	PRIMARY KEY (follower_id, followed_id)
);

CREATE TABLE posts (
	post_id INT PRIMARY KEY,
	message TEXT NOT NULL, 
	poster_id INT NOT NULL,
	year INT,
	month TEXT IN (january, february, march, april, may, june, july, august, september, october, november, december),
	day INT, 
	hour INT,
	minute INT
);

CREATE TABLE likes (
	post_id INT,
	liker_id INT,
	PRIMARY KEY(post_id, liker_id)
);

CREATE TABLE replies (
	post_id INT ,
	message TEXT NOT NULL, 
	replier_id INT,
	year INT,
	month TEXT IN (january, february, march, april, may, june, july, august, september, october, november, december),
	day INT, 
	hour INT,
	minute INT,
	PRIMARY KEY (post_id, replier_id)
);
