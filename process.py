import requests
import wrap_db, wrap_cc

def init_system():
    wrap_db.initilise_db()
    wrap_cc.initilise_cc()

def load_demo():
    #print(wrap_cc.read_ref(True))
    #wrap_cc.load_demo_cc()
    wrap_db.load_demo_db()

def show_full_network():
    return wrap_cc.read_all()

def get_owner_holdings():
    return wrap_cc.read_all(easy = True)
