CREATE TABLE users (
	user_id INTEGER PRIMARY KEY,
	email_address TEXT NOT NULL UNIQUE
);

CREATE TABLE accounts (
	account_id INT PRIMARY KEY,
	email_address TEXT NOT NULL,
	username TEXT NOT NULL,
	FOREIGN KEY (email_address) REFERENCES users(email_address)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE followers (
	follower_id INT NOT NULL,
	followed_id INT NOT NULL,
	PRIMARY KEY (follower_id, followed_id),
	FOREIGN KEY (follower_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (followed_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE posts (
	post_id INT PRIMARY KEY,
	message TEXT NOT NULL, 
	poster_id INT NOT NULL,
	year INT,
	month TEXT check(month IN ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')),
	day INT, 
	hour INT,
	minute INT,
	FOREIGN KEY (poster_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE likes (
	post_id INT,
	liker_id INT,
	PRIMARY KEY(post_id, liker_id),
	FOREIGN KEY (liker_id) REFERENCES accounts(account_id)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (post_id) REFERENCES posts(post_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE replies (
	reply_id INT PRIMARY KEY,
	post_id INT ,
	message TEXT NOT NULL, 
	replier_id INT,
	parent_reply_id INT REFERENCES accounts(reply_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	year INT,
	month TEXT check(month in ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')),
	day INT, 
	hour INT,
	minute INT,
	FOREIGN KEY (replier_id) REFERENCES accounts(account_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (post_id) REFERENCES posts(post_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);
