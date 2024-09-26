import os 
import io
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from operator import itemgetter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
# from changeColumns import *
from dotenv import load_dotenv
from sbc_utils import *
import gzip 
import zipfile 
import boto3
from dateutil.parser import *
import pytz


load_dotenv()



now = datetime.now(pytz.utc) - timedelta(hours=2)
now_naive = now.replace(tzinfo=None)
client = MongoClient("mongodb+srv://admin-infinivirt:GtqUdrSPotN0ieaC@euscallstor.41mox.mongodb.net/" )



header = ['Setup Time', 'Connect Time', 'Node Time Zone', 'Call Duration(centisegundos)', 'Ingress Calling User(From Customer)', 'Ingress Dialed User(TO Customer)', 'Egress Calling User(From SBC)', 'Egress Called User(To SBC)', 'Ingress Call Source IP(IP Origen)', 'Ingress Calling Host(IP SBC)', 'Egress Call Destination IP(IP Destino)', 'Egress SIP Termination Reason', 'Egress Termination Reason', 'Ingress IP Group Name(IP Group Origen)', 'Egress IP Group Name(Ipg Destino)', 'Ingress Var Call User Defined 2(Cliente)', 'Session ID', 'Ingress Call ID', 'Egress Call ID', 'SIP Interface Origen', 'SIP Interface Destino', 'Ingress Source URI Before Manipulation']
formato_entrada = '%H:%M:%S.%f UTC %a %b %d %Y'
formato_salida = '%Y-%m-%d %H:%M:%S.%f'

if(now_naive >= datetime(year=2024, month=5, day=31, hour=16, minute=0, second=0)):
    try:
        s3_client = boto3.client('s3')
        uri= 'mongodb+srv://julian-berrio:jkXfcfEAld74GzJJ@euscallstor.41mox.mongodb.net/'
        bucket_name = os.getenv('BUCKET_NAME')

        db = client.db_infinivirt
        sbc_backup = db.cdr_sbc_2024



        approximate_name = build_approximate_filename(now)
        filename_list = get_file_name(approximate_name)
    # print(filename_list)
        for obj in filename_list:
            data_list = []

            name = obj['Key']
            print(name)
            data = get_cdr_file_csv(name)
            for row in data:
                if(len(row) <= 22):
                    document = zip(header, row)
                    document = dict(document)
                    setup_time = document['Setup Time']
                    connect_time = document['Connect Time']
                    document['Call Duration(centisegundos)'] = int(document['Call Duration(centisegundos)'])
                    setup_time_converted = datetime.strptime(setup_time, formato_entrada)
                    connect_time_converted = datetime.strptime(connect_time, formato_entrada)
                    
                    document['Setup Time'] = setup_time_converted.strftime(formato_salida)
                    document['Connect Time'] = connect_time_converted.strftime(formato_salida)
                    
                    data_list.append(document)
                else: 
                    archivo = open("BadRows-.txt", "a")
                    archivo.write('\n')
                    archivo.write(', '.join(row))
                    archivo.close()

            sbc_backup.insert_many(data_list)
            # print(data)
            # print(import_data(unzip))
                
    except Exception as e:
        archivo = open("logs/log-sbc.txt", "a")
        archivo.write('\n')
        archivo.write('FileName: '+ name+ ' error: '+e)
        archivo.close()

