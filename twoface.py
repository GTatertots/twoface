#!/usr/bin/env python3

import click
import os
import sqlite3
import sys
from datetime import datetime

DB_FILE = 'twoface.db'

def getdb():
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con


@click.group()
def cli():
    pass

@click.command()
@click.argument('email_addr')
def insert_user(email_addr):
    with getdb() as con:
        c = con.cursor()
        c.execute("INSERT INTO users (email_address) VALUES (?)", (email_addr,))
        con.commit()
    print("--> created user:", email_addr)

@click.command()
@click.argument('username')
@click.argument('email_addr')
def insert_account(username, email_addr): 
    with getdb() as con:
        c = con.cursor()
        c.execute("INSERT INTO accounts (username, email_address) VALUES (?, ?)", (username, email_addr))
        con.commit()
    print("--> user ", email_addr, "created account: ", username)


@click.command()
@click.argument('follower')
@click.argument('followed')
def insert_follower(follower, followed): 
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO followers (follower_id, followed_id) VALUES ((SELECT account_id FROM accounts WHERE username = ?), (SELECT account_id FROM accounts WHERE username = ?))", (follower, followed))
        con.commit()
    print("--> user ", followed, "followed user: ", followed)

@click.command()
@click.argument('follower')
@click.argument('followed')
def unfollow(follower, followed):
    with getdb() as con: 
        c = con.cursor()
        c.execute("DELETE FROM followers WHERE follower_id = (SELECT account_id FROM accounts WHERE username = ?) AND (SELECT account_id FROM accounts WHERE username = ?)", (follower, followed))
        con.commit()
    print("--> user ", follower, "created account: ", followed)


@click.command()
@click.argument('username')
@click.argument('title')
@click.argument('message')
def insert_post(username, title, message):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour =  datetime.now().hour
    minute = datetime.now().minute
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO posts (poster_id, title, message, year, month, day, hour, minute) VALUES ((SELECT account_id FROM accounts WHERE username = ?), ?, ?, ?, ?, ?, ?, ?)", (username, title, message, year, month, day, hour, minute))
        con.commit()
    print("--> account ", username, "posted with title: ", title)

        
@click.command()
@click.argument('title')
def delete_post(title):
    with getdb() as con: 
        c = con.cursor()
        c.execute("DELETE FROM posts WHERE title = ?", (title,))
        con.commit()
    print("--> post deleted")
    

@click.command()
@click.argument('username')
@click.argument('posttitle')
@click.argument('title')
@click.argument('message')
@click.argument('reply_to_post')
def insert_reply(username, posttitle, title, message, reply_to_post):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour =  datetime.now().hour
    minute = datetime.now().minute
    with getdb() as con: 
        c = con.cursor()
        if reply_to_post == "true":
            c.execute("INSERT INTO replies (message, title, post_id, replier_id, year, month, day, hour, minute) VALUES (?, ?, (SELECT post_id FROM posts WHERE title = ?), (SELECT account_id FROM accounts WHERE username = ?), ?, ?, ?, ?, ?)", (message, title, posttitle, username, year, month, day, hour, minute))
        else:
            c.execute("INSERT INTO replies (message, title, post_id, replier_id, year, month, day, hour, minute) VALUES (?, ?, (SELECT reply_id FROM replies WHERE title = ?), (SELECT account_id FROM accounts WHERE username = ?), ?, ?, ?, ?, ?)", (message, title, posttitle, username, year, month, day, hour, minute))
        con.commit()
    print("--> user ", username, "replied to ", posttitle)

@click.command()
@click.argument('username')
@click.argument('posttitle')
def insert_like(username, posttitle):
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO likes (post_id, liker_id) VALUES ((SELECT post_id FROM posts WHERE title = ?), (SELECT account_id FROM accounts WHERE username = ?))", (posttitle, username))
        con.commit()
    print("--> user ", username, "liked ", posttitle)

@click.command()
@click.argument('username')
@click.argument('posttitle')
def reply_like(username, posttitle):
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO reply_likes (reply_id, liker_id) VALUES ((SELECT reply_id FROM replies WHERE title = ?), (SELECT account_id FROM accounts WHERE username = ?))", (posttitle, username))
        con.commit()
    print("--> user ", username, "liked ", posttitle)

@click.command()
@click.argument('posttitle')
def replies_to_post(posttitle):
    with getdb() as con: 
        c = con.cursor()
        c.execute('''SELECT accounts.username, replies.message, count(1) AS likes 
FROM posts
JOIN replies ON
	replies.post_id = posts.post_id
LEFT JOIN reply_likes ON
	replies.reply_id = reply_likes.reply_id
JOIN accounts ON
    replies.replier_id = account_id
WHERE posts.title = ?
GROUP BY reply_likes.reply_id
ORDER BY likes DESC;''', (posttitle,))
        list = c.fetchall()
        for x in list:
            print('\t',x)
        con.commit()

@click.command()
@click.argument('username')
def get_feed(username):
    with getdb() as con: 
        c = con.cursor()
        c.execute("SELECT posts.title, posts.message, count(1) AS likes FROM accounts JOIN followers ON follower_id == account_id JOIN posts ON poster_id == followed_id JOIN likes ON likes.post_id == posts.post_id WHERE accounts.username = ? GROUP BY likes.post_id ORDER BY year, month, day, hour, minute DESC", (username,))
        list = c.fetchall()
        con.commit()
        for x in list:
            print(x)
            title, _, _ = x
            replies_to_post.callback(title)


@click.command()
def most_popular():
    with getdb() as con: 
        c = con.cursor()
        c.execute(
'''SELECT accounts.username, count(1) as follower_count
FROM followers
JOIN accounts ON 
	followed_id == account_id
GROUP BY followed_id
ORDER BY follower_count DESC
LIMIT 10;''')
        list = c.fetchall()
        for x in list:
            print(x)
        con.commit()

@click.command()
@click.argument('username')
def find_stalker(username):
    with getdb() as con: 
        c = con.cursor()
        c.execute(
'''SELECT A.username AS greatest_liker, count(1) AS like_amount
FROM accounts
JOIN posts ON
	poster_id == accounts.account_id
JOIN likes ON 
	likes.post_id == posts.post_id
JOIN accounts AS A ON 
	liker_id == A.account_id
WHERE accounts.username = ? 
GROUP BY liker_id
ORDER BY like_amount DESC;
''', (username,))
        list = c.fetchall()
        for x in list:
            print(x)
        con.commit()

cli.add_command(insert_user)
cli.add_command(insert_account)
cli.add_command(insert_follower)
cli.add_command(insert_post)
cli.add_command(insert_reply)
cli.add_command(insert_like)
cli.add_command(reply_like)
cli.add_command(get_feed)
cli.add_command(unfollow)
cli.add_command(delete_post)
cli.add_command(most_popular)
cli.add_command(find_stalker)
cli.add_command(replies_to_post)
cli()

#def main():
#    parser = argparse.ArgumentParser(
#            prog = 'TwoFace Interface',
#            description = 'UI for TwoFace social network')
#    subparsers = parser.add_subparsers(help='sub-command help')
#
#    parser_insert_user = subparsers.add_parser('insertuser',help='adds a user')
#    parser_insert_user.add_argument('email')
#    parser_insert_user.set_defaults(func=add_user)
#    args = parser.parse_args()
#
#    print(args,filename,args.count,args.verbose)
#
#
#
#import click
#import os
#import sqlite3
#import sys
#
#DB_FILE = 'twoface.db'
#
#def getdb(create=False):
#    if os.path.exists(DB_FILE):
#        if create:
#            os.remove(DB_FILE)
#    else:
#        if not create:
#            print('no database found')
#            sys.exit(1)
#    con = sqlite3.connect(DB_FILE)
#    con.execute('PRAGMA foreign_keys = ON')
#    return con
#
#@click.group()
#def cli():
#    pass
#
#@click.command()
#@click.argument('email')
#def adduser(email):
#    print('creating user with email address', email)
#    with getdb() as con:
#        cursor = con.cursor()
#        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
#        id = cursor.lastrowid
#        print(f'inserted with id={id}')
#
#@click.command()
#@click.argument('email')
#@click.argument('username')
#def addaccount(email, username):
#    print('creating account with username', username, 'for email', email)
#    with getdb() as con:
#        cursor = con.cursor()
#        cursor.execute('''INSERT INTO accounts (user_id, username)
#VALUES ((SELECT id FROM users WHERE email = ?), ?)''', (email, username))
#        id = cursor.lastrowid
#        print(f'inserted with id={id}')
#
#
#
#cli.add_command(adduser)
#cli.add_command(addaccount)
#cli()
