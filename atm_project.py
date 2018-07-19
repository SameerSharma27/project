## atm with database project.
import sqlite3 as sq
from datetime import datetime##to get current time and date
import os
import time
import welcome


class Error(Exception):
    pass
class name_null(Error):
    pass
class incorrect_gender_format(Error):
    pass
class passwordTooSmall(Error):
    pass
class address_notnull(Error):
    pass
class insufficientFunds(Error):
    pass
class idLengthIncorrect(Error):
    pass

con=sq.connect("atm.db")
default_login=None
def main_menu():
    os.system('CLS')##this function clears screen in command prompt
    welcome.welcome()
    print("""
    1.Create NEW ACCOUNT
    2.LOGIN to existing account
    3.EXIT
    """,end="\n\n")
    try:
        a=int(input("    Please Input the Choice    "))
    except ValueError:
        print("\n\n    Please enter a valid choice(1/2/3)\n\n")
        os.system("pause")
        main_menu()
    else:
        os.system('CLS') 
        if a==1:
            new_account()
        elif(a==2):
            login(default_login)
        elif(a==3):
            exit_transaction()
        else:
            print("\n    Please enter a valid choice")
            os.system("pause")
            main_menu()

def new_account():
    ##how to declare sttatic variables? 
    count_account=1111111111
    cursor=con.execute("SELECT COUNT(*) FROM details")
    for i in cursor:
        addfactor=i[0]
    ## to generate a new account number everytime we count total number of accounta already present then add that number to 1111111111    
    count_account+=addfactor
    os.system('CLS')
    try:
        #########################################check for valid name###############################
        name=input("Please enter your good name    ")
        if not name:
            raise name_null
        gender=input("please enter your gender (M/F)    ")
        if not (gender=='m'or gender=='M'or gender=='f'or gender=='F'):
            raise incorrect_gender_format
        address=input("please enter your address    ")
        if not address:
            raise address_notnull
        password=input("please enter the password you want(password length should be 6 or more)    ")
        if len(password)<6:
            raise passwordTooSmall
    except name_null:
        print("\nYou cant leave your name null.Retry opening an account")
        os.system("pause")
        new_account()
    except incorrect_gender_format:
        print("\nPlease enter from (m/f) only for gender")
        os.system("pause")
        new_account()
    except address_notnull:
        print("\nyou cant leave your address empty")
        os.system("pause")
        new_account()
    except passwordTooSmall:
        print("\nLength of password should be more than 6 characters")
        os.system("pause")
        new_account()
    else:
        con.execute("INSERT INTO details(id,name,gender,address)values(?,?,?,?)",(count_account,name,address,gender))
        con.execute("INSERT INTO pass(id,password)values(?,?)",(count_account,password))##entered id and password of new usere into pass table
        con.execute("INSERT INTO balance(id,current_balance)values(?,?)",(count_account,0.0))##entered balance of new user into balance table
        os.system('CLS')
        display_id(count_account,password)
        print("\n\nCongratulations!!!! you have successfully opened a ***ZERO BALANCE ACCOUNT*** account")
        con.commit()
        os.system("pause")
        main_menu()


def login(login_id):
    os.system('CLS')
    if login_id==None:
        print("WELCOME TO THE LOGIN WINDOW",end="\n\n\n")
        try:
            login_id=int(input("Please enter your id    "))
            if len(str(login_id))!=10:
                raise idLengthIncorrect
        except ValueError:
                print("\n\nPlease enter a valid ID\n\n")
                os.system("pause")
                login(None)
        except idLengthIncorrect:
            print("\n\n\nincorrect ID")
            os.system("pause")
            login(None)
        ##if i do not put the remaining thing into the else part then after catching error it will execute rest of the code so beware of that
        else:
            login_password=input("Please enter your Password    ")
            row= con.execute("SELECT id,password FROM pass WHERE pass.id= ? and pass.password=? ",(login_id,login_password))
            check=0
            for i in row:
                check=1
                break
            if check==0: 
                print("\n\nPlease enter valid id and password or if you have not yet registered please do get registered",end="\n\n\n")
                os.system("pause")
                main_menu()
            
    
    os.system('CLS')
    print("""Please select from the following options\n\n
    1.DEPOSIT cash  
    2.WITHDRAWL
    3.Transaction History
    4.Check BALANCE
    5.CHANGE PASSWORD 
    6.MAIN MENU
    7.EXIT
    """)
    try:
        a=int(input("\n\nPlease enter the operation you want to perform    "))
    except ValueError:
        print("\n\nplease enter valid choice\n\n")
        os.system("pause")
        login(login_id)
        
    if a==1:
        deposit_cash(login_id)
    elif a==2:
        cash_withdrawl(login_id)
    elif a==3:
        transaction_history(login_id)
    elif a==4:
        check_balance(login_id)
    elif a==5:
        change_password(login_id)
    elif a==6:
        main_menu()
    elif a==7:
        exit_transaction()
    else :
        print("\n\nplease enter a valid choice")
        os.system("pause")
        login(login_id)
            
def exit_transaction():## to exit from the program
    os.system('CLS')
    print("Transaction completed")
    exit()

def deposit_cash(login_id):
    os.system('CLS')
    try:
        credit=float(input("please enter the amount of cash you want to deposit    "))
    except ValueError:
        print("\n\nPlease enter a valid amount\n\n")
        os.system("pause")
        deposit_cash(login_id)
    else:
        con.execute("UPDATE balance set current_balance=current_balance + ?  WHERE balance.id=?",(credit,login_id))##updated the table with new balance
        con.execute("INSERT INTO trans_credit (date,time,id,credit)values(?,?,?,?)",(datetime.now().strftime('%Y-%m-%d'),datetime.now().strftime("%H:%M:%S"),login_id,credit))##unique constrain fails if same amount is deposited in same account twice ,so date and time columns are required to make every constraint unique
        con.commit()
        os.system('CLS')
        print("AMOUNT DEPOSITED SUCCESSFULLY")
        os.system("pause")
        login(login_id)


def cash_withdrawl(login_id):
    os.system('CLS')
    a= con.execute("SELECT  current_balance FROM balance WHERE balance.id=?",(login_id,))
    for i in a:
        check_balance=i[0]
        break 
    try:
        debit=float(input("please enter the amount you want to withdraw    "))
        if debit>check_balance:
            raise insufficientFunds
        
    except ValueError:
        print("\n\nPlease enter a valid amount\n\n")
        os.system("pause")
        cash_withdrawl(login_id)
    except insufficientFunds:
        print("\n\nyou have Insufficient Funds")
        os.system("pause")
        main_menu()
    else:    
        con.execute("UPDATE balance set current_balance=current_balance - ? WHERE balance.id=?",(debit,login_id))##updated the amount after withdrawl
        con.execute("INSERT INTO trans_debit (date,time,id,debit)values(?,?,?,?)",(datetime.now().strftime('%Y-%m-%d'),datetime.now().strftime("%H:%M:%S"),login_id,debit))
        con.commit()
        os.system('CLS')
        print("AMOUNT WITHDRAWN SUCCESSFULLY")
        os.system("pause")
        login(login_id)


def transaction_history(login_id):
    os.system('CLS')
    trans_credit(login_id)
    trans_debit(login_id)
    a=input("\n\n\n\t\t\tPress any key to continue")
    login(login_id)

def trans_credit(login_id):
    result=con.execute("SELECT date,credit FROM trans_credit WHERE trans_credit.id= ?",(login_id,))## here "," is necessary to make the argument a tuple otherwise it will be treated as a sequence of characters and If that string is 74 characters long, then Python sees that as 74 separate bind values, each one character long.
    print("credit details \n")
    for i in result :
        print(i[0],end="    ", sep='')
        print(i[1],end=" Rs\n")

def trans_debit(login_id):
    result=con.execute("SELECT date,debit FROM trans_debit WHERE trans_debit.id= ?",(login_id,))## here "," is necessary to make the argument a tuple otherwise it will be treated as a sequence of characters and If that string is 74 characters long, then Python sees that as 74 separate bind values, each one character long.
    print("\n\ndebit details \n")
    for i in result :
        print(i[0],end="    ",sep='')
        print(i[1],end=" Rs\n")

def check_balance(login_id):
    os.system('CLS')
    balance=con.execute("SELECT current_balance FROM balance WHERE balance.id=?",(login_id,))## without "," argument for the placeholder will be treated as a sequence of characters and  not a tuple which is the required argument

    for i in balance:
        print("Your Current Balance is  ", i[0],end=" Rs\n")
    os.system("pause")
    login(login_id)

def change_password(login_id):
    os.system('CLS')
    new_password=input("please enter the new password (length should be 6 or more)   ")
    try:
        
        if(len(new_password)<6):
            raise passwordTooSmall
    except passwordTooSmall:
        print("\n\n\t please enter password of length 6 or more")
        os.system("pause")
        change_password(login_id)
    try:
        con.execute("UPDATE pass SET password=? WHERE id= ?",(new_password,login_id))
    except Exception:
        print("\n\n\t this password is unavailable due to technical reasons")
        os.system("pause")
        change_password(login_id)
        
    con.commit()
    os.system('CLS')
    print("password changed successfully")
    os.system("pause")
    main_menu()

def display_id(accountnumber,password):
    print("\n\n\t\t PLEASE NOTE DOWN YOUR ACCOUNT CREDENTIALS\n\n")
    print("your id is :          ", accountnumber)
    print("your password is :    ",password)
    print("\n\t\tPLEASE KEEP YOUR ID AND PASSWORD CONFIDENTIAL!!!!!",end="\n\n\n        ")
    continue_process=input("hit enter to continue")
    
    


main_menu()














        
      
      





























