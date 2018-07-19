import sqlite3 as sq
con=sq.connect("atm.db")
con.execute("CREATE TABLE pass(id INTEGER NOT NULL , password VARCHAR(20) NOT NULL PRIMARY KEY)")
con.execute("CREATE TABLE trans_debit(date text,time text,id INTEGER NOT NULL , debit REAL NOT NULL)")
con.execute("CREATE TABLE trans_credit(date text,time text,id INTEGER NOT NULL , credit REAL NOT NULL)")
con.execute("CREATE TABLE balance(id INTEGER NOT NULL PRIMARY KEY, current_balance REAL)")
con.execute("CREATE TABLE details(id INTEGER NOT NULL PRIMARY KEY,name varchar(30),gender varchar(1),address varchar(50))")
con.close()
