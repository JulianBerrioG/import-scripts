import os 
import io
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from operator import itemgetter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
# from changeColumns import *
from dotenv import load_dotenv
# from utils import *
import gzip 
import zipfile 
import boto3
import csv

load_dotenv()

s3_client = boto3.client('s3')
uri= 'mongodb+srv://julian-berrio:jkXfcfEAld74GzJJ@euscallstor.41mox.mongodb.net/'
bucket_name = os.getenv('BUCKET_NAME')
file = pd.read_csv(rf'Cambios_En_Columnas_Digitalk.csv', header=None )

def build_approximate_filename(now):
    today = now
    print("Today's date:", today) 
    hour = today.strftime("%H") 
    minutes = int(today.strftime("%M")) 
    today = today.strftime('%d%m%Y')
    minutes = minutes - (minutes%15)

    print('Hour: ', hour)
    print('Minute', minutes)    

    last_file= 'CDR_' + today + '-' + str(hour)+ ''+ str(minutes).zfill(2)
    # last_file= 'CDR_01012023-0200'
    return last_file

def log_incomplete_calls(name):
    client = MongoClient(uri)
    db = client.db_infinivirt_staging
    failed_collection = db.failed
    failed_collection.insert_one({"name": name})

def get_file_name(approximate_filename):
    global bucket_name
    all_objects = []
    try:
        response = s3_client.list_objects(
            Bucket=bucket_name,
            Delimiter=',',
            EncodingType='url',
            Marker='string',
            Prefix=rf'xDR/Digitalk/2024/{approximate_filename}',
            RequestPayer='requester',
            OptionalObjectAttributes=[
                'RestoreStatus',
            ]
        )

        return response['Contents']
    # resultado = subprocess.run(script, capture_output=True, text=True)
        # if(datos_json):
        #     return rf"{datos_json[0]['Key']}"
        # else:
        #     log_incomplete_calls(approximate_filename)
        #     body ={"file_name": approximate_filename}
        #     print(body)
        #     #requests.post('http://localhost:8081/api/mail-service/mongoErrorLog', body)

        #     print('error')
        #     return None
    except Exception:
        print(Exception)

def get_cdr_file(name):
    global bucket_name
    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=name
        )
        byteObj = io.BytesIO(response['Body'].read())
        # with  zipfile (fileobj=BytesIO(data)) as gz_file:
        with zipfile.ZipFile(byteObj, 'r') as zip_ref:
            zip_file_list = zip_ref.namelist()
            with zip_ref.open(zip_ref.namelist()[0]) as data_file:
                data = pd.read_csv(data_file, low_memory=False)
                return data
    except Exception:
        print(Exception)

def get_cdr_file_csv(name):
    global bucket_name
    
    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=name
        )
        byteObj = io.BytesIO(response['Body'].read())
        with zipfile.ZipFile(byteObj, 'r') as zip_ref:
            zip_file_list = zip_ref.namelist()
            with zip_ref.open(zip_ref.namelist()[0]) as data_file:

                # print(data_file)

            # data = pd.read_csv(zip_ref,on_bad_lines='skip',index_col=False, low_memory=False)
                content = data_file.read().decode('utf-8')
            
            # # Usar csv.reader para procesar el contenido
                data = csv.reader(io.StringIO(content), delimiter=',')
          

            return data
    except Exception as e:
        print(e)

def separate_incoming(data):
    file = data
    
    # Filtrar los datos directamente usando pandas
    inbound = file[(file['sell_zone'].str.upper().str.contains('INCOMING')) | 
                   (file['buy_zone'].str.upper().str.contains('INCOMING'))]
    
    outbound = file[~((file['sell_zone'].str.upper().str.contains('INCOMING')) | 
                      (file['buy_zone'].str.upper().str.contains('INCOMING')))]
    
    return [inbound, outbound]

def change_columns(data):
        columns_order =  file.iloc[0]
        columns_order = columns_order.values


        data.columns = columns_order 

        return data

def delete_headers(data):
    new_columns_order =  file.iloc[0]
    new_columns_order = new_columns_order.values

    default_order = get_default_columns()
    debug = debug_columns()
    for i in range(len(data)):
        if default_order[i].startswith('sell') or default_order[i].startswith('asig') or default_order[i].startswith('artp'):
 
            aux = data[default_order[i]]
            data[default_order[i]] = data[new_columns_order[i]]
            data[new_columns_order[i]] = aux
        if default_order[i] in debug:
            del data[default_order[i]]

    return data

def debug_columns():
        data =  file
        binary_columns = data.iloc[2]
        unnecessary_columns = []
        for index,item  in enumerate(binary_columns):
             if item != '1':
                  unnecessary_columns.append(data.iloc[0][index])
        return unnecessary_columns

def get_default_columns():
        data =  file

        default_columns = []
        for index,item  in enumerate(data.iloc[1]):
            default_columns.append(data.iloc[1][index])
        return default_columns
# name = build_approximate_filename(datetime.now())
# name = get_file_name(name)
# data = get_cdr_file(name)


