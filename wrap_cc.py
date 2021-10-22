import json
import requests
from requests.auth import HTTPBasicAuth

with open("config/config.json") as f_in:
    _CONFIG = json.load(f_in)

def initilise_cc():
    with open("config/init_cc.json") as f_in:
        init_cc = json.load(f_in)

    for i_ in init_cc:
        url = _CONFIG["ccode"]["server_loc"] + '/' + i_["command"]
        headers = _CONFIG["ccode"]["headers"]
        body = i_["body"]
        type = i_["type"]

        if type == "POST":
            r = requests.post(url, headers=headers, data=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
        elif type == "GET":
            r = requests.get(url, headers=headers, data=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))

        print(i_["command"] + ", " + str(r.text))

def load_demo_cc():
    with open("config/demo_cc.json") as f_in:
        demo_cc = json.load(f_in)
    
    ref_data = read_ref(easy = True)

    lc_shape_id = ref_data["shapes"]["local coin"]
    cc_shape_id = ref_data["shapes"]["community coin"]
    demo_town_id = ref_data["towns"]["Friendly Town"]
    last_owner_id = ""

    for i_ in demo_cc:
        url = _CONFIG["ccode"]["server_loc"] + '/' + i_["command"]
        headers = _CONFIG["ccode"]["headers"]
        body = i_["body"]

        body_s = json.dumps(body)
        body_s = body_s.replace("[LC_SHAPE_ID]", lc_shape_id)
        body_s = body_s.replace("[CC_SHAPE_ID]", cc_shape_id)
        body_s = body_s.replace("[DEMO_TOWN_ID]", demo_town_id)
        body_s = body_s.replace("[LAST_OWNER_ID]", last_owner_id)
        body = json.loads(body_s)

        r = requests.post(url, headers=headers, json=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
        r_obj = json.loads(r.text)

        if i_["command"] == "create-owner":
            last_owner_id = r_obj["message"]["id"]

        print(i_["command"] + ", " + str(r.text))

def read_all(easy = False):
    url = _CONFIG["ccode"]["server_loc"] + '/read-all'
    headers = _CONFIG["ccode"]["headers"]

    r = requests.get(url, headers=headers, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))

    r_obj = json.loads(r.text)

    if not easy:
        return r_obj
    else:
        owners = []
        if "owners" in r_obj:
            for o in r_obj["message"]["owners"]:
                owners.append({"id": o["id"], "username": o["username"], "userType": o["userType"], "coins": []})

            for c in r_obj["message"]["caps"]:
                o_ = [x for x in owners if x["id"] == c["owner"]["id"]][0]
                o_["coins"].append({"id": c["id"], "shape": c["shape"]["name"], "color": c["color"], "size": c["size"]})
        
        return owners

def read_ref(easy = False):
    url = _CONFIG["ccode"]["server_loc"] + '/read-ref'
    headers = _CONFIG["ccode"]["headers"]

    r = requests.get(url, headers=headers, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))

    r_obj = json.loads(r.text)
    
    if not easy:
        return r_obj
    else:
        ret_obj = {}
        ret_obj["shapes"] = {}
        for s in r_obj["message"]["shapes"]:
            ret_obj["shapes"][s["name"]] = s["id"]
        
        ret_obj["towns"] = {}
        for t in r_obj["message"]["towns"]:
            ret_obj["towns"][t["name"]] = t["id"]

        return ret_obj

