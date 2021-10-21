import json
import requests
from requests.auth import HTTPBasicAuth

with open("config/config.json") as f_in:
    _CONFIG = json.load(f_in)

def initilise_cc():
    with open("config/init_cc.json") as f_in:
        initcc = json.load(f_in)

    for i_ in initcc:
        url = _CONFIG["ccode"]["server_loc"] + '/' + i_["command"]
        headers = _CONFIG["ccode"]["headers"]
        body = i_["body"]
        type = i_["type"]

        if type == "POST":
            r = requests.post(url, headers=headers, data=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))
        elif type == "GET":
            r = requests.get(url, headers=headers, data=body, auth= HTTPBasicAuth('admin', _CONFIG["ccode"]["admin_pw"]))

        print(i_["command"] + ", " + str(r.text))

