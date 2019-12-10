# Fall, 2019, CSc 32200, Professor Jie Wei
# FoodProject
#This is the final project for csc 322 (Software Engineering Course)  

#Project Team MEMBER:
#                    Shahan Rahman,
#                    Hasibul Islam,
#                    Eftekher Husain,
#                    Daniel Lee
import pandas

def chef_catalog():
    chefs = pandas.read_csv("data/users.csv")
    chefs = chefs.loc[(chefs["level"]==4) & (chefs["approved"]==1)]
    return (chefs["name"].values, chefs["uid"].values)

def menu_catalog(input):
    did_database = pandas.read_csv("data/menu.csv")
    did_database = did_database.loc[(did_database["uid"]==input) | (did_database["uid"]==-1)]
    return (list(reversed(did_database.sort_values("time")["did"].values)))

def image_catalog(input):
    path_database = pandas.read_csv("data/menu.csv")
    path_database = path_database.loc[(path_database["uid"]==input) | (path_database["uid"]==-1)]
    return (list(reversed(path_database.sort_values("time")["path"].values)))

def name_catalog(input):
    name_database = pandas.read_csv("data/menu.csv")
    name_database = name_database.loc[(name_database["uid"]==input) | (name_database["uid"]==-1)]
    return (list(reversed(name_database.sort_values("time")["dish"].values)))

def price_catalog(input):
    price_database = pandas.read_csv("data/menu.csv")
    price_database = price_database.loc[(price_database["uid"]==input) | (price_database["uid"]==-1)]
    return (list(reversed(price_database.sort_values("time")["price"].values)))

def high_image_catalog(input):
    image_list = []
    image_database = pandas.read_csv("data/meal.csv")
    for e in input:
        image_list.append(image_database.loc[image_database["did"]==e]["path"].iloc[0])
    return image_list

def high_name_catalog(input):
    name_list = []
    name_database = pandas.read_csv("data/meal.csv")
    for e in input:
        name_list.append(name_database.loc[name_database["did"]==e]["dish"].iloc[0])
    return name_list

def high_price_catalog(input):
    price_list = []
    price_database = pandas.read_csv("data/meal.csv")
    for e in input:
        price_list.append(price_database.loc[price_database["did"]==e]["price"].iloc[0])
    return price_list