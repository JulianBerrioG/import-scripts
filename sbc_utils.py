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
# from utils import *
import gzip 
import zipfile 
import boto3
from dateutil.parser import *
import pytz
import csv


load_dotenv()

s3_client = boto3.client('s3')
uri= 'mongodb+srv://julian-berrio:jkXfcfEAld74GzJJ@euscallstor.41mox.mongodb.net/'
bucket_name = os.getenv('BUCKET_NAME')


def build_name_day(date):
    # today = datetime.now(timezone.utc)- timedelta(hours=2)
    today = date
    hour = today.strftime("%H") 
    today = today.strftime('%y.%m.%d') 
    last_file= f'SDR__{today}'
    return last_file


def build_approximate_filename(date):
    today = date
    hour = today.strftime("%H") 
    today = today.strftime('%y.%m.%d') 
    last_file= f'SDR__{today}-{hour}'
    print (last_file)
    return last_file
    
def log_incomplete_calls(name):
    client = MongoClient(uri)
    db = client.db_infinivirt_staging
    failed_collection = db.failed
    failed_collection.insert_one({"name": name})

def get_file_name(approximate_filename):
    global bucket_name
    try:
        response = s3_client.list_objects(
            Bucket=bucket_name,
            Delimiter=',',
            EncodingType='url',
            Marker='string',
            Prefix=rf'xDR/EUSCE1/2024/{approximate_filename}',
            RequestPayer='requester',
            OptionalObjectAttributes=[
                'RestoreStatus',
            ]
        )
        # print(response)
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
    except Exception as e:
        print(e)

def change_values(df):
    df['Setup Time'] = df['Setup Time'].apply(lambda x: parse(x).strftime('%Y-%m-%d %H:%M:%S'))
    df['Connect Time'] = df['Connect Time'].apply(lambda x: parse(x).strftime('%Y-%m-%d %H:%M:%S'))
    # formatted_setup = pd.to_datetime(df["Setup Time"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
    # formatted_connect = pd.to_datetime(df["Connect Time"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

    # df['Setup Time'] = formatted_setup
    # df['Connect Time'] = formatted_connect

    

def get_cdr_file(name):
    global bucket_name
    header = ['Setup Time', 'Connect Time', 'Node Time Zone', 'Call Duration(centisegundos)', 'Ingress Calling User(From Customer)', 'Ingress Dialed User(TO Customer)', 'Egress Calling User(From SBC)', 'Egress Called User(To SBC)', 'Ingress Call Source IP(IP Origen)', 'Ingress Calling Host(IP SBC)', 'Egress Call Destination IP(IP Destino)', 'Egress SIP Termination Reason', 'Egress Termination Reason', 'Ingress IP Group Name(IP Group Origen)', 'Egress IP Group Name(Ipg Destino)', 'Ingress Var Call User Defined 2(Cliente)', 'Session ID', 'Ingress Call ID', 'Egress Call ID', 'SIP Interface Origen', 'SIP Interface Destino']

    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=name
        )
        # print(response['Body'])
        # byteObj = io.BytesIO(response['Body'].read())
        # print(byteObj)
        # with  zipfile (fileobj=BytesIO(data)) as gz_file:
        with gzip.GzipFile(fileobj=io.BytesIO(response['Body'].read())) as zip_ref:

            data = pd.read_csv(zip_ref,on_bad_lines='skip',index_col=False, low_memory=False,header=None)

            data.columns = header
            change_values(data)

            return data
    except Exception as e:
        print(e)

def get_cdr_file_errors(name):
    global bucket_name
    header = ['Setup Time', 'Connect Time', 'Node Time Zone', 'Call Duration(centisegundos)', 'Ingress Calling User(From Customer)', 'Ingress Dialed User(TO Customer)', 'Egress Calling User(From SBC)', 'Egress Called User(To SBC)', 'Ingress Call Source IP(IP Origen)', 'Ingress Calling Host(IP SBC)', 'Egress Call Destination IP(IP Destino)', 'Egress SIP Termination Reason', 'Egress Termination Reason', 'Ingress IP Group Name(IP Group Origen)', 'Egress IP Group Name(Ipg Destino)', 'Ingress Var Call User Defined 2(Cliente)', 'Session ID', 'Ingress Call ID', 'Egress Call ID', 'SIP Interface Origen', 'SIP Interface Destino']

    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=name
        )
        # print(response['Body'])
        # byteObj = io.BytesIO(response['Body'].read())
        # print(byteObj)
        # with  zipfile (fileobj=BytesIO(data)) as gz_file:
        with gzip.GzipFile(fileobj=io.BytesIO(response['Body'].read())) as gz_file:

            # data = pd.read_csv(zip_ref,on_bad_lines='skip',index_col=False, low_memory=False)
            content = gz_file.read().decode('utf-8')
            
            # Usar csv.reader para procesar el contenido
            reader = csv.reader(io.StringIO(content), delimiter=',')
            

            return reader
    except Exception as e:
        print(e)

def get_cdr_file_csv(name):
    global bucket_name
    header = ['Setup Time', 'Connect Time', 'Node Time Zone', 'Call Duration(centisegundos)', 'Ingress Calling User(From Customer)', 'Ingress Dialed User(TO Customer)', 'Egress Calling User(From SBC)', 'Egress Called User(To SBC)', 'Ingress Call Source IP(IP Origen)', 'Ingress Calling Host(IP SBC)', 'Egress Call Destination IP(IP Destino)', 'Egress SIP Termination Reason', 'Egress Termination Reason', 'Ingress IP Group Name(IP Group Origen)', 'Egress IP Group Name(Ipg Destino)', 'Ingress Var Call User Defined 2(Cliente)', 'Session ID', 'Ingress Call ID', 'Egress Call ID', 'SIP Interface Origen', 'SIP Interface Destino']

    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=name
        )
        # print(response['Body'])
        # byteObj = io.BytesIO(response['Body'].read())
        # print(byteObj)
        # with  zipfile (fileobj=BytesIO(data)) as gz_file:
        with gzip.GzipFile(fileobj=io.BytesIO(response['Body'].read())) as gz_file:

            # data = pd.read_csv(zip_ref,on_bad_lines='skip',index_col=False, low_memory=False)
            content = gz_file.read().decode('utf-8')
            
            # Usar csv.reader para procesar el contenido
            data = csv.reader(io.StringIO(content), delimiter=',')


            return data
    except Exception as e:
        print(e)