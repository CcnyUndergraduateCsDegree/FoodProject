# Fall, 2019, CSc 32200, Professor Jie Wei
# FoodProject
#This is the final project for csc 322 (Software Engineering Course)  

#Project Team MEMBER:
#                    Shahan Rahman,
#                    Hasibul Islam,
#                    Eftekher Husain,
#                    Daniel Lee
import pandas
import numpy
from tkinter import *
from tkinter import messagebox

def validate(username_input,password_input):
    users_database = pandas.read_csv("data/users.csv")
    users_username_database = users_database["username"].values
    users_password_database = users_database["password"].values
    users_uid_database = users_database["uid"].values
    users_level_database = users_database["level"].values
    users_approved_database = users_database["approved"].values
    i=0
    for username_check in users_username_database:
        if username_check == username_input:
            if users_approved_database[i] == 0:
                messagebox.showwarning("", "Account is waiting approval. Please Wait")
                return 10
            else:
                if users_password_database[i] == password_input and \
                users_approved_database[i] == 1:
                    return (users_level_database[i],users_uid_database[i])
                else:
                    return False
        i+=1
    return False

def retrieve(email_input):
    users_database = pandas.read_csv("data/users.csv")
    users_username_database = users_database["username"].values
    users_password_database = users_database["password"].values
    users_email_database = users_database["email"].values
    i=0
    for email_check in users_email_database:
        if email_check == email_input:
            return (users_username_database[i],",",users_password_database[i])
        i+=1
    return ("?",",","?")

def register(username_input,password_input,email_input):
    users_database = pandas.read_csv("data/users.csv")
    users_username_database = users_database["username"].values.tolist()
    users_password_database = users_database["password"].values.tolist()
    users_balance_database = users_database["balance"].values.tolist()
    users_email_database = users_database["email"].values.tolist()
    users_level_database = users_database["level"].values.tolist()
    users_uid_database = users_database["uid"].values.tolist()
    users_cart_database = users_database["cart"].values.tolist()
    users_name_database = users_database["name"].values.tolist()
    users_approved_database = users_database["approved"].values.tolist()
    users_warning_database = users_database["warning"].values.tolist()
    users_spent = users_database["spent"].values.tolist()
    orders_amount = users_database["orders"].values.tolist()
    if username_input == "" or password_input == "" or email_input == "":
        return ("Please fill out all information")
    for u,e in zip(users_username_database,users_email_database):
        if u == username_input or e == email_input:
            return ("Username or Email is registered already")
    users_username_database.append(username_input)
    users_password_database.append(password_input)
    users_email_database.append(email_input)
    users_balance_database.append(50)
    users_level_database.append(1)
    users_uid_database.append(users_uid_database[-1]+1)
    users_approved_database.append(0)
    users_warning_database.append(0)
    users_cart_database.append(numpy.nan)
    users_name_database.append(numpy.nan)
    users_spent.append(0)
    orders_amount.append(0)
    users_database = pandas.DataFrame({"username": users_username_database,
                                        "password": users_password_database,
                                        "balance": users_balance_database,
                                        "email": users_email_database,
                                        "level": users_level_database,
                                        "uid": users_uid_database,
                                        "cart": users_cart_database,
                                        "name": users_name_database,
                                        "approved": users_approved_database,
                                        "warning": users_warning_database,
                                        "spent": users_spent,
                                        "orders": orders_amount})
    users_database = users_database[["username",
                                    "password",
                                    "balance",
                                    "email",
                                    "level",
                                    "uid",
                                    "cart",
                                    "name",
                                    "approved",
                                    "warning",
                                    "spent",
                                    "orders"]]
    users_database.to_csv("data/users.csv", index=False)
    return ("Congrats You Are Registered")

def register_employee(t, name, username, password, email):
    users_database = pandas.read_csv("data/users.csv")
    users_username_database = users_database["username"].values.tolist()
    users_password_database = users_database["password"].values.tolist()
    users_balance_database = users_database["balance"].values.tolist()
    users_email_database = users_database["email"].values.tolist()
    users_level_database = users_database["level"].values.tolist()
    users_uid_database = users_database["uid"].values.tolist()
    users_cart_database = users_database["cart"].values.tolist()
    users_name_database = users_database["name"].values.tolist()
    users_approved_database = users_database["approved"].values.tolist()
    users_warning_database = users_database["warning"].values.tolist()
    users_spent = users_database["spent"].values.tolist()
    orders_amount = users_database["orders"].values.tolist()
    if name == "" or username == "" or password == "" or email == "":
        messagebox.showwarning("", "Please fill out all information")
        return False
    for u,e in zip(users_username_database,users_email_database):
        if u == username or e == email:
            messagebox.showwarning("", "Username or Email is registered already")
            return False
    users_username_database.append(username)
    users_password_database.append(password)
    users_email_database.append(email)
    users_balance_database.append(numpy.nan)
    if t == 1:
        users_level_database.append(4)
        edit_menu = pandas.read_csv("data/menu.csv")
        edit_menu.loc[len(edit_menu)] = [users_uid_database[-1]+1, -1, -1, "etc", 0, "images/etc.gif"]
        edit_menu.to_csv("data/menu.csv", index=False)
    else:
        users_level_database.append(3)
    users_uid_database.append(users_uid_database[-1]+1)
    users_approved_database.append(1)
    users_warning_database.append(numpy.nan)
    users_cart_database.append(numpy.nan)
    users_name_database.append(name)
    users_spent.append(numpy.nan)
    orders_amount.append(numpy.nan)
    users_database = pandas.DataFrame({"username": users_username_database,
                                        "password": users_password_database,
                                        "balance": users_balance_database,
                                        "email": users_email_database,
                                        "level": users_level_database,
                                        "uid": users_uid_database,
                                        "cart": users_cart_database,
                                        "name": users_name_database,
                                        "approved": users_approved_database,
                                        "warning": users_warning_database,
                                        "spent": users_spent,
                                        "orders": orders_amount})
    users_database = users_database[["username",
                                    "password",
                                    "balance",
                                    "email",
                                    "level",
                                    "uid",
                                    "cart",
                                    "name",
                                    "approved",
                                    "warning",
                                    "spent",
                                    "orders"]]
    users_database.to_csv("data/users.csv", index=False)
    salary_database = pandas.read_csv("data/paycheck.csv")
    salary_uid = salary_database["uid"].values.tolist()
    salary_salary = salary_database["salary"].values.tolist()
    salary_complaints = salary_database["complaints"].values.tolist()
    salary_compliments = salary_database["compliments"].values.tolist()
    salary_demoted = salary_database["demoted"].values.tolist()
    salary_salary.append(100)
    salary_uid.append(users_uid_database[-1])
    salary_complaints.append(0)
    salary_compliments.append(0)
    salary_demoted.append(0)
    salary_database = pandas.DataFrame({"uid": salary_uid,
                                        "salary": salary_salary,
                                        "complaints": salary_complaints,
                                        "compliments": salary_compliments,
                                        "demoted": salary_demoted})
    salary_database = salary_database[["uid", "salary", "complaints", "compliments", "demoted"]]
    salary_database.to_csv("data/paycheck.csv", index=False)
    messagebox.showinfo("", "Successful added")
    return True