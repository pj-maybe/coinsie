import sqlite3
import os
import json

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
                print(" execute,  [" + str(l_.strip) + "]")
    
    conn.commit()
