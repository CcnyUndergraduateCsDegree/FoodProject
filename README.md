# Fall, 2019, CSc 32200, Professor Jie Wei
# FoodProject
This is the final project for csc 322 (Software Engineering Course)  

Project Team MEMBER:
                    Shahan Rahman,
                    Hasibul Islam,
                    Eftekher Husain,
                    Daniel Lee


![FASTLaneFood](https://user-images.githubusercontent.com/36207058/67982589-61ef1e00-fbf9-11e9-8c8c-397210670091.png)

# Given Specification: 
        5 user types
        
- [X] Managers/Superusers :
  - [X] Pays of cooks and delivery people
  - [X] Handles Complaints and Management of Customers
  - [X] Can approve/deny customers
- [X] Cooks
  - [X] Can Post new items on menu
  - [X] Each store has at least two cooks.
- [X] Delivery People
  - [X] Bid on deliveries
  - [X] Decide route to and from the restaurant
- [X] Customers
  - [X] Can order, and pay.
  - [X] Evaluate food
  - [X] Evaluate Delivery People
  - [X] Can be blacklisted from stores
  - [X] Store history of purchases
  - [X] Customer Types per Store (determines price):
  - [X] Visitors
  - [X] Registered Customers
  - [X] VIPs
- [ ] Salespeople
  - [ ] Deal with suppliers maximizing best food supplies and prices
  - [ ] Each store has at least two
  
On Visit
- [X] Customer can login anytime they want too.
- [X] If not logged in, treated as visitor. Can always log in.
- [X] Store manager must approve registered customer (the manager can check the customer record).
- [X] Blacklisted gives manager option to be declined.

On ordering
- [X] Restaurant Lists most relevant 3 food choices based on order history for VIPs and Registered Customer.
- [X] Customer can choose food.
- [X] Registered Customers recieve discounted prices.
- [X] VIPs are registered and get a discount.
- [X] Visitors can read but not post ratings.

On order submit
- [X] After customer submits choice, delivery person can see route and determine if it is a good choice.
- [X] Accept lowest asking price bidder
  - [X] The delivery person then decides which route to go for this transaction based on traffic on the road: the algorithm decides the optimal route, assuming each segment of street can be randomly assigned to be of type good, busy, and closed.

After order finished, customer can:
- [X] Rate food/cook from 1-5.
- [X] Rate delivery person from 1-5.
- [X] If rating < 3, then views as a complaint and should be asked to provide reason.
- [X] Delivery person can rate the customer as well right after delivery 

Delivery Person 
- [X] When given an average rating < 2 for last 3 deliveries, recieves a warning which can be erased by manager.
- [X] More than 3 warnings leads to layoff.

Food/Cook 
- [X] A food item recieving average rating < 2 in last 3 orders is dropped.
- [X] The cook whose food was dropped twice will be warned.
- [X] A cook with 3 warnings will be laid off.

Sales Person 
- [ ] When recieving 3 straight 5's, recieve 10% raise.
- [ ] If the supplies ordered complained by cooks 3 times, sales person recieve a warning and 10% commission reduction.
- [ ] Laid off after 3 warnings.

Special Requirement
- [ ] Voice-based order feature should be avaliable.
      ### NOTE
          Voice order was too much for our group but we decided to have a graphic interface. 

OUR CHOSEN EXTRA FEATURE:
- [X] GUI using tkinter python


## Current Plan (Subject to change): Technologies
    - Python3 
    - Tkinter
     - PLT

## How to run
Download the required libraries.


### Database
Our database was using xml files to store all types of data. 



### FINAL NOTES
This project is only on local computers and must be downloaded 
