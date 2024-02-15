#!/usr/bin/env python3

import argparse
import sqllite



def insert_user(database_name, email_addr):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO users (email_address) VALUES (?)", (email_addr))
    conn.commit()
    conn.close()


def insert_account(database_name, username, email_addr, account_id):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO accounts (username, email_address, account_id) VALUES (?, ?, ?)", (username, email_addr, account_id))
    conn.commit()
    conn.close()

def insert_follower(database_name, follower, followed):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO followers (follower, followed) VALUES (?, ?)", (follower, followed))
    conn.commit()
    conn.close()

def insert_post(database_name, message, poster_id, year, month, day, hour, minute):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO posts (message, poster_id, year, month, day, hour, minute) VALUES (?, ?, ?, ?, ?, ?, ?)", (message, poster_id, year, month, day, hour, minute))
    conn.commit()
    conn.close()

def insert_follower(database_name, poster_id, liker_id):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO followers (poster_id, liker_id) VALUES (?, ?)", (poster_id, liker_id))
    conn.commit()
    conn.close()

def insert_reply(database_name, post_id, message, replier_id, year, month, day, hour, minute):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO replies (message, post_id, replier_id, year, month, day, hour, minute) VALUES (?, ?, ?, ?, ?, ?, ?)", (message, post_id, replier_id, year, month, day, hour, minute))
    conn.commit()
    conn.close()

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
#def create():
#    with getdb(create=True) as con:
#        con.execute(
#'''CREATE TABLE users (
#    id          INTEGER PRIMARY KEY,
#    email       TEXT NOT NULL
#)''')
#        con.execute(
#'''CREATE UNIQUE INDEX users_email ON users (email)''')
#
#        con.execute(
#'''CREATE TABLE accounts (
#    id          INTEGER PRIMARY KEY,
#    user_id     INTEGER NOT NULL,
#    username    TEXT NOT NULL,
#
#    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
#)''')
#    print('database created')
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
#cli.add_command(create)
#cli.add_command(adduser)
#cli.add_command(addaccount)
#cli()
##import sqlite3
##
##con = sqlite3.connect("twoface.db")
##cur = con.cursor()
##
##def main():
##    parser = argparse.ArgumentParser(
##            prog = 'TwoFace Interface',
##            description = 'UI for TwoFace social network')
##    subparsers = parser.add_subparsers(help='sub-command help')
##
##    parser_create = subparsers.add_parser('create',help='create the database')
##
##    args = parser.parse_args()
##
##    print(args,filename,args.count,args.verbose)
#
