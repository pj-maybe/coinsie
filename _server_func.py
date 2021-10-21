
import os
import json
import requests
from requests.auth import HTTPBasicAuth

with open("config.json") as f_in:
    _CONFIG = json.load(f_in)

def show_whole_data():
    url = _CONFIG["ccode"]["server_loc"] + '/read-all'
    r = requests.get(url, verify=False, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    #r_text = r.text
    #r_json = json.loads(r_text)
    #print(json.dumps(r_json, indent=4, sort_keys=True))
    return r.text
    
def get_holdings():
    url = _CONFIG["ccode"]["server_loc"] + '/read-all'
    r = requests.get(url, verify=False, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    r_text = r.text
    r_json = json.loads(r_text)

    owners = []
    for o in r_json["message"]["owners"]:
        owners.append({"id": o["id"], "username": o["username"], "userType": o["userType"], "coins": []})

    for c in r_json["message"]["caps"]:
        o_ = [x for x in owners if x["id"] == c["owner"]["id"]][0]
        o_["coins"].append({"id": c["id"], "shape": c["shape"]["name"], "color": c["color"], "size": c["size"]})
    
    owners_str = json.dumps(owners)
    return owners_str

def transfer_cap2(username_from, username_to, shapename, color, amount):
    url = _CONFIG["ccode"]["server_loc"] + '/read-all'
    r = requests.get(url, verify=False, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    r_text = r.text
    r_obj = json.loads(r_text)
    r_owners = r_obj["message"]["owners"]

    for o in r_owners:
        if o["username"] == username_from:
            o_id = o["id"]

        if o["username"] == username_to:
            newo_id = o["id"]

    url = _CONFIG["ccode"]["server_loc"] + '/read-ref'
    headers = _CONFIG["ccode"]["headers"]
    r = requests.get(url, headers=headers, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))

    r_obj = json.loads(r.text)
    t_id = [x for x in r_obj["message"]["towns"] if x["name"] == "Friendly Town"][0]["id"]
    s_id = [x for x in r_obj["message"]["shapes"] if x["name"] == shapename][0]["id"]
        
    url = _CONFIG["ccode"]["server_loc"] + '/transfer-cap2'
    headers = _CONFIG["ccode"]["headers"]
    body_str = '''
    {
        "owner_id": "''' + o_id + '''",
        "new_owner_id": "''' + newo_id + '''",
        "shape_id": "''' + s_id + '''",
        "color": "''' + color + '''",
        "amount": "''' + str(amount) + '''"
    }
    '''
    print(body_str)
    body = json.loads(body_str)
    r = requests.post(url, headers=headers, json=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    print("r..................")
    print(r.text)
    
    return r

def add_demo_owner(usertype, username, user_lcoin, user_ccoin):
    url = _CONFIG["ccode"]["server_loc"] + '/read-ref'
    headers = _CONFIG["ccode"]["headers"]
    r = requests.get(url, headers=headers, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))

    r_obj = json.loads(r.text)
    t_id = [x for x in r_obj["message"]["towns"] if x["name"] == "Friendly Town"][0]["id"]
    lc_id = [x for x in r_obj["message"]["shapes"] if x["name"] == "local coin"][0]["id"]
    cc_id = [x for x in r_obj["message"]["shapes"] if x["name"] == "community coin"][0]["id"]

    url = _CONFIG["ccode"]["server_loc"] + '/create-owner'
    headers = _CONFIG["ccode"]["headers"]
    body_str = '''
    {
        "username" : "''' + username + '''",
        "wordpressID": "dummy",
        "userwcid": "dummy",
        "company": "United Caps",
        "password":"dummy",
        "usertype": "''' + usertype + '''",
        "colorLineAmount": [{
            "color":"blue",
            "lineAmount":100
        }],
        "shapeLineAmount":[{
            "shape":"local coin",
            "lineAmount":100
        },{
            "shape":"community coin",
            "lineAmount":100
        }],
        "towns": "Friendly Town"
    }
    '''
    body = json.loads(body_str)
    r = requests.post(url, headers=headers, json=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    r_o = r
    print("create-owner" + ", " + str(r_o.text))
    r_obj = json.loads(r.text)
    o_id = r_obj["message"]["id"]

    url = _CONFIG["ccode"]["server_loc"] + '/create-cap'
    headers = _CONFIG["ccode"]["headers"]
    body_str = '''
    {
        "color":"blue",
        "size": ''' + str(user_lcoin) + ''',
        "shape_id":"''' + lc_id + '''",
        "owner_id":["''' + o_id + '''"],
        "town_id": "''' + t_id + '''"
    }
    '''
    body = json.loads(body_str)
    r = requests.post(url, headers=headers, json=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    print("create-cap" + ", " + str(r.text))

    url = _CONFIG["ccode"]["server_loc"] + '/create-cap'
    headers = _CONFIG["ccode"]["headers"]
    body_str = '''
    {
        "color":"blue",
        "size": ''' + str(user_ccoin) + ''',
        "shape_id":"''' + cc_id + '''",
        "owner_id":["''' + o_id + '''"],
        "town_id": "''' + t_id + '''"
    }
    '''
    body = json.loads(body_str)
    r = requests.post(url, headers=headers, json=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
    print("create-cap" + ", " + str(r.text))

    return r_o

