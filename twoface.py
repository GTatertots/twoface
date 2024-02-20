#!/usr/bin/env python3

import click
import os
import sqlite3
import sys

DB_FILE = 'twoface.db'

def getdb(create=False):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    else:
        if not create:
            print('no database found')
            sys.exit(1)
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
        c.execute("INSERT INTO users (email_address) VALUES (?)", (email_addr))
        con.commit()
        con.close()

@click.command()
@click.argument('username')
@click.argument('email_addr')
def insert_account(username, email_addr): 
    with getdb() as con:
        c = con.cursor()
        c.execute("INSERT INTO accounts (username, email_address) VALUES (?, ?)", (username, email_addr))
        con.commit()
        con.close()

@click.command()
@click.argument('follower')
@click.argument('followed')
def insert_follower(follower, followed): 
    with getdb() as con: 
        c = con.cursor()
        #TODO needs to be fixed NOT (cause i fixed it)
        c.execute("INSERT INTO followers (follower, followed) VALUES ((SELECT account_id FROM account WHERE email_address = ?), (SELECT account_id FROM account WHERE email_address = ?))", (follower, followed))
        con.commit()
        con.close()

@click.command()
@click.argument('username')
@click.argument('message')
@click.argument('year')
@click.argument('month')
@click.argument('day')
@click.argument('hour')
@click.argument('minute')
def insert_post(username, message, year, month, day, hour, minute):
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO posts (message, poster_id, year, month, day, hour, minute) VALUES (?, ?, ?, ?, ?, ?, ?)", (message, poster_id, year, month, day, hour, minute))
        con.commit()
        con.close()

@click.command()
@click.argument('')
def insert_reply(post_id, message, replier_id, year, month, day, hour, minute): 
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO replies (message, post_id, replier_id, year, month, day, hour, minute) VALUES (?, ?, ?, ?, ?, ?, ?)", (message, post_id, replier_id, year, month, day, hour, minute))
        con.commit()
        con.close()

@click.command()
@click.argument('')
def insert_like(post_id, liker_id):
    with getdb() as con: 
        c = con.cursor()
        c.execute("INSERT INTO likes (post_id, liker_id) VALUES (?, ?)", (post_id, liker_id))
        con.commit()
        con.close()


cli.add_command(insert_user)
cli.add_command(insert_account)
cli.add_command(insert_follower)
cli.add_command(insert_post)
cli.add_command(insert_reply)
cli.add_command(insert_like)
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
