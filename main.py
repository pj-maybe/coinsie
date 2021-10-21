
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

from colorama import Fore
from colorama import Style

from random import *
import linecache

from prettytable import PrettyTable
import process

with open("config/config.json") as f_in:
    _CONFIG = json.load(f_in)

def random_name():
    fn_num = randint(1, 4945)
    fname = linecache.getline("fnames.txt", fn_num).replace('\n','')    
    return fname

def test_server():
    url = 'http://localhost:5000/testapi'
    r = requests.get(url)
    print(r.text)

def call_init_demo():
    print()
    print("for a real hard reset, do on the cli- ")
    print("cd marbles-api && ./resetServer.sh")
    print()
    # url = 'http://localhost:5000/init_demo'
    # r = requests.get(url)
    # print(r)
    process.init_demo()

def call_show_data():
    url = 'http://localhost:5000/show_data'
    r = requests.get(url)
    r_text = r.text
    r_json = json.loads(r_text)
    print(json.dumps(r_json, indent=4, sort_keys=True))

def call_get_holdings():
    url = 'http://localhost:5000/get_holdings'
    r = requests.get(url)
    r_text = r.text
    r_json = json.loads(r_text)
    #print(r_json)

    user_table = PrettyTable()
    user_table.field_names = ["username", "LC", "CC"]

    for o in r_json:
        if o["userType"] == 'user':
            user_table.add_row([o["username"], sum([x['size'] for x in o["coins"] if x["shape"] == "local coin"]), sum([x['size'] for x in o["coins"] if x["shape"] == "community coin"])])

    print()
    print(user_table)

def call_get_user_holdings():
    username = input("Enter Username (cancel): ")
    username = username.strip()        
    if username == "":
        return

    url = 'http://localhost:5000/get_holdings'
    r = requests.get(url)
    r_text = r.text
    r_json = json.loads(r_text)

    for o in r_json:
        if o["username"] == username:
            print()
            print(json.dumps(o, indent=4, sort_keys=True))

def call_add_owner():
    usertype = input("Enter User Type [user/merchant/cgroup] (user): ")
    usertype = usertype.strip()        
    if usertype == "":
        usertype = "user"        
    print(f"{Fore.LIGHTCYAN_EX}" + usertype + f"{Style.RESET_ALL}")

    rname = random_name()
    username = input("Enter New User Name (" + rname + "): ")
    username = username.strip()        
    if username == "":
        username = rname
    print(f"{Fore.LIGHTCYAN_EX}" + username + f"{Style.RESET_ALL}")

    user_lcoin = input("Enter Local Coin Size (0): ")
    user_lcoin = user_lcoin.strip()        
    if user_lcoin == "":
        user_lcoin = 0        
    else:
        user_lcoin = int(user_lcoin)
    print(f"{Fore.LIGHTCYAN_EX}" + str(user_lcoin) + f"{Style.RESET_ALL}")
    
    user_ccoin = input("Enter Community Coin Size (0): ")
    user_ccoin = user_ccoin.strip()        
    if user_ccoin == "":
        user_ccoin = 0        
    else:
        user_ccoin = int(user_ccoin)
    print(f"{Fore.LIGHTCYAN_EX}" + str(user_ccoin) + f"{Style.RESET_ALL}")
    
    url = 'http://localhost:5000/add_owner'
    #r = requests.get(url)
    body = {"usertype": usertype, "username": username, "user_lcoin": user_lcoin, "user_ccoin": user_ccoin, }
    r = requests.post(url, json=body)
    r_text = r.text

    r_json = json.loads(r_text)
    #print(json.dumps(r_json, indent=4, sort_keys=True))

def call_transfer_cap():
    username_from = input("Enter *From* Username (cancel): ")
    username_from = username_from.strip()        
    if username_from == "":
        return

    username_to = input("Enter *To* Username (cancel): ")
    username_to = username_to.strip()        
    if username_to == "":
        return

    shapename = input("Enter Shape Name [LC/CC] (LC): ")
    shapename = shapename.strip()        
    if shapename == "CC":
        shapename = "community coin"
    else:
        shapename = "local coin"

    color = input("Enter Color Name (blue): ")
    color = color.strip()        
    if color == "":
        color = "blue"
    
    amount = input("Enter Coin Amount (1): ")
    amount = amount.strip()        
    if amount == "":
        amount = 1
    else:
        amount = int(amount)
                
    url = 'http://localhost:5000/transfer_cap2'
    #r = requests.get(url)
    body = {"username_from": username_from, "username_to": username_to, "shapename": shapename, "color": color, "amount": amount}
    r = requests.post(url, json=body)
    r_text = r.text

    r_json = json.loads(r_text)
    #print(json.dumps(r_json, indent=4, sort_keys=True))

    print()
    print(r_json)

def test_ccode():
    url = _CONFIG["ccode"]["server_loc"] + '/read-all'
    r = requests.get(url, verify=False, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    r_text = r.text
    r_json = json.loads(r_text)
    print(r_json)

def main_menu():
    all_done = False

    while not all_done:    
        print()
        print(f"{Style.BRIGHT}{Fore.YELLOW}Welcome to Townsie {Fore.WHITE}Coins{Fore.YELLOW} Demo{Style.RESET_ALL}")
        print()
        print(f"===> {Fore.GREEN}{Style.BRIGHT}ADMIN MENU{Style.RESET_ALL} <===")
        print("--------------------")
        print()
        print(f"{Fore.YELLOW}0{Fore.WHITE}: Reset network & setup demo")
        print()
        print(f"{Fore.YELLOW}1{Fore.WHITE}: Display the full network") 
        print(f"{Fore.YELLOW}2{Fore.WHITE}: Display owner holdings") 
        print(f"{Fore.YELLOW}3{Fore.WHITE}: Display single user detail") 
        print()
        print(f"{Fore.YELLOW}4{Fore.WHITE}: Add a demo owner (any type)")
        print(f"{Fore.YELLOW}5{Fore.WHITE}: Transfer a coin between users")
        print()
        print(f"{Fore.YELLOW}Q{Fore.WHITE}: {Fore.WHITE}Quit{Style.RESET_ALL}")
        print()

        selc =  input("Selection: ")

        if selc is None:
            return
        elif selc == "0":
            call_init_demo()
        elif selc == "1":
            call_show_data()
        elif selc == "2":
            call_get_holdings()        
        elif selc == "3":
            call_get_user_holdings() 
        elif selc == "4":
            call_add_owner()
        elif selc == "5":
            call_transfer_cap()            
        elif selc == "Q":            
            all_done = True
        else:
            print("?")

    

def main():
    main_menu()


if __name__ == '__main__':
    main()