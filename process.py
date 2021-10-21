import requests
import wrap_db, wrap_cc

def init_demo():
    wrap_db.initilise_db()
    wrap_cc.initilise_cc()