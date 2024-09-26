import os 
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from operator import itemgetter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
from dotenv import load_dotenv
from digitalk_utils import *
import pytz
# from mail import *
# load_dotenv()
try:
    client = MongoClient("mongodb+srv://admin-infinivirt:GtqUdrSPotN0ieaC@euscallstor.41mox.mongodb.net/" )
    db = client.db_infinivirt
    s3_test = db.cdr_digitalk_2024

    now = datetime.now(pytz.utc) - timedelta(minutes=30)
    now_naive = now.replace(tzinfo=None)

    print(now, now_naive)
    columns = debug_columns()

    approximate_filename = build_approximate_filename(now)

    file_name = get_file_name(approximate_filename)[0]['Key']
    if(now_naive >= datetime(year=2024, month=5, day=31, hour=19, minute=0, second=0)):
        if(file_name):
            data = get_cdr_file(file_name)
            [inbound, outbound] = separate_incoming(data)
            if outbound.empty:
                # sendMail(rf'The file {file_name} has no data') 
                1+1 
            else:
                columns_to_drop_existing = [col for col in columns if col in outbound.columns]

                outbound = outbound.drop(columns_to_drop_existing, axis=1)
                outbound['sell_start_bal'] = outbound['sell_start_bal'].astype(str) 
                outbound['sell_end_bal'] = outbound['sell_end_bal'].astype(str)   
                outbound['asig_to'] = outbound['asig_to'].astype(str) 
                outbound['bsig_to'] = outbound['bsig_to'].astype(str) 
                s3_test.insert_many(outbound.to_dict('records'))
                

            if not inbound.empty:
                columns_to_drop_existing = [col for col in columns if col in outbound.columns]

                inbound = change_columns(inbound)
                inbound = inbound.drop(columns_to_drop_existing, axis=1)
                inbound['sell_start_bal'] = inbound['sell_start_bal'].astype(str) 
                inbound['sell_end_bal'] = inbound['sell_end_bal'].astype(str)   
                inbound['asig_to'] = inbound['asig_to'].astype(str) 
                inbound['bsig_to'] = inbound['bsig_to'].astype(str) 
                s3_test.insert_many(inbound.to_dict('records'))

except Exception as e:
    archivo = open("log-digitalk.txt", "a")
    archivo.write('\n')
    archivo.write(str(e) + '-- Filename: ' + file_name)
    archivo.close()



