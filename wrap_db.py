import sqlite3
import os
import json
import wrap_cc
import pandas as pd

with open("config/config.json") as f_in:
    _CONFIG = json.load(f_in)

def initilise_db():
    fn = "dbase/coinsie.db"    
    os.remove(fn) if os.path.exists(fn) else None
    
    conn = sqlite3.connect(fn)
    cursor = conn.cursor()
    
    with open('config/init_db.sql') as f_in:
        for l_ in f_in:
            if len(l_.strip()) > 0:
                cursor.execute(l_.strip())
                print(" execute,  [" + str(l_.strip()) + "]")
    
    conn.commit()

def load_demo_db():
    r_obj = wrap_cc.read_all(easy= True)
    o_ids = {}
    for o_ in r_obj:
        o_ids[o_["username"]] = o_["id"]

    r_ref = wrap_cc.read_ref(easy= True)

    fn = "dbase/coinsie.db"  
    
    conn = sqlite3.connect(fn)
    cursor = conn.cursor()
    
    tables = ["UserDetails", "OwnerDetails", "OfferDetails"]
    for t_ in tables:
        cursor.execute("DELETE FROM " + t_.strip())

    conn.commit()

    demo_db = pd.read_csv("config/demo_db1.csv")

    for index, row in demo_db.iterrows():
        print(row['username'])

    i = 0


    # with open('config/demo_db.txt') as f_in:
    #     for l_ in f_in:
    #         if len(l_.strip()) > 0:
                

    #             first_qry = " INSERT INTO OwnerDetails ( OwnerId, OwnerType, ShortText, LongText ) VALUES ( 'OwnerId', 'OwnerType', 'ShortText', 'LongText' ) "
    #             second_qry = " INSERT INTO OfferDetails (OfferId, OwnerId, OfferType, StarsNeeded, Direction, ShapeId, ColorId,CoinSize, ShortText, LongText) " + \
    #                          " VALUES ('OfferId', 'OwnerId', 'OfferType', 'StarsNeeded', 'Direction', 'ShapeId', 'ColorId', 'CoinSize', 'ShortText', 'LongText') "

    #             cursor.execute(l_.strip())
    #             print(" execute,  [" + str(l_.strip()) + "]")
    
    
        
    
    # conn.commit()

