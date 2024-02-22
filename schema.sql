CREATE TABLE users (
	user_id INTEGER PRIMARY KEY,
	email_address TEXT NOT NULL UNIQUE
);

CREATE TABLE accounts (
	account_id INTEGER PRIMARY KEY,
	email_address TEXT NOT NULL,
	username TEXT NOT NULL UNIQUE,
	FOREIGN KEY (email_address) REFERENCES users(email_address)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE followers (
	follower_id INTEGER NOT NULL,
	followed_id INTEGER NOT NULL,
	PRIMARY KEY (follower_id, followed_id),
	FOREIGN KEY (follower_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (followed_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE posts (
	post_id INTEGER PRIMARY KEY,
	message TEXT NOT NULL, 
	poster_id INTEGER NOT NULL,
	year INTEGER,
	month INTEGER check(month BETWEEN 1 AND 12),
	day INTEGER check(day BETWEEN 1 AND 31), 
	hour INTEGER check(hour BETWEEN 0 AND 23),
	minute INTEGER check(minute BETWEEN 0 and 59),
	FOREIGN KEY (poster_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE likes (
	post_id INTEGER,
	liker_id INTEGER,
	PRIMARY KEY(post_id, liker_id),
	FOREIGN KEY (liker_id) REFERENCES accounts(account_id)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (post_id) REFERENCES posts(post_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE reply_likes (
	reply_id INTEGER,
	liker_id INTEGER,
	PRIMARY KEY(reply_id, liker_id),
	FOREIGN KEY (liker_id) REFERENCES accounts(account_id)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (reply_id) REFERENCES replies(post_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);


CREATE TABLE replies (
	reply_id INTEGER PRIMARY KEY,
	post_id INTEGER ,
	message TEXT NOT NULL, 
	replier_id INTEGER,
	parent_reply_id INT REFERENCES accounts(reply_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	year INTEGER,
	month INTEGER check(month BETWEEN 1 AND 12),
	day INTEGER check(day BETWEEN 1 AND 31), 
	hour INTEGER check(hour BETWEEN 0 AND 23),
	minute INTEGER check(minute BETWEEN 0 AND 59),
	FOREIGN KEY (replier_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (post_id) REFERENCES posts(post_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);
