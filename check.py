import sqlite3
con=sqlite3.connect("atm.db")
a= con.execute("select count (*) from balance")
for i in a :
    print(i[0])
    print (type(i[0]))
