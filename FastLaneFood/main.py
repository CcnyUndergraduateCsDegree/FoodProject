# Fall, 2019, CSc 32200, Professor Jie Wei
# FoodProject
#This is the final project for csc 322 (Software Engineering Course)  

#Project Team MEMBER:
#                    Shahan Rahman,
#                    Hasibul Islam,
#                    Eftekher Husain,
#                    Daniel Lee
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image
#All Imports needed for project
import login
import catalog
import object
import manager
import store
import maptarget

program = Tk()
program.title("FastLaneFood")
program.resizable(width=False, height=False)

menucatalog = Menu(program)
chef_list = Menu(menucatalog, tearoff=0)
menucatalog.add_cascade(label="Menus", menu=chef_list)
program.config(menu=menucatalog)

#Setting up Variables
class user:
    def __init__(self):
        self.user_level = 0
        self.storeping_cart = []
        self.current_menu = []
        self.top_menu = []
        self.total = 0
        self.uid = -1

class parameter:
    def __init__(self):
        self.menu_max_page = 1
        self.menu_current_page = 1
        self.chef_list = []
        self.menu_list = []
        self.image_list = []
        self.name_list = []
        self.price_list = []
        self.current_chef_uid = -1
        self.current_chef_name = "All"
        self.employee_type = 0
        self.current_cart_page = 1
        self.max_cart_page = 1
        self.storeping_did_list = []
        self.storeping_quantity_list = []
        self.storeping_name_list = []
        self.storeping_price_list = []
        self.storeping_image_list = []
        self.available_dish = []
        self.added_dish = []
        self.star_food_rate = 0
        self.star_delivery_rate = 0
        self.alldish = []

global current_parameter
global current_user
current_parameter = parameter()
current_user = user()

temp = catalog.chef_catalog()
current_parameter.chef_list = temp
chef_list.delete(0,END)
chef_list.add_command(label="All", command=lambda: catalog_change_menu("all","All"))
chef_list.add_command(label="Top", command=lambda: catalog_change_menu("top","Top"))
for e,f in zip(temp[0],temp[1]):
    chef_list.add_command(label=str(e), command=lambda uid=f,name=e: catalog_change_menu(uid,name))

def comment_interface():
    reset_gui()
    order_history_label.grid(row=0, column=0)
    combined_rate_frame.grid(row=0, column=1, rowspan=2)
    rate_order_list.grid(row=1, column=0)
    refresh_comment()

def refresh_comment():
    for e in star_food_list:
        e.config(image=star_b)
    for e in star_delivery_list:
        e.config(image=star_b)
    rate_order_list.delete(0,END)
    for e in object.get_ddid_list(current_user.uid):
        rate_order_list.insert(END, e)
    current_parameter.star_food_rate = 0
    current_parameter.star_delivery_rate = 0
    rate_comment.delete(0,END)

def submit_rating():
    if current_parameter.star_food_rate == 0 or current_parameter.star_delivery_rate == 0:
        messagebox.showwarning("","Please rate food and delivery from 1 star to 5 stars")
    else:
        result = messagebox.askyesno("", "Food: "+str(current_parameter.star_food_rate)+"\nDelivery: "
                                    +str(current_parameter.star_delivery_rate)+"\nComment: "+str(rate_comment.get())+
                                    "\nConfirm?")
        if result:
            try:
                order_did = object.get_did_list(rate_order_list.get(rate_order_list.curselection()))
                object.save_comment(current_parameter.star_delivery_rate, current_parameter.star_food_rate,
                                     current_user.uid, order_did, rate_comment.get())
                object.save_rating(current_parameter.star_food_rate, order_did, current_user.user_level)
                object.delivery_rating(current_parameter.star_delivery_rate, rate_order_list.get(rate_order_list.curselection()))
                refresh_comment()
            except TclError:
                messagebox.showwarning("", "Please select an order to rate")

def star_food_change(num):
    for e in star_food_list:
        e.config(image=star_b)
    i=0
    while i<num:
        star_food_list[i].config(image=star_c)
        i+=1
    current_parameter.star_food_rate = num

def star_delivery_change(num):
    for e in star_delivery_list:
        e.config(image=star_b)
    i=0
    while i<num:
        star_delivery_list[i].config(image=star_c)
        i+=1
    current_parameter.star_delivery_rate = num

def refresh_menu(input):
    temp = catalog.chef_catalog()
    current_parameter.chef_list = temp
    chef_list.delete(0,END)
    chef_list.add_command(label="All", command=lambda: catalog_change_menu("all","All"))
    chef_list.add_command(label="Top", command=lambda: catalog_change_menu("top","Top"))
    for e,f in zip(temp[0],temp[1]):
        chef_list.add_command(label=str(e), command=lambda uid=f,name=e: catalog_change_menu(uid,name))
    if input == 1:
        if current_parameter.current_chef_uid != -1:
            catalog_change_menu(current_parameter.current_chef_uid,current_parameter.current_chef_name)
        else:
            catalog_change_menu("all",current_parameter.current_chef_name)

def catalog_change_menu(uid,name):
    if uid == "all":
        current_parameter.current_chef_uid = uid
        current_parameter.current_chef_name = name
        chef_name.config(text=current_parameter.current_chef_name)
        start_interface()
    elif uid == "top":
        if current_user.uid == -1:
            messagebox.showwarning("", "Please log in first")
        else:
            current_parameter.current_chef_uid = uid
            current_parameter.current_chef_name = name
            chef_name.config(text=current_parameter.current_chef_name)
            top_menu_list(object.get_top_listing(current_user.uid))
    elif object.menu_check(uid):
        messagebox.showwarning("", "This chef has not yet added any dishes to the menu")
    else:
        current_parameter.current_chef_uid = uid
        current_parameter.current_chef_name = name
        chef_name.config(text=current_parameter.current_chef_name)
        current_parameter.menu_list = catalog.menu_catalog(uid)
        current_parameter.image_list = catalog.image_catalog(uid)
        current_parameter.name_list = catalog.name_catalog(uid)
        current_parameter.price_list = catalog.price_catalog(uid)
    if (len(current_parameter.menu_list)-1) % 6 == 0:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6)
    else:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6 + 1)
    current_parameter.menu_current_page = 1
    page_change()
    display_menu()

def top_menu_list(did_list):
    if len(did_list) == 0:
        messagebox.showwarning("", "Please make some purchases first")
    else:
        current_parameter.menu_list = did_list
        current_parameter.image_list = catalog.high_image_catalog(did_list)
        current_parameter.name_list = catalog.high_name_catalog(did_list)
        current_parameter.price_list = catalog.high_price_catalog(did_list)

def set_parameter():
    current_parameter.menu_list = object.menu_catalog()
    current_parameter.image_list = object.image_catalog()
    current_parameter.name_list = object.name_catalog()
    current_parameter.price_list = object.price_catalog()
    if (len(current_parameter.menu_list)-1) % 6 == 0:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6)
    else:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6 + 1)
    current_parameter.menu_current_page = 1
    
def reset_gui():
    image_entry.delete(0,END)
    profile_deposit.delete(0,END)
    search_entry.delete(0,END)
    login_username_entry.delete(0,END)
    login_password_entry.delete(0,END)
    login_forget_entry.delete(0,END)
    register_password_entry.delete(0,END)
    register_username_entry.delete(0,END)
    register_email_entry.delete(0,END)
    label_quantity_entry.delete(0,END)
    rate_order_list.delete(0,END)
    dish_name_entry.delete(0,END)
    price_entry.delete(0,END)
    description_entry.delete(0,END)
    image_entry.delete(0,END)
    for widget in program.winfo_children():
        widget.grid_remove()

def login_confirm_button_action():
    login_confirm_result = login.validate(login_username_entry.get(),
                                            login_password_entry.get())
    if login_confirm_result == 10:
        login_username_entry.delete(0,END)
        login_password_entry.delete(0,END)
    else:
        if login_confirm_result == False:
            messagebox.showwarning("","Username or Password is incorrect")
            login_username_entry.delete(0,END)
            login_password_entry.delete(0,END)
        elif login_confirm_result[0] == 1 or login_confirm_result[0] == 2:
            current_user.uid = login_confirm_result[1]
            current_user.user_level = login_confirm_result[0]
            current_user.storeping_cart = store.get_cart(current_user.uid)
            update_total()
            start_interface()
        elif login_confirm_result[0] == 3:
            current_user.user_level = 3
            delivery_interface()
        elif login_confirm_result[0] == 4:
            current_user.user_level = 4
            current_user.uid = login_confirm_result[1]
            chef_interface()
        elif login_confirm_result[0] == 5:
            current_user.user_level = 5
            manager_interface()

def chef_interface():
    reset_gui()
    available_dish_list.grid(row=2, column=0)
    available_dish_list.delete(0,END)
    add_new_dish_button.grid(row=0, column=0)
    signout_button.grid(row=0, column=2)
    current_dish_list.grid(row=2, column=2)
    current_dish_list.delete(0,END)
    available_dish_label.grid(row=1, column=0)
    current_dish_label.grid(row=1, column=2)
    chef_frame.grid(row=2, column=1)
    save_menu_button.grid(row=3, column=2)
    object.get_edit_menu(current_user.uid)
    temp_list = object.get_edit_menu(current_user.uid)
    current_parameter.available_dish = temp_list[0]
    current_parameter.added_dish = temp_list[1]
    for e in current_parameter.available_dish:
        available_dish_list.insert(END, e)
    for e in current_parameter.added_dish:
         if e != -1:
            current_dish_list.insert(END, e)

def add_new_dish_interface():
    reset_gui()
    add_back_button.grid(row=0, column=1)
    dish_name_label.grid(row=1, column=0)
    price_label.grid(row=2, column=0)
    description_label.grid(row=3, column=0)
    image_label.grid(row=4, column=0)
    save_button.grid(row=5, column=1)
    dish_name_entry.grid(row=1, column=1)
    price_entry.grid(row=2, column=1)
    description_entry.grid(row=3, column=1)
    image_path.grid(row=4, column=1)

def select_file():
    filename = askopenfilename()
    image_entry.config(state=NORMAL)
    image_entry.delete(0,END)
    image_entry.insert(0, filename)
    image_entry.config(state=DISABLED)

def update_edit_menu():
    available_dish_list.delete(0,END)
    current_dish_list.delete(0,END)
    for e in current_parameter.available_dish:
        available_dish_list.insert(END, e)
    for e in current_parameter.added_dish:
        if e != -1:
            current_dish_list.insert(END, e)

def save_menu_action():
    object.save_edit_menu(current_parameter.added_dish, current_user.uid)

def add_dish():
    try:
        item = available_dish_list.get(available_dish_list.curselection())
        current_parameter.available_dish.remove(int(item))
        current_parameter.added_dish.append(int(item))
    except TclError:
        messagebox.showwarning("", "Select an available dish to add")
    update_edit_menu()

def remove_dish():
    try:
        item = current_dish_list.get(current_dish_list.curselection())
        current_parameter.added_dish.remove(int(item))
        current_parameter.available_dish.append(int(item))
    except TclError:
        messagebox.showwarning("", "Select a current dish to remove")
    update_edit_menu()

def login_forget_button_action():
    reset_gui()
    login_forget_label.grid(row=0, column=0)
    login_forget_entry.grid(row=0, column=1)
    login_retrive_button.grid(row=1, column=1)
    forget_back_button.grid(row=1, column=0)

def login_retrieve_button_action():
    messagebox.showinfo("",login.retrieve(login_forget_entry.get()))

def signout_button_action():
    current_user.user_level = 0
    current_user.uid = -1
    current_user.storeping_cart = []
    start_interface()  

def login_interface():
    reset_gui()
    login_username_label.grid(row=0, column=0)
    login_password_label.grid(row=1, column=0)
    login_username_entry.grid(row=0, column=1)
    login_password_entry.grid(row=1, column=1)
    login_confirm_button.grid(row=2, column=1)
    login_forget_button.grid(row=2, column=0)
    register_button.grid(row=3, column=1)
    login_back_button.grid(row=3, column=0)

def register_button_action():
    reset_gui()
    register_username_entry.grid(row=0, column=1)
    register_username_label.grid(row=0, column=0)
    register_password_entry.grid(row=1, column=1)
    register_password_label.grid(row=1, column=0)
    register_email_entry.grid(row=2, column=1)
    register_email_label.grid(row=2, column=0)
    register_enter_button.grid(row=4, column=1)
    register_back_button.grid(row=4, column=0)

def become_member_button_action():
    result = messagebox.askyesno("", "Fixed amount of deposit ($50) is required. Still wish to apply?")
    if result:
        messagebox.showinfo("",login.register(register_username_entry.get(),
                            register_password_entry.get(),
                            register_email_entry.get()))
        register_password_entry.delete(0,END)
        register_username_entry.delete(0,END)
        register_email_entry.delete(0,END)

def display_cart():
    i=0
    while i<6:
        cart_did_list[i]=-1
        i+=1
    if current_parameter.current_cart_page != current_parameter.max_cart_page:
        for i in range(current_parameter.current_cart_page*6-6,current_parameter.current_cart_page*6):
            cart_did_list[i-(current_parameter.current_cart_page-1)*6] = current_parameter.storeping_did_list[i]
            storeping_name_label_list[i-(current_parameter.current_cart_page-1)*6].config(text=current_parameter.storeping_name_list[i])
            cart_item_price_list[i-(current_parameter.current_cart_page-1)*6].config(text=current_parameter.storeping_price_list[i])
            cart_image_list[i-(current_parameter.current_cart_page-1)*6] = PhotoImage(file=current_parameter.storeping_image_list[i]).subsample(2,2)
            cart_item_image_list[i-(current_parameter.current_cart_page-1)*6].config(image=cart_image_list[i-(current_parameter.current_cart_page-1)*6])
            cart_item_entry_list[i-(current_parameter.current_cart_page-1)*6].config(state=NORMAL)
            cart_item_entry_list[i-(current_parameter.current_cart_page-1)*6].insert(0,current_parameter.storeping_quantity_list[i])
    else:
        i=0
        for e in current_parameter.storeping_did_list[(current_parameter.current_cart_page-1)*6:]:
            cart_did_list[i]=e
            i+=1
        i=0
        for e in current_parameter.storeping_image_list[(current_parameter.current_cart_page-1)*6:]:
            cart_image_list[i] = PhotoImage(file=e).subsample(2,2)
            cart_item_image_list[i].config(image=cart_image_list[i])
            i+=1
        i=0
        for e in current_parameter.storeping_name_list[(current_parameter.current_cart_page-1)*6:]:
            storeping_name_label_list[i].config(text=e)
            i+=1
        i=0
        for e in current_parameter.storeping_price_list[(current_parameter.current_cart_page-1)*6:]:
            cart_item_price_list[i].config(text=e)
            i+=1
        i=0
        for e in current_parameter.storeping_quantity_list[(current_parameter.current_cart_page-1)*6:]:
            cart_item_entry_list[i].config(state=NORMAL)
            cart_item_entry_list[i].insert(0,e)
            i+=1

def storepingcart_checkout_button_action():
    if current_user.total == 0:
        messagebox.showwarning("", "Empty cart")
    else:
        current_user.user_level = object.update_user(current_user.uid)
        result = store.checkout_balance(current_user.user_level, current_user.total, current_user.uid)
        if current_user.user_level != 0 and result:
            store.write_order(current_user.uid,current_user.storeping_cart)
            current_user.storeping_cart = []
            current_user.total = 0
            storeping_cart_button_action()
        manager.auto_vip_block()

def cart_page_change():
    if current_parameter.current_cart_page == 1:
        cart_previous.config(state=DISABLED)
    else:
        cart_previous.config(state=NORMAL)
    if current_parameter.current_cart_page == current_parameter.max_cart_page:
        cart_next.config(state=DISABLED)
    else:
        cart_next.config(state=NORMAL)
    cart_item_price1.config(text="--")
    cart_item_price2.config(text="--")
    cart_item_price3.config(text="--")
    cart_item_price4.config(text="--")
    cart_item_price5.config(text="--")
    cart_item_price6.config(text="--")
    storeping_name_label1.config(text="--")
    storeping_name_label2.config(text="--")
    storeping_name_label3.config(text="--")
    storeping_name_label4.config(text="--")
    storeping_name_label5.config(text="--")
    storeping_name_label6.config(text="--")
    for e in cart_item_entry_list:
        e.delete(0,END)
    cart_item1_entry.config(state=DISABLED)
    cart_item2_entry.config(state=DISABLED)
    cart_item3_entry.config(state=DISABLED)
    cart_item4_entry.config(state=DISABLED)
    cart_item5_entry.config(state=DISABLED)
    cart_item6_entry.config(state=DISABLED)
    cart_item1_image.config(image=NotAvailable_photo_small)
    cart_item2_image.config(image=NotAvailable_photo_small)
    cart_item3_image.config(image=NotAvailable_photo_small)
    cart_item4_image.config(image=NotAvailable_photo_small)
    cart_item5_image.config(image=NotAvailable_photo_small)
    cart_item6_image.config(image=NotAvailable_photo_small)

def set_cart_data():
    did_quantity = store.get_list(current_user.storeping_cart)
    current_parameter.storeping_did_list = []
    current_parameter.storeping_quantity_list = []
    current_parameter.storeping_name_list = []
    current_parameter.storeping_price_list = []
    current_parameter.storeping_image_list = []
    for e in did_quantity:
        current_parameter.storeping_did_list.append(e[0])
        current_parameter.storeping_quantity_list.append(e[1])
    temp = store.name_list(current_parameter.storeping_did_list)
    current_parameter.storeping_name_list = temp[0]
    current_parameter.storeping_price_list = temp[1]
    current_parameter.storeping_image_list = temp[2]
    if (len(current_parameter.storeping_did_list)) % 6 == 0 and len(current_parameter.storeping_did_list) != 0:
        current_parameter.max_cart_page = int((len(current_parameter.storeping_did_list))/6)
    else:
        current_parameter.max_cart_page = int((len(current_parameter.storeping_did_list))/6 + 1)
    current_parameter.current_cart_page = 1

def storeping_cart_button_action():
    reset_gui()
    set_cart_data()
    cart_page_change()
    display_cart()
    label_storepingcart_item.grid(row=0,column=0)
    label_storepingcart_price.grid(row=0,column=1)
    label_storepingcart_quantity.grid(row=0,column=2)
    cart_label_frame.grid(row=8, column=2)
    storepingcart_checkout_total.config(text=str(current_user.total))
    cart_button_frame.grid(row=10,column=2)
    login_back_button.grid(row=10, column=0)
    cart_next.grid(row=9, column=2)
    cart_previous.grid(row=9, column=0)
    item_name_frame1.grid(row=2,column=0)
    item_name_frame2.grid(row=3,column=0)
    item_name_frame3.grid(row=4,column=0)
    item_name_frame4.grid(row=5,column=0)
    item_name_frame5.grid(row=6,column=0)
    item_name_frame6.grid(row=7,column=0)
    cart_item_price1.grid(row=2,column=1)
    cart_item_price2.grid(row=3,column=1)
    cart_item_price3.grid(row=4,column=1)
    cart_item_price4.grid(row=5,column=1)
    cart_item_price5.grid(row=6,column=1)
    cart_item_price6.grid(row=7,column=1)
    cart_item1_entry.grid(row=2,column=2)
    cart_item2_entry.grid(row=3,column=2)
    cart_item3_entry.grid(row=4,column=2)
    cart_item4_entry.grid(row=5,column=2)
    cart_item5_entry.grid(row=6,column=2)
    cart_item6_entry.grid(row=7,column=2)
    update_cart()

def update_total():
    set_cart_data()
    total_price = 0
    for e,f in zip(current_parameter.storeping_quantity_list, current_parameter.storeping_price_list):
        total_price += int(e)*int(f)
    current_user.total = total_price

def update_cart():
    update_quantity = [cart_item1_entry.get(), cart_item2_entry.get(), cart_item3_entry.get(), cart_item4_entry.get(), cart_item5_entry.get(), cart_item6_entry.get()]
    if current_parameter.current_cart_page != current_parameter.max_cart_page:
        for e in update_quantity:
            if not store.check_quantity(e):
                return
        current_parameter.storeping_quantity_list[(current_parameter.current_cart_page-1)*6:(current_parameter.current_cart_page-1)*6+6] = update_quantity
    else:
        if cart_item6_entry["state"] == DISABLED:
            del update_quantity[5]
        if cart_item5_entry["state"] == DISABLED:
            del update_quantity[4]
        if cart_item4_entry["state"] == DISABLED:
            del update_quantity[3]
        if cart_item3_entry["state"] == DISABLED:
            del update_quantity[2]
        if cart_item2_entry["state"] == DISABLED:
            del update_quantity[1]
        if cart_item1_entry["state"] == DISABLED:
            del update_quantity[0]
        for e in update_quantity:
            if not store.check_quantity(e):
                return
        current_parameter.storeping_quantity_list[(current_parameter.current_cart_page-1)*6:] = update_quantity
    current_user.storeping_cart = []
    for e,f in zip(current_parameter.storeping_quantity_list, current_parameter.storeping_did_list):
        for i in range(int(e)):
            current_user.storeping_cart.append(f)
    total_price = 0
    for e,f in zip(current_parameter.storeping_quantity_list, current_parameter.storeping_price_list):
        total_price += int(e)*int(f)
    current_user.total = total_price
    store.write_cart(current_user.uid, current_user.storeping_cart)
    set_cart_data()
    cart_page_change()
    display_cart()
    storepingcart_checkout_total.config(text=str(current_user.total))

def add_cart_button_action(i):
    reset_gui()
    storeping_image = dish_image_list[i]
    storeping_image.grid(row=0,column=0)
    storeping_name= dish_name_list[i]
    storeping_name.grid(row=1,column=0)
    storeping_price.append(current_parameter.price_list[i])
    dish_price_list[i].grid(row=2,column=0)
    storeping_did.append(dish_did_list[i])
    label_quantity_entry.grid(row=4,column=0)
    label_quantity.grid(row=3, column=0)
    login_back_button.grid(row=6, column=0)
    storeping_enter_button.grid(row=5,column=0)

def storeping_enter_button_action():
    if current_user.uid != -1:
        if store.check_quantity(label_quantity_entry.get()):
            for i in range(int(label_quantity_entry.get())):
                current_user.storeping_cart.append(storeping_did[-1])
                current_user.total += int(storeping_price[-1])
            messagebox.showinfo("", "Added to cart")
        label_quantity_entry.delete(0,END)
        store.write_cart(current_user.uid, current_user.storeping_cart)
    else:
        messagebox.showwarning("", "Please log in first")

def page_change():
    if current_parameter.menu_current_page == 1:
        previous_page_button.config(state=DISABLED)
    else:
        previous_page_button.config(state=NORMAL)
    if current_parameter.menu_current_page == current_parameter.menu_max_page:
        next_page_button.config(state=DISABLED)
    else:
        next_page_button.config(state=NORMAL)
    dish_image1.config(image=NotAvailable_photo)
    dish_image2.config(image=NotAvailable_photo)
    dish_image3.config(image=NotAvailable_photo)
    dish_image4.config(image=NotAvailable_photo)
    dish_image5.config(image=NotAvailable_photo)
    dish_image6.config(image=NotAvailable_photo)
    dish_name1.config(text="Coming soon...")
    dish_name2.config(text="Coming soon...")
    dish_name3.config(text="Coming soon...")
    dish_name4.config(text="Coming soon...")
    dish_name5.config(text="Coming soon...")
    dish_name6.config(text="Coming soon...")
    dish_price1.config(text="")
    dish_price2.config(text="")
    dish_price3.config(text="")
    dish_price4.config(text="")
    dish_price5.config(text="")
    dish_price6.config(text="")

def display_menu():
    for e in dish_comment_list:
        e.config(state=NORMAL)
    i=0
    while i<6:
        dish_did_list[i]=-1
        i+=1
    if current_parameter.menu_current_page != current_parameter.menu_max_page:
        for i in range(current_parameter.menu_current_page*6-6,current_parameter.menu_current_page*6):
            dish_did_list[i-(current_parameter.menu_current_page-1)*6] = current_parameter.menu_list[i]
            dish_name_list[i-(current_parameter.menu_current_page-1)*6].config(text=current_parameter.name_list[i])
            dish_price_list[i-(current_parameter.menu_current_page-1)*6].config(text=current_parameter.price_list[i])
            dish_img_list[i-(current_parameter.menu_current_page-1)*6] = PhotoImage(file=current_parameter.image_list[i])
            dish_image_list[i-(current_parameter.menu_current_page-1)*6].config(image=dish_img_list[i-(current_parameter.menu_current_page-1)*6])
    else:
        i=0
        for e in current_parameter.menu_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_did_list[i]=e
            i+=1
        i=0
        for e in current_parameter.image_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_img_list[i] = PhotoImage(file=e)
            dish_image_list[i].config(image=dish_img_list[i])
            i+=1
        i=0
        for e in current_parameter.name_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_name_list[i].config(text=e)
            i+=1
        i=0
        for e in current_parameter.price_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_price_list[i].config(text=e)
            i+=1
    if current_user.user_level != 0:
        i=0
        for e in dish_did_list:
            if e == -1:
                dish_buy_list[i].config(state=DISABLED)
            else:
                dish_buy_list[i].config(state=NORMAL)
            i+=1
    i=0
    for e in dish_did_list:
        if e == -1:
            dish_comment_list[i].config(state=DISABLED)
        i+=1

def cart_next_page():
    current_parameter.current_cart_page += 1
    cart_page_change()
    display_cart()

def cart_previous_page():
    current_parameter.current_cart_page -= 1
    cart_page_change()
    display_cart()

def menu_next_page():
    current_parameter.menu_current_page += 1
    page_change()
    display_menu()

def menu_previous_page():
    current_parameter.menu_current_page -= 1
    page_change()
    display_menu()

def delivery_interface():
    reset_gui()
    signout_button.grid(row=0, column=0)
    delivery_order_listName.grid(row=1, column=0)
    delivery_order_list.grid(row=2, column=0)
    delivery_frame.grid(row=3, column=0)
    order_list = object.get_order_list()
    delivery_order_list.delete(0,END)
    for item in order_list:
        delivery_order_list.insert(END, item)

def current_location():
    reset_gui()
    selection_label.grid(row=0, column=0, columnspan=9)
    node0.grid(row=1, column=0)
    node1.grid(row=1, column=2)
    node2.grid(row=1, column=4)
    node3.grid(row=1, column=6)
    node4.grid(row=1, column=8)
    node5.grid(row=3, column=0)    
    node6.grid(row=3, column=2)
    node7.grid(row=3, column=4)
    node8.grid(row=3, column=6)
    node9.grid(row=3, column=8)
    node10.grid(row=5, column=0)
    node11.grid(row=5, column=2)
    node12.grid(row=5, column=4)
    node13.grid(row=5, column=6)
    node14.grid(row=5, column=8)
    node15.grid(row=7, column=0)
    node16.grid(row=7, column=2)
    node17.grid(row=7, column=4)
    node18.grid(row=7, column=6)
    node19.grid(row=7, column=8)
    node20.grid(row=9, column=0)
    node21.grid(row=9, column=2)
    node22.grid(row=9, column=4)
    node23.grid(row=9, column=6)
    node24.grid(row=9, column=8)
    edge1.grid(row=1, column=1)
    edge2.grid(row=1, column=3)
    edge3.grid(row=1, column=5)
    edge4.grid(row=1, column=7)
    edge5.grid(row=2, column=0)
    edge6.grid(row=2, column=2)
    edge8.grid(row=2, column=6)
    edge9.grid(row=2, column=8)
    edge10.grid(row=3, column=1)
    edge11.grid(row=3, column=3)
    edge12.grid(row=3, column=5)
    edge13.grid(row=3, column=7)
    edge14.grid(row=4, column=0)
    edge15.grid(row=4, column=2)
    edge16.grid(row=4, column=4)
    edge17.grid(row=4, column=6)
    edge18.grid(row=4, column=8)
    edge20.grid(row=5, column=3)
    edge21.grid(row=5, column=5)
    edge23.grid(row=6, column=0)
    edge24.grid(row=6, column=2)
    edge25.grid(row=6, column=4)
    edge26.grid(row=6, column=6)
    edge27.grid(row=6, column=8)
    edge28.grid(row=7, column=1)
    edge29.grid(row=7, column=3)
    edge30.grid(row=7, column=5)
    edge31.grid(row=7, column=7)
    edge32.grid(row=8, column=0)
    edge33.grid(row=8, column=2)
    edge35.grid(row=8, column=6)
    edge36.grid(row=8, column=8)
    edge37.grid(row=9, column=1)
    edge38.grid(row=9, column=3)
    edge39.grid(row=9, column=5)
    edge40.grid(row=9, column=7)
    for e in node_list:
        e.config(state=NORMAL, highlightbackground="white")
    for e in h_edge_list:
        e.config(image=EmptyRoads)
    for e in v_edge_list:
        e.config(image=EmptyRoad)

def delivery_track_interface_action(w):
    if w == 0:
        try:
            current_location()
        except TclError:
            messagebox.showwarning("", "Please select an order to track")
    elif w == 1:
        try:
            object.issue_warning(delivery_order_list.get(delivery_order_list.curselection()))
            delivery_interface()
        except TclError:
            messagebox.showwarning("", "Please select an order to issue warning")

def delivered_action(ddid):
    if object.delivery_track_status(ddid):
        delivery_interface()

def delivery_track_interface(ddid, cur_loc):
    reset_gui()
    for e in node_list:
        e.config(state=DISABLED)
    node0.grid(row=0, column=0)
    node1.grid(row=0, column=2)
    node2.grid(row=0, column=4)
    node3.grid(row=0, column=6)
    node4.grid(row=0, column=8)
    node5.grid(row=2, column=0)    
    node6.grid(row=2, column=2)
    node7.grid(row=2, column=4)
    node8.grid(row=2, column=6)
    node9.grid(row=2, column=8)
    node10.grid(row=4, column=0)
    node11.grid(row=4, column=2)
    node12.grid(row=4, column=4)
    node13.grid(row=4, column=6)
    node14.grid(row=4, column=8)
    node15.grid(row=6, column=0)
    node16.grid(row=6, column=2)
    node17.grid(row=6, column=4)
    node18.grid(row=6, column=6)
    node19.grid(row=6, column=8)
    node20.grid(row=8, column=0)
    node21.grid(row=8, column=2)
    node22.grid(row=8, column=4)
    node23.grid(row=8, column=6)
    node24.grid(row=8, column=8)
    edge1.grid(row=0, column=1)
    edge2.grid(row=0, column=3)
    edge3.grid(row=0, column=5)
    edge4.grid(row=0, column=7)
    edge5.grid(row=1, column=0)
    edge6.grid(row=1, column=2)
    edge8.grid(row=1, column=6)
    edge9.grid(row=1, column=8)
    edge10.grid(row=2, column=1)
    edge11.grid(row=2, column=3)
    edge12.grid(row=2, column=5)
    edge13.grid(row=2, column=7)
    edge14.grid(row=3, column=0)
    edge15.grid(row=3, column=2)
    edge16.grid(row=3, column=4)
    edge17.grid(row=3, column=6)
    edge18.grid(row=3, column=8)
    edge20.grid(row=4, column=3)
    edge21.grid(row=4, column=5)
    edge23.grid(row=5, column=0)
    edge24.grid(row=5, column=2)
    edge25.grid(row=5, column=4)
    edge26.grid(row=5, column=6)
    edge27.grid(row=5, column=8)
    edge28.grid(row=6, column=1)
    edge29.grid(row=6, column=3)
    edge30.grid(row=6, column=5)
    edge31.grid(row=6, column=7)
    edge32.grid(row=7, column=0)
    edge33.grid(row=7, column=2)
    edge35.grid(row=7, column=6)
    edge36.grid(row=7, column=8)
    edge37.grid(row=8, column=1)
    edge38.grid(row=8, column=3)
    edge39.grid(row=8, column=5)
    edge40.grid(row=8, column=7)
    legend_frame.grid(row=9, column=0, columnspan=10)
    delivery_track_frame.grid(row=10, column=0, columnspan=10)
    map_matrix = maptarget.rand_situation()
    change_map(map_matrix, maptarget.find_path(map_matrix, maptarget.get_destination(ddid), cur_loc))
    delivered.config(command=lambda: delivered_action(ddid))

def change_map(map_matrix, path):
    for h,v in zip(h_edge_list, v_edge_list):
        h.config(image=EmptyRoads)
        v.config(image=EmptyRoad)
    i = 0
    while i<len(path)-1:
        if h_edge_matrix[path[i]][path[i+1]] != 0:
            h_edge_matrix[path[i]][path[i+1]].config(image=GreenLights)
        elif v_edge_matrix[path[i]][path[i+1]] != 0:
            v_edge_matrix[path[i]][path[i+1]].config(image=GreenLight)
        i+=1
    for e in node_list:
        e.config(highlightbackground="white")
    i = 0
    for e in path:
        if i == 0 or i==len(path)-1:
            node_list[e].config(highlightbackground="Yellow")
        else:
            node_list[e].config(highlightbackground="Green")
        i+=1
    for x in range(0,25):
        for y in range(0,25):
            if map_matrix[x][y] == 0:
                if h_edge_matrix[x][y] != 0:
                    h_edge_matrix[x][y].config(image=CarTraffics)
                if v_edge_matrix[x][y] != 0:
                    v_edge_matrix[x][y].config(image=CarTraffic)
            elif map_matrix[x][y] == 1:
                if h_edge_matrix[x][y] != 0:
                    h_edge_matrix[x][y].config(image=StopSigns)
                if v_edge_matrix[x][y] != 0:
                    v_edge_matrix[x][y].config(image=StopSign)

def start_interface():
    reset_gui()
    if current_user.user_level == 0:
        dish_buy1.config(state=DISABLED)
        dish_buy2.config(state=DISABLED)
        dish_buy3.config(state=DISABLED)
        dish_buy4.config(state=DISABLED)
        dish_buy5.config(state=DISABLED)
        dish_buy6.config(state=DISABLED)
    else:
        dish_buy1.config(state=NORMAL)
        dish_buy2.config(state=NORMAL)
        dish_buy3.config(state=NORMAL)
        dish_buy4.config(state=NORMAL)
        dish_buy5.config(state=NORMAL)
        dish_buy6.config(state=NORMAL)
    i=0
    for e in dish_did_list:
        if e == -1:
            dish_comment_list[i].config(state=DISABLED)
        i+=1
    current_parameter.alldish = object.get_all_dish()
    chef_name.config(text="All")
    current_parameter.current_chef_name = "All"
    current_parameter.current_chef_uid = -1
    set_parameter()
    page_change()
    display_menu()
    refresh_button.grid(row=0, column=0)
    chef_name.grid(row=1, column=1)
    if(current_user.user_level == 0):
        login_button.grid(row=0, column=2)
    else:
        info_button.grid(row=1, column=2)
        comment_button.grid(row=1, column=0)
        signout_button.grid(row=0, column=2)
    storeping_cart_items.grid(row=0, column=1)
    search_frame.grid(row=2, column=0, columnspan=3)
    dish_image1.grid(row=3, column=0)
    dish_name1.grid(row=4, column=0)
    dish_price1.grid(row=5, column=0)
    dish_buy1.grid(row=6, column=0)
    dish_comment1.grid(row=7, column=0)
    dish_image2.grid(row=3, column=1)
    dish_name2.grid(row=4, column=1)
    dish_price2.grid(row=5, column=1)
    dish_buy2.grid(row=6, column=1)
    dish_comment2.grid(row=7, column=1)
    dish_image3.grid(row=3, column=2)
    dish_name3.grid(row=4, column=2)
    dish_price3.grid(row=5, column=2)
    dish_buy3.grid(row=6, column=2)
    dish_comment3.grid(row=7, column=2)
    dish_image4.grid(row=8, column=0)
    dish_name4.grid(row=9, column=0)
    dish_price4.grid(row=10, column=0)
    dish_buy4.grid(row=11, column=0)
    dish_comment4.grid(row=12, column=0)
    dish_image5.grid(row=8, column=1)
    dish_name5.grid(row=9, column=1)
    dish_price5.grid(row=10, column=1)
    dish_buy5.grid(row=11, column=1)
    dish_comment5.grid(row=12, column=1)
    dish_image6.grid(row=8, column=2)
    dish_name6.grid(row=9, column=2)
    dish_price6.grid(row=10, column=2)
    dish_buy6.grid(row=11, column=2)
    dish_comment6.grid(row=12, column=2)
    next_page_button.grid(row=13, column=2)
    previous_page_button.grid(row=13, column=0)

def new_employee():
    reset_gui()
    employee_chef.config(state=NORMAL)
    employee_deliver.config(state=NORMAL)
    employee_back.grid(row=5, column=0)
    employee_type.grid(row=0, column=0)
    employee_type_frame.grid(row=0, column=1)
    employee_username.grid(row=2, column=1)
    employee_password.grid(row=3, column=1)
    employee_email.grid(row=4, column=1)
    employee_add.grid(row=5, column=1)
    employee_username_label.grid(row=2, column=0)
    employee_password_label.grid(row=3, column=0)
    employee_email_label.grid(row=4, column=0)
    employee_name_label.grid(row=1, column=0)
    employee_name.grid(row=1, column=1)

def select_type(t):
    if t == "c":
        current_parameter.employee_type = 1
        employee_chef.config(state=DISABLED)
        employee_deliver.config(state=NORMAL)
    else:
        current_parameter.employee_type = 2
        employee_chef.config(state=NORMAL)
        employee_deliver.config(state=DISABLED)

def register_new_employee():
    if employee_chef["state"] == "normal" and employee_deliver["state"] == "normal":
        messagebox.showwarning("", "Please select an employee type")
    else:
        if login.register_employee(current_parameter.employee_type, employee_name.get(), employee_username.get(), 
                            employee_password.get(), employee_email.get()):
            employee_chef["state"] = "normal"
            employee_deliver["state"] = "normal"
            employee_email.delete(0,END)
            employee_name.delete(0,END)
            employee_password.delete(0,END)
            employee_username.delete(0,END)
            refresh_menu(0)

def manager_interface():
    reset_gui()
    manager_employee.grid(row=0, column=1, columnspan=2)
    signout_button.grid(row=0, column=3)
    users_approve_list_label.grid(row=1, column=0)
    update_all_button.grid(row=0, column=0)
    users_approve_list.grid(row=2, column=0)
    user_approved_list_label.grid(row=1, column=1)
    user_approved_list.grid(row=2, column=1)
    user_declined_list_label.grid(row=1, column=2)
    user_declined_list.grid(row=2, column=2)
    dish_compliments_list_label.grid(row=3, column=0)
    dish_compliments_list.grid(row=4, column=0)
    dish_approved_compliements_list_label.grid(row=3, column=1)
    dish_approved_compliements_list.grid(row=4, column=1)
    dish_declined_compliments_list_label.grid(row=3, column=2)
    dish_declined_compliments_list.grid(row=4, column=2)
    dish_complaints_list_label.grid(row=5, column=0)
    dish_complaints_list.grid(row=6, column=0)
    dish_approved_compliants_list_label.grid(row=5, column=1)
    dish_approved_compliants_list.grid(row=6, column=1)
    dish_declined_compliants_list.grid(row=6, column=2)
    dish_declined_compliants_list_label.grid(row=5, column=2)
    manager_approve_button.grid(row=9, column=3)
    manager_decline_button.grid(row=9, column=0)
    user_quit_label.grid(row=1, column=3)
    user_quit_list.grid(row=2, column=3)
    manager_update_all_action()

def manager_update_all_action():
    dish_compliments_list.delete(0,END)
    dish_complaints_list.delete(0,END)
    users_approve_list.delete(0,END)
    user_approved_list.delete(0,END)
    user_declined_list.delete(0,END)
    dish_approved_compliements_list.delete(0, END)
    dish_declined_compliments_list.delete(0, END)
    dish_approved_compliants_list.delete(0, END)
    dish_declined_compliants_list.delete(0, END)
    user_quit_list.delete(0,END)
    pending_list = object.get_pending_registrations()
    compliments_list = object.get_pending_compliments()
    complaints_list = object.get_pending_complaints()
    approved_list = object.get_users(1)
    declined_list = object.get_users(-1)
    blocked_list = object.get_users(0)
    approved_compliments_list = object.get_comment(1,1)
    declined_compliments_list = object.get_comment(1,-1)
    approved_compliants_list = object.get_comment(0,1)
    declined_compliants_list = object.get_comment(0,-1)
    quit_list = object.get_quit_list()
    for e in quit_list:
        user_quit_list.insert(END, e)
    for item in approved_compliments_list:
        dish_approved_compliements_list.insert(END, item)
    for item in declined_compliments_list:
        dish_declined_compliments_list.insert(END, item)
    for item in approved_compliants_list:
        dish_approved_compliants_list.insert(END, item)
    for item in declined_compliants_list:
        dish_declined_compliants_list.insert(END, item)
    for item in pending_list:
        users_approve_list.insert(END, item)
    for item in compliments_list:
        dish_compliments_list.insert(END, item)
    for item in complaints_list:
        dish_complaints_list.insert(END, item)
    for item in approved_list:
        user_approved_list.insert(END, item)
    for item in declined_list:
        user_declined_list.insert(END, item)
    
def manager_approve_decline_button_action(input):
    try:
        manager.approve_pending_registrations(users_approve_list.get(users_approve_list.curselection()), input)
    except TclError:
        try:
            manager.approve_compliments(dish_compliments_list.get(dish_compliments_list.curselection()), input)
        except TclError:
            try:
                manager.approve_complaints(dish_complaints_list.get(dish_complaints_list.curselection()), input)
            except TclError:
                try:
                    manager.approve_pending_registrations(user_approved_list.get(user_approved_list.curselection()), input) 
                except TclError:
                    try:
                        manager.approve_pending_registrations(user_declined_list.get(user_declined_list.curselection()), input)        
                    except TclError:
                        try:
                            manager.approve_compliments(dish_approved_compliements_list.get(dish_approved_compliements_list.curselection()), input)            
                        except TclError:
                            try:
                                manager.approve_compliments(dish_declined_compliments_list.get(dish_declined_compliments_list.curselection()), input)                 
                            except TclError:
                                try:
                                    manager.approve_complaints(dish_approved_compliants_list.get(dish_approved_compliants_list.curselection()), input)                   
                                except TclError:
                                    try:
                                        manager.approve_complaints(dish_declined_compliants_list.get(dish_declined_compliants_list.curselection()), input)                       
                                    except TclError:
                                        try:
                                            if input == 1:
                                                manager.approve_pending_registrations(user_quit_list.get(user_quit_list.curselection()), 2)
                                            else:
                                                manager.approve_pending_registrations(user_quit_list.get(user_quit_list.curselection()), -2)                             
                                        except TclError:
                                            messagebox.showwarning("","Please select an item to process")
    manager_update_all_action()
    manager.auto_demote_promote_employee()
    manager.auto_vip_block()
    refresh_menu(0)

def employee_managerment():
    reset_gui()
    employee_chef["state"] = "normal"
    employee_deliver["state"] = "normal"
    employee_email.delete(0,END)
    employee_name.delete(0,END)
    employee_password.delete(0,END)
    employee_username.delete(0,END)
    chef_employee_list.delete(0,END)
    dish_complaints_list.delete(0,END)
    deliver_employee_list.delete(0,END)
    add_employee.grid(row=0, column=0)
    chef_employee_list_label.grid(row=1, column=0)
    deliver_employee_list_label.grid(row=1, column=1)
    chef_employee_list.grid(row=2, column=0)
    deliver_employee_list.grid(row=2, column=1)
    managerment_back.grid(row=0, column=1)
    employee_promote.grid(row=3, column=1)
    employee_demote.grid(row=3, column=0)
    for item in object.get_chef_employee():
        chef_employee_list.insert(END, item)
    for item in object.get_deliver_employee():
        deliver_employee_list.insert(END, item)

def employee_salary_adjust(i):
    try:
        manager.demote_promote_employee(chef_employee_list.get(chef_employee_list.curselection()), i)
    except TclError:
        try:
            manager.demote_promote_employee(deliver_employee_list.get(deliver_employee_list.curselection()), i)
        except TclError:
            messagebox.showwarning("","Please select an item to process")
    chef_employee_list.selection_clear(0, END)
    deliver_employee_list.selection_clear(0, END)

def profile_button_action():
    reset_gui()
    first_row.grid(row=0, column=0)
    second_row.grid(row=1, column=0)
    profile_back_button.grid(row=2, column=1)
    profile_deposit_frame.grid(row=2,column=0)
    profile = object.profile(current_user.uid)
    profile_username.config(text=profile[0])
    profile_uid.config(text=current_user.uid)
    profile_balance.config(text=profile[1])
    profile_email.config(text=profile[2])
    profile_warning.config(text=profile[3])
    if profile[4] == 1:
        profile_vip_status.config(text="Regular")
    else:
        profile_vip_status.config(text="VIP")

def make_deposit():
    object.deposit_money(profile_deposit.get(),current_user.uid)
    profile_deposit.delete(0,END)
    profile_button_action()

def view_comment(did):
    reset_gui()
    description_view.grid(row=3, column=0)
    description_view.config(text=object.get_description(did), wraplength=185, justify=LEFT)
    view_user_comment.grid(row=0, column=0, rowspan=2)
    view_star.grid(row=0, column=1)
    view_delivery.grid(row=1, column=1)
    profile_back_button.grid(row=3, column=1)
    data = object.comment_op(did)
    view_user_comment.delete(0,END)
    for e in data[0]:
        view_user_comment.insert(END, e)
    for e,f in zip(view_star_list, view_delivery_list):
        e.config(image=star_b)
        f.config(image=star_b)
    i=0
    for e in view_star_list:
        if i<data[1]:
            e.config(image=star_c)
        i+=1
    i=0
    for e in view_delivery_list:
        if i<data[2]:
            e.config(image=star_c)
        i+=1

def user_quit_action():
    if object.user_quit(current_user.uid):
        signout_button_action()

def search_button_action(text):
    found = False
    text = text.lower()
    if current_parameter.alldish.get(text) != None:
        found = True
        temp = object.get_all(current_parameter.alldish.get(text))
    if not found:
        messagebox.showwarning("", "No dish named "+str(text))
        search_entry.delete(0,END)
    else:
        reset_gui()
        search_component[0] = PhotoImage(file=temp[2])
        storeping_image.config(image=search_component[0])
        storeping_image.grid(row=0,column=0)
        storeping_name.config(text=temp[0])
        storeping_name.grid(row=1,column=0)
        storeping_price.append(temp[1])
        dish_price.config(text=temp[1])
        dish_price.grid(row=2,column=0)
        storeping_did.append(current_parameter.alldish.get(text))
        label_quantity_entry.grid(row=4,column=0)
        label_quantity.grid(row=3, column=0)
        login_back_button.grid(row=6, column=0)
        storeping_enter_button.grid(row=5,column=0)

def save_new_dish_action():
    if object.save_new_dish(dish_name_entry.get(), price_entry.get(), description_entry.get(), image_entry.get()):
        dish_name_entry.delete(0,END)
        price_entry.delete(0,END)
        description_entry.delete(0,END)
        image_entry.config(state=NORMAL)
        image_entry.delete(0,END)
        image_entry.config(state=DISABLED)

#view comment interface
star_c = PhotoImage(file="images/RateGold.gif").subsample(5,5)
star_b = PhotoImage(file="images/RateBlack.gif").subsample(5,5)
view_user_comment = Listbox(program)
view_star = Frame(program)
view_delivery = Frame(program)
view_food_label = Label(view_star, text="Food")
view_delivery_label = Label(view_delivery, text="Delivery")
view_star1 = Label(view_star, image=star_b)
view_star2 = Label(view_star, image=star_b)
view_star3 = Label(view_star, image=star_b)
view_star4 = Label(view_star, image=star_b)
view_star5 = Label(view_star, image=star_b)
view_star_list = [view_star1, view_star2, view_star3, view_star4, view_star5]
view_delivery1 = Label(view_delivery, image=star_b)
view_delivery2 = Label(view_delivery, image=star_b)
view_delivery3 = Label(view_delivery, image=star_b)
view_delivery4 = Label(view_delivery, image=star_b)
view_delivery5 = Label(view_delivery, image=star_b)
view_delivery_list = [view_delivery1, view_delivery2, view_delivery3, view_delivery4, view_delivery5]
view_food_label.pack(side="left")
view_star1.pack(side="left")
view_star2.pack(side="left")
view_star3.pack(side="left")
view_star4.pack(side="left")
view_star5.pack(side="left")
view_delivery_label.pack(side="left")
view_delivery1.pack(side="left")
view_delivery2.pack(side="left")
view_delivery3.pack(side="left")
view_delivery4.pack(side="left")
view_delivery5.pack(side="left")
description_view = Label(program)

#comment interface
combined_rate_frame = Frame(program)
star_food_frame = Frame(combined_rate_frame)
star_delivery_frame = Frame(combined_rate_frame)
rate_button_frame = Frame(combined_rate_frame)
rate_food_back = Button(rate_button_frame, text="Back", command=start_interface)
rate_food = Button(rate_button_frame, text="Submit", command=submit_rating)
rate_food_back.pack(side="left")
rate_food.pack(side="left")
rate_comment_frame = Frame(combined_rate_frame)
rate_comment_label = Label(rate_comment_frame, text="Comment")
rate_comment = Entry(rate_comment_frame)
rate_comment_label.pack(side="left")
rate_comment.pack(side="left")
star_food_frame.pack(side="top")
star_delivery_frame.pack(side="top")
rate_comment_frame.pack(side="top")
rate_button_frame.pack(side="top")
rate_food.pack(side="top")
star_food_label = Label(star_food_frame, text="Food")
star1_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(1))
star2_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(2))
star3_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(3))
star4_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(4))
star5_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(5))
star_food_list = [star1_food, star2_food, star3_food, star4_food, star5_food]
star_food_label.pack(side="left")
star1_food.pack(side="left")
star2_food.pack(side="left")
star3_food.pack(side="left")
star4_food.pack(side="left")
star5_food.pack(side="left")
star_delivery_label = Label(star_delivery_frame, text="Delivery")
star1_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(1))
star2_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(2))
star3_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(3))
star4_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(4))
star5_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(5))
star_delivery_list = [star1_delivery, star2_delivery, star3_delivery, star4_delivery, star5_delivery]
star_delivery_label.pack(side="left")
star1_delivery.pack(side="left")
star2_delivery.pack(side="left")
star3_delivery.pack(side="left")
star4_delivery.pack(side="left")
star5_delivery.pack(side="left")
order_history_label = Label(program, text="Unrated order")
rate_order_list = Listbox(program)

#user profile
first_row = Frame(program)
second_row = Frame(program)
profile_username_label = Label(first_row, text="Username")
profile_username = Button(first_row, text="", command=None)
profile_uid_label = Label(first_row, text="ID")
profile_uid = Button(first_row, text="", command=None)
profile_balance_label = Label(first_row, text="Balance")
profile_balance = Button(first_row, text="", command=None)
profile_username_label.pack(side="left")
profile_username.pack(side="left")
profile_uid_label.pack(side="left")
profile_uid.pack(side="left")
profile_balance_label.pack(side="left")
profile_balance.pack(side="left")
profile_email_label = Label(second_row, text="Email")
profile_email = Button(second_row, text="", command=None)
profile_warning_label = Label(second_row, text="Warning")
profile_warning = Button(second_row, text="", command=None)
profile_vip = Label(second_row, text="Account level")
profile_vip_status = Button(second_row, text="", command=None)
profile_vip.pack(side="left")
profile_vip_status.pack(side="left")
profile_email_label.pack(side="left")
profile_email.pack(side="left")
profile_warning_label.pack(side="left")
profile_warning.pack(side="left")
profile_back_button = Button(text="Back", command = start_interface)
profile_deposit_frame = Frame(program)
profile_deposit = Entry(profile_deposit_frame)
profile_deposit_button = Button(profile_deposit_frame, text="Deposit", command=make_deposit)
profile_deposit.pack(side="left")
profile_deposit_button.pack(side="left")
profile_user_quit = Button(profile_deposit_frame, text="Close account", command= user_quit_action)
profile_user_quit.pack(side="left")

#chef interface
available_dish_list = Listbox(program)
current_dish_list = Listbox(program)
available_dish_label = Label(program, text="Available dish")
current_dish_label = Label(program, text="Current dish")
add_new_dish_button_label = Label(program, text="Add new dish")
add_new_dish_button = Button(text="Add new dish", command=add_new_dish_interface)
chef_frame = Frame(program)
save_menu_button = Button(text="Save", command=save_menu_action)
dish_add = Button(chef_frame, text="Add ->", command=add_dish)
dish_remove = Button(chef_frame, text="<- Remove", command=remove_dish)
dish_add.pack(side="top")
dish_remove.pack(side="top")

#add new dish interface
add_back_button = Button(text="Back", command=chef_interface)
dish_name_label = Label(program, text="Name")
price_label = Label(program, text="Price $")
description_label = Label(program, text="Description")
image_label = Label(program, text="Image")
dish_name_entry = Entry(program)
price_entry = Entry(program)
description_entry = Entry(program)
image_path = Frame(program)
image_add_button = Button(image_path, text="Add image", command=select_file)
image_entry = Entry(image_path, state=DISABLED)
image_entry.pack(side="left")
image_add_button.pack(side="left")
save_button = Button(text="Save", command= save_new_dish_action)

#manager interface
managerment_back = Button(text="Back", command=manager_interface)
deliver_employee_list_label = Label(program, text="Deliver")
chef_employee_list_label = Label(program, text="Chef")

sales_employee_list_label = Label(program, text="Sales")

chef_employee_list = Listbox(program)
deliver_employee_list = Listbox(program)

sales_employee_list = Listbox(program)

employee_promote = Button(text="Promote", command=lambda: employee_salary_adjust(1))
employee_demote = Button(text="Demote", command=lambda: employee_salary_adjust(-1))
manager_employee = Button(text="manager employees", command=employee_managerment)
employee_type_frame = Frame(program)
employee_chef = Button(employee_type_frame, text="Chef", command=lambda: select_type("c"))
employee_back = Button(text="Back", command=employee_managerment)
employee_deliver = Button(employee_type_frame, text="Deliver", command=lambda: select_type("d"))

employee_sale = Button(employee_type_frame, text="Sales", command=lambda: select_type("s"))

employee_sale.pack(side = "left")
employee_chef.pack(side="left")
employee_deliver.pack(side="left")


employee_username = Entry(program)
employee_password = Entry(program)
employee_email = Entry(program)
employee_add = Button(text="Add", command=register_new_employee)
employee_username_label = Label(program, text="Username")
employee_password_label = Label(program, text="Password")
employee_email_label = Label(program, text="Email")
employee_name_label = Label(program, text="Name")
employee_name = Entry(program)
employee_type = Label(program, text="Type")
add_employee = Button(text="Add employee", command=new_employee)
users_approve_list = Listbox(program)
users_approve_list_label = Label(program, text="Pending registrations")
manager_approve_button = Button(text="Approve", command=lambda: manager_approve_decline_button_action(1))
manager_decline_button = Button(text="Decline", command=lambda: manager_approve_decline_button_action(-1))
dish_compliments_list_label = Label(program, text="Pending compliments")
dish_compliments_list = Listbox(program)
dish_complaints_list_label = Label(program, text="Pending complaints")
dish_complaints_list = Listbox(program)
update_all_button = Button(text="Refresh", command=manager_update_all_action)
dish_approved_compliements_list_label = Label(program, text="Approved compliments")
dish_approved_compliants_list_label = Label(program, text="Approved complaints")
dish_declined_compliments_list_label = Label(program, text="Declined compliments")
dish_declined_compliants_list_label = Label(program, text="Declined complaints")
user_approved_list_label = Label(program, text="Approved users")
user_declined_list_label = Label(program, text="Black Listed Users")
dish_approved_compliements_list = Listbox(program)
dish_approved_compliants_list = Listbox(program)
dish_declined_compliments_list = Listbox(program)
dish_declined_compliants_list = Listbox(program)
user_approved_list = Listbox(program)
user_declined_list = Listbox(program)
user_quit_label = Label(program, text="Closing accounts")
user_quit_list = Listbox(program)

#login interface
login_username_label = Label(program, text="Username")
login_password_label = Label(program, text="Password")
login_username_entry = Entry(program)
login_password_entry = Entry(program)
login_confirm_button = Button(text="Sign in", command=login_confirm_button_action)
login_forget_button = Button(text="Forget", command=login_forget_button_action)
login_back_button = Button(text="Back", command=start_interface)
register_button = Button(text="Register", command=register_button_action)

#forget interface
login_forget_entry = Entry(program)
login_forget_label = Label(program, text="Email")
login_retrive_button = Button(text="Retrive", command=login_retrieve_button_action)
forget_back_button = Button(text="Back", command=login_interface)

#register_interface
register_username_entry = Entry(program)
register_username_label = Label(program, text="User")
register_password_entry = Entry(program)
register_password_label = Label(program, text="Pass")
register_email_entry = Entry(program)
register_email_label = Label(program, text="Email")
register_enter_button = Button(text="Become Member", command=become_member_button_action)
register_back_button = Button(text="Back", command=login_interface)

#storeping cart interface
photo=""
search_component = [photo]
dish_price = Label(program, text="")
cart_next = Button(program, text="Next", command=cart_next_page)
cart_previous = Button(program, text="Previous", command=cart_previous_page)
label_quantity_entry = Entry(program)
label_quantity = Label(program, text="Quantity")
storeping_enter_button = Button(text="Enter", command=storeping_enter_button_action)
storeping_image = Label(image=None)
storeping_did = []
storeping_name = Label(program, text="")
storeping_price=[]
storeping_quantity=[]
cart_button_frame = Frame(program)
storepingcart_checkout_button=Button(cart_button_frame, text="Check out",command=storepingcart_checkout_button_action)
cart_update = Button(cart_button_frame, text="Update", command=update_cart)
cart_update.pack(side="left")
storepingcart_checkout_button.pack(side="left")
cart_label_frame = Frame(program)
storepingcart_checkout_total= Label(cart_label_frame,text=0)
storepingcart_checkout_total_label = Label(cart_label_frame, text="Total:")
storepingcart_checkout_total_label.pack(side="left")
storepingcart_checkout_total.pack(side="left")
label_storepingcart_item =Label(program,text="Item")
label_storepingcart_price =Label(program,text="Unit Price")
label_storepingcart_quantity =Label(program,text="Quantity")
label_storepingcart_sumnarry =Label(program,text="Your order summury:")
item_name_frame1 = Frame(program)
item_name_frame2 = Frame(program)
item_name_frame3 = Frame(program)
item_name_frame4 = Frame(program)
item_name_frame5 = Frame(program)
item_name_frame6 = Frame(program)
cart_item1_image = Label(item_name_frame1, image=None)
cart_item2_image = Label(item_name_frame2, image=None)
cart_item3_image = Label(item_name_frame3, image=None)
cart_item4_image = Label(item_name_frame4, image=None)
cart_item5_image = Label(item_name_frame5, image=None)
cart_item6_image = Label(item_name_frame6, image=None)
storeping_name_label1 = Label(item_name_frame1, text="Name")
storeping_name_label2 = Label(item_name_frame2, text="Name")
storeping_name_label3 = Label(item_name_frame3, text="Name")
storeping_name_label4 = Label(item_name_frame4, text="Name")
storeping_name_label5 = Label(item_name_frame5, text="Name")
storeping_name_label6 = Label(item_name_frame6, text="Name")
cart_item1_image.pack(side="left")
cart_item2_image.pack(side="left")
cart_item3_image.pack(side="left")
cart_item4_image.pack(side="left")
cart_item5_image.pack(side="left")
cart_item6_image.pack(side="left")
storeping_name_label1.pack(side="left")
storeping_name_label2.pack(side="left")
storeping_name_label3.pack(side="left")
storeping_name_label4.pack(side="left")
storeping_name_label5.pack(side="left")
storeping_name_label6.pack(side="left")
cart_item_price1 = Label(program, text="Price")
cart_item_price2 = Label(program, text="Price")
cart_item_price3 = Label(program, text="Price")
cart_item_price4 = Label(program, text="Price")
cart_item_price5 = Label(program, text="Price")
cart_item_price6 = Label(program, text="Price")
cart_item1_entry = Entry(program)
cart_item2_entry = Entry(program)
cart_item3_entry = Entry(program)
cart_item4_entry = Entry(program)
cart_item5_entry = Entry(program)
cart_item6_entry = Entry(program)
cart_item_price_list = [cart_item_price1, cart_item_price2, cart_item_price3, cart_item_price4, cart_item_price5, cart_item_price6]
cart_item_image_list = [cart_item1_image, cart_item2_image, cart_item3_image, cart_item4_image, cart_item5_image, cart_item6_image]
storeping_name_label_list = [storeping_name_label1, storeping_name_label2, storeping_name_label3, storeping_name_label4, storeping_name_label5, storeping_name_label6]
cart_item_entry_list = [cart_item1_entry, cart_item2_entry, cart_item3_entry, cart_item4_entry, cart_item5_entry, cart_item6_entry]
cart_did_list1 = ""
cart_did_list2 = ""
cart_did_list3 = ""
cart_did_list4 = ""
cart_did_list5 = ""
cart_did_list6 = ""
cart_image1 = Label(image=None)
cart_image2 = Label(image=None)
cart_image3 = Label(image=None)
cart_image4 = Label(image=None)
cart_image5 = Label(image=None)
cart_image6 = Label(image=None)
cart_image_list = [cart_image1, cart_image2, cart_image3, cart_image4, cart_image5, cart_image6]
cart_did_list = [cart_did_list1, cart_did_list2, cart_did_list3, cart_did_list4, cart_did_list5, cart_did_list6]

#delivery track interface
delivery_track_frame = Frame(program)
delivery_back_button = Button(delivery_track_frame, text="Back", command=delivery_interface)
delivered = Button(delivery_track_frame, text="Delivered", command=None)
delivered.pack(side=LEFT)
delivery_back_button.pack(side=LEFT)

#delivery interface
selection_label = Label(text="Select your current location")
delivery_order_list = Listbox(program)
delivery_order_listName = Label(program, text="Order list")
node0 = Button(state=DISABLED, text=0, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 0))
node1 = Button(state=DISABLED, text=1, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 1))
node2 = Button(state=DISABLED, text=2, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 2))
node3 = Button(state=DISABLED, text=3, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 3))
node4 = Button(state=DISABLED, text=4, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 4))
node5 = Button(state=DISABLED, text=5, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 5))
node6 = Button(state=DISABLED, text=6, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 6))
node7 = Button(state=DISABLED, text=7, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 7))
node8 = Button(state=DISABLED, text=8, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 8))
node9 = Button(state=DISABLED, text=9, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 9))
node10 = Button(state=DISABLED, text=10, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 10))
node11 = Button(state=DISABLED, text=11, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 11))
node12 = Button(state=DISABLED, text=12, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 12))
node13 = Button(state=DISABLED, text=13, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 13))
node14 = Button(state=DISABLED, text=14, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 14))
node15 = Button(state=DISABLED, text=15, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 15))
node16 = Button(state=DISABLED, text=16, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 16))
node17 = Button(state=DISABLED, text=17, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 17))
node18 = Button(state=DISABLED, text=18, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 18))
node19 = Button(state=DISABLED, text=19, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 19))
node20 = Button(state=DISABLED, text=20, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 20))
node21 = Button(state=DISABLED, text=21, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 21))
node22 = Button(state=DISABLED, text=22, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 22))
node23 = Button(state=DISABLED, text=23, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 23))
node24 = Button(state=DISABLED, text=24, command=lambda: delivery_track_interface(delivery_order_list.get(delivery_order_list.curselection()), 24))
node_list = [node0, node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, 
            node11, node12, node13, node14, node15, node16, node17, node18, node19, node20, 
            node21, node22, node23, node24]
EmptyRoad = PhotoImage(file="images/EmptyRoad.gif").subsample(10,10)
EmptyRoads = PhotoImage(file="images/EmptyRoads.gif").subsample(10,10)
StopSign = PhotoImage(file="images/StopSign.gif").subsample(10,10)
StopSigns = PhotoImage(file="images/StopSigns.gif").subsample(10,10)
GreenLight = PhotoImage(file="images/GreenLight.gif").subsample(10,10)
GreenLights = PhotoImage(file="images/GreenLights.gif").subsample(10,10)
CarTraffic = PhotoImage(file="images/CarTraffic.gif").subsample(10,10)
CarTraffics = PhotoImage(file="images/CarTraffics.gif").subsample(10,10)
legend_frame = Frame(program)
legend_frame1 = Frame(legend_frame)
legend_frame2 = Frame(legend_frame)
legend_button = Button(legend_frame1, state=DISABLED, highlightbackground="yellow")
legend_button_text = Label(legend_frame1, text="Start/Destination")
legend_button.pack(side="left")
legend_button_text.pack(side="left")
legend_label_free = Label(legend_frame2, bg="Green")
legend_label_text_free = Label(legend_frame2, text="Path")
legend_label_free.pack(side="left")
legend_label_text_free.pack(side="left")
legend_label_block = Label(legend_frame2, bg="Red")
legend_label_text_block = Label(legend_frame2, text="Blocked")
legend_label_block.pack(side="left")
legend_label_text_block.pack(side="left")
legend_label_notra = Label(legend_frame2, bg="yellow")
legend_label_text_notra = Label(legend_frame2, text="No traffic")
legend_label_notra.pack(side="left")
legend_label_text_notra.pack(side="left")
legend_frame1.pack(side="top")
legend_frame2.pack(side="top")
edge1 = Label(image=EmptyRoads)
edge2 = Label(image=EmptyRoads)
edge3 = Label(image=EmptyRoads)
edge4 = Label(image=EmptyRoads)
edge10 = Label(image=EmptyRoads)
edge11 = Label(image=EmptyRoads)
edge12 = Label(image=EmptyRoads)
edge13 = Label(image=EmptyRoads)
edge20 = Label(image=EmptyRoads)
edge21 = Label(image=EmptyRoads)
edge28 = Label(image=EmptyRoads)
edge29 = Label(image=EmptyRoads)
edge30 = Label(image=EmptyRoads)
edge31 = Label(image=EmptyRoads)
edge37 = Label(image=EmptyRoads)
edge38 = Label(image=EmptyRoads)
edge39 = Label(image=EmptyRoads)
edge40 = Label(image=EmptyRoads)
edge5 = Label(image=EmptyRoad)
edge6 = Label(image=EmptyRoad)
edge8 = Label(image=EmptyRoad)
edge9 = Label(image=EmptyRoad)
edge14 = Label(image=EmptyRoad)
edge15 = Label(image=EmptyRoad)
edge16 = Label(image=EmptyRoad)
edge17 = Label(image=EmptyRoad)
edge18 = Label(image=EmptyRoad)
edge23 = Label(image=EmptyRoad)
edge24 = Label(image=EmptyRoad)
edge25 = Label(image=EmptyRoad)
edge26 = Label(image=EmptyRoad)
edge27 = Label(image=EmptyRoad)
edge32 = Label(image=EmptyRoad)
edge33 = Label(image=EmptyRoad)
edge35 = Label(image=EmptyRoad)
edge36 = Label(image=EmptyRoad)
h_edge_matrix = [[0 for i in range(25)] for j in range(25)]
v_edge_matrix = [[0 for i in range(25)] for j in range(25)]
h_edge_matrix[0][1] = edge1
h_edge_matrix[1][2] = edge2
h_edge_matrix[2][3] = edge3
h_edge_matrix[3][4] = edge4
v_edge_matrix[0][5] = edge5
v_edge_matrix[1][6] = edge6
v_edge_matrix[3][8] = edge8
v_edge_matrix[4][9] = edge9
h_edge_matrix[5][6] = edge10
h_edge_matrix[6][7] = edge11
h_edge_matrix[7][8] = edge12
h_edge_matrix[8][9] = edge13
v_edge_matrix[5][10] = edge14
v_edge_matrix[6][11] = edge15
v_edge_matrix[7][12] = edge16
v_edge_matrix[8][13] = edge17
v_edge_matrix[9][14] = edge18
h_edge_matrix[11][12] = edge20
h_edge_matrix[12][13] = edge21
v_edge_matrix[10][15] = edge23
v_edge_matrix[11][16] = edge24
v_edge_matrix[12][17] = edge25
v_edge_matrix[13][18] = edge26
v_edge_matrix[14][19] = edge27
h_edge_matrix[15][16] = edge28
h_edge_matrix[16][17] = edge29
h_edge_matrix[17][18] = edge30
h_edge_matrix[18][19] = edge31
v_edge_matrix[15][20] = edge32
v_edge_matrix[16][21] = edge33
v_edge_matrix[18][23] = edge35
v_edge_matrix[19][24] = edge36
h_edge_matrix[20][21] = edge37
h_edge_matrix[21][22] = edge38
h_edge_matrix[22][23] = edge39
h_edge_matrix[23][24] = edge40
h_edge_matrix[1][0]= edge1
h_edge_matrix[2][1]= edge2
h_edge_matrix[3][2]= edge3
h_edge_matrix[4][3]= edge4
v_edge_matrix[5][0]= edge5
v_edge_matrix[6][1]= edge6
v_edge_matrix[8][3]= edge8
v_edge_matrix[9][4]= edge9
h_edge_matrix[6][5]= edge10
h_edge_matrix[7][6]= edge11
h_edge_matrix[8][7]= edge12
h_edge_matrix[9][8]= edge13
v_edge_matrix[10][5] = edge14
v_edge_matrix[11][6] = edge15
v_edge_matrix[12][7] = edge16
v_edge_matrix[13][8] = edge17
v_edge_matrix[14][9] = edge18
h_edge_matrix[12][11] = edge20
h_edge_matrix[13][12] = edge21
v_edge_matrix[15][10] = edge23
v_edge_matrix[16][11] = edge24
v_edge_matrix[17][12] = edge25
v_edge_matrix[18][13] = edge26
v_edge_matrix[19][14] = edge27
h_edge_matrix[16][15] = edge28
h_edge_matrix[17][16] = edge29
h_edge_matrix[18][17] = edge30
h_edge_matrix[19][18] = edge31
v_edge_matrix[20][15] = edge32
v_edge_matrix[21][16] = edge33
v_edge_matrix[23][18] = edge35
v_edge_matrix[24][19] = edge36
h_edge_matrix[21][20] = edge37
h_edge_matrix[22][21] = edge38
h_edge_matrix[23][22] = edge39
h_edge_matrix[24][23] = edge40
h_edge_list = [edge1, edge2, edge3, edge4, edge10, edge11, edge12, edge13, edge20, edge21, edge28,
            edge29, edge30, edge31, edge37, edge38, edge39, edge40]
v_edge_list = [edge5, edge6, edge8, edge9, edge14, edge15, edge16, edge17, edge18, edge23, edge24,
            edge25, edge26, edge27, edge32, edge33, edge35, edge36]
delivery_order_listName = Label(program, text="Order list")
signout_button = Button(text="Sign Out", command=signout_button_action)
delivery_frame = Frame(program)
issue_warning = Button(delivery_frame, text="Issue warning", command=lambda: delivery_track_interface_action(1))
order_track_button = Button(delivery_frame, text="Track", command=lambda: delivery_track_interface_action(0))
order_track_button.pack(side="left")
issue_warning.pack(side="left")

#start interface
search_frame = Frame(program)
search_entry = Entry(search_frame)
#search_button = Button(search_frame, text="Search", command = lambda: search_button_action(search_entry.get()))
#search_entry.pack(side="left")
#search_button.pack(side="left")
chef_name = Label(program, text="All")
info_button = Button(text="Profile", command=profile_button_action)
comment_button = Button(text="Comment", command=comment_interface)


logo = PhotoImage(file="images/FASTLaneFood.gif")
logo = logo.zoom(1) #with 250, I ended up running out of memory


refresh_button = Button(text="Refresh", image =logo, command=lambda: refresh_menu(1))

bag = PhotoImage(file="images/BagIcon.gif")
storeping_cart_items = Button(text="Your storeping Cart", image = bag, command=storeping_cart_button_action)


signout_button = Button(text="Sign Out", command=signout_button_action)

profile = PhotoImage(file="images/ProfileIcon.gif")
login_button = Button(text="Sign In", image = profile, command=login_interface)

next_page_button = Button(text="-> Next Restaurant", command=menu_next_page)
previous_page_button = Button(text="<- Previous Restaurant", command=menu_previous_page)


NotAvailable_photo = PhotoImage(file="images/NotAvailable.gif")
NotAvailable_photo_small = PhotoImage(file="images/NotAvailable.gif").subsample(2,2)
dish_image1 = Label(image=None)
dish_name1 = Label(program, text="Name")
dish_price1 = Label(program, text="Price")
dish_buy1 = Button(text="Add to bag", command=lambda: add_cart_button_action(0))
dish_did1=""
dish_comment1 = Button(text="View", command=lambda: view_comment(dish_did_list[0]))
dish_image2 = Label(image=None)
dish_name2 = Label(program, text="Name")
dish_price2 = Label(program, text="Price")
dish_buy2 = Button(text="Add to bag", command=lambda: add_cart_button_action(1))
dish_did2=""
dish_comment2 = Button(text="View", command=lambda: view_comment(dish_did_list[1]))
dish_image3 = Label(image=None)
dish_name3 = Label(program, text="Name")
dish_price3 = Label(program, text="Price")
dish_buy3 = Button(text="Add to bag", command=lambda: add_cart_button_action(2))
dish_did3=""
dish_comment3 = Button(text="View", command=lambda: view_comment(dish_did_list[2]))
dish_image4 = Label(image=None)
dish_name4 = Label(program, text="Name")
dish_price4 = Label(program, text="Price")
dish_buy4 = Button(text="Add to bag", command=lambda: add_cart_button_action(3))
dish_did4=""
dish_comment4 = Button(text="View", command=lambda: view_comment(dish_did_list[3]))
dish_image5 = Label(image=None)
dish_name5 = Label(program, text="Name")
dish_price5 = Label(program, text="Price")
dish_buy5 = Button(text="Add to bag", command=lambda: add_cart_button_action(4))
dish_did5=""
dish_comment5 = Button(text="View", command=lambda: view_comment(dish_did_list[4]))
dish_image6 = Label(image=None)
dish_name6 = Label(program, text="Name")
dish_price6 = Label(program, text="Price")
dish_buy6 = Button(text="Add to bag", command=lambda: add_cart_button_action(5))
dish_did6=""
dish_comment6 = Button(text="View", command=lambda: view_comment(dish_did_list[5]))
img1=""
img2=""
img3=""
img4=""
img5=""
img6=""
dish_comment_list = [dish_comment1, dish_comment2, dish_comment3, dish_comment4, dish_comment5, dish_comment6]
dish_image_list = [dish_image1, dish_image2, dish_image3, dish_image4, dish_image5, dish_image6]
dish_buy_list = [dish_buy1, dish_buy2, dish_buy3, dish_buy4, dish_buy5, dish_buy6]
dish_did_list = [dish_did1, dish_did2, dish_did3, dish_did4, dish_did5, dish_did6]
dish_name_list = [dish_name1, dish_name2, dish_name3, dish_name4, dish_name5, dish_name6]
dish_price_list = [dish_price1, dish_price2, dish_price3, dish_price4, dish_price5, dish_price6]
dish_img_list = [img1, img2, img3, img4, img5, img6]

start_interface()
manager.auto_demote_promote_employee()
manager.auto_vip_block()
program.mainloop()
