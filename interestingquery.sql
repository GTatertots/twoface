// find greatest liker
SELECT A.username AS greatest_liker, count(1) AS like_amount
FROM accounts
JOIN posts ON
	poster_id == accounts.account_id
JOIN likes ON 
	likes.post_id == posts.post_id
JOIN accounts AS A ON 
	liker_id == A.account_id
GROUP BY liker_id
ORDER BY like_amount DESC;

// display feed
SELECT posts.message, count(1) AS likes
FROM accounts 
JOIN followers ON
	follower_id == account_id
JOIN posts ON
	poster_id == followed_id
JOIN likes ON
	likes.post_id == posts.post_id
GROUP BY likes.post_id
ORDER BY year, month, day, hour, minute DESC;

// display who has the most followers
SELECT accounts.username, count(1) as follower_count
FROM followers
JOIN accounts ON 
	followed_id == account_id
GROUP BY followed_id
ORDER BY follower_count DESC
LIMIT 10;

// display replies to post
SELECT replies.message, count(1) AS likes
FROM posts
JOIN replies ON
	replies.post_id == posts.post_id
JOIN reply_likes ON
	replies.reply_id = reply_likes.reply_id
GROUP BY reply_likes.reply_id
ORDER BY LIKES DESC;
