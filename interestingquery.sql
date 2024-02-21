SELECT A.username AS greatest_liker, count(1) AS like_amount
FROM accounts,
WHERE accounts.username = ?,
JOIN posts ON
	poster_id == account_id,
JOIN likes ON 
	likes.post_id == posts.post_id,
JOIN accounts AS A ON 
	liker_id = A.account_id,
GROUP BY liker_id,
SORT BY like_amount DESC

SELECT posts.message
FROM accounts, 
JOIN followers ON
	follower_id == account_id,
JOIN posts ON
	poster_id == followed_id,

