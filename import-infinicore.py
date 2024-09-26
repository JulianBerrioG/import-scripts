import os 
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from operator import itemgetter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import threading
import requests
from zipfile import ZipFile 
from ftplib import FTP
import pytz
from dotenv import load_dotenv
from utils import *
import platform
from mail import *

system = platform.system()
uri= 'mongodb+srv://julian-berrio:jkXfcfEAld74GzJJ@euscallstor.41mox.mongodb.net/'


today = datetime.now(pytz.utc)
load_dotenv()

base_route = formatted_route(os.getenv('BASE_ROUTE_INFINICORE_L'))
base_route_zip = formatted_route(os.getenv('BASE_ROUTE_INFINICORE_L_ZIP'))
uri= 'mongodb+srv://julian-berrio:jkXfcfEAld74GzJJ@euscallstor.41mox.mongodb.net/'

def ftp_connection():
    ftp = FTP(host='10.10.101.6')
    return ftp
def download_file_ftp(zip):
    try:
        ftp = ftp_connection()
        ftp.login( user='dev_staging_ftp', passwd='uo6*.Kt%8jLu4')
        ftp.retrlines('LIST')
        print(zip)
        with open(rf'{base_route}{zip}', 'wb') as archivo_local:
            ftp.retrbinary('RETR ' + zip, archivo_local.write)


        # with open(f'C:\\Users\\julian.berrio\\Documents\\xDR\\Infinicore\\{file_name}', 'wb') as file:
        #     ftp.retrbinary('RETR ' + file_name, file.write)
        ftp.quit()
    except Exception as e:
        sendMail(e) 
        print(e)
        return e
def build_name(date):
    date = date.strftime('%Y-%m-%d')   
    last_file= 'xDR_Infinivirt_' + date + '.zip' 
    return last_file

def download_file(file_name):
    try:
        get_file_from_s3 = rf'aws s3 cp s3://sftpgw-i-0d3f2dcfa9a89ebd4/xDR/Infinicore/2024/{file_name} {base_route}{file_name}'
        os.system(get_file_from_s3)
    except Exception as e:
        sendMail(e) 
        print(e)
        return e

def unzip_xDR(file_name):
    try:
        print(rf'{base_route}{file_name}')
        with ZipFile(rf'{base_route}{file_name}', 'r') as zObject:
            zObject.extractall(base_route)
    except Exception as e: 
        return e
    
def clean(names):
    try:
        for name in names:
            if system == 'Windows':
                os.system(rf'del {base_route_zip}{name}')
            else:
                os.system(rf'rm {base_route_zip}{name}')
    except Exception as e:
        sendMail(e) 
        return e

def import_data(file_name):
    #os.chdir(rf'C:\Program Files\MongoDB\Tools\100\bin')
    mongoimport_command = rf' mongoimport --uri "mongodb+srv://euscallstor.41mox.mongodb.net/" --password "GtqUdrSPotN0ieaC" ' \
        rf' --username "admin-infinivirt" --db "db_infinivirt" --collection "cdr_infinicore_2024"' \
        rf' --type csv --headerline --file "{base_route_zip}{file_name}"'
    os.system(mongoimport_command)



def start(today):

        try: 
            zipname = build_name(today)
            print(zipname)
            name = os.path.splitext(zipname)[0]
            #download_file_ftp(zip)
            download_file(zipname)
            unzip_xDR(zipname)
            import_data(rf'{name}.csv')
            clean([rf'{name}.zip', rf'{name}.csv'])
        except Exception as e:
            print(e)
            sendMail(e)
            return e


start(today)
# def build_approximate_filename(today):


# def log_incomplete_calls(name):
#     client = MongoClient(uri)
#     db = client.db_infinivirt_staging
#     failed_collection = db.failed
#     failed_collection.insert_one({"name": name})

# def get_file_name(bucket_name, approximate_filename):
#     try:
#         script = rf'aws s3api list-objects --bucket {bucket_name} --prefix "xDR/Digitalk/{approximate_filename}" --delimiter "/" --query "Contents" --output json'
#         resultado = os.popen(script).read()
#         datos_json = json.loads(resultado)
#         if(datos_json):
#             return rf"{datos_json[0]['Key']}"
#         else:
#             log_incomplete_calls(approximate_filename)
#             body ={"file_name": approximate_filename}
#             requests.post('http://localhost:8081/api/mail-service/mongoErrorLog', body)
#         return None
#     except ConnectionError as e:
#         print('Error de conexión:', e)
#         return e
#     except Exception as e:
#         print('Error inesperado:', e)
#         return e




# # resultado = subprocess.run(script, capture_output=True, text=True)





# def import_data(file_route):
#     os.chdir(rf'C:\Program Files\MongoDB\Tools\100\bin')
#     mongoimport_command = rf' mongoimport --uri "mongodb+srv://euscallstor.41mox.mongodb.net/" --password "GtqUdrSPotN0ieaC" --username "admin-infinivirt" --db "db_infinivirt_staging" --collection "s3_test" --type csv --headerline --file "C:\Users\julian.berrio\Documents\{file_route}"'
#     os.system(mongoimport_command)
#     os.system(rf'del C:\Users\julian.berrio\Documents\{file_route}')


# def run_script(today , fin):
#     while(today < fin):
#         try:
#             file_route = get_file_name('sftpgw-i-0d3f2dcfa9a89ebd4' ,build_approximate_filename(today))
#             if (file_route):
#                 csv_name = os.path.basename(file_route)
#                 dirname = os.path.dirname(file_route)
#                 download_file(file_route)
#                 import_data(file_route)
#         except Exception as e:
#             print(e)
#             continue
#         finally:
#             today +=  timedelta(minutes=5)
        
# t1 = threading.Thread(target=run_script, args=(today, fin))
# t2 = threading.Thread(target=run_script, args=(today2, fin2))
        

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# last_file_from_bucket('sftpgw-i-0d3f2dcfa9a89ebd4', 'CDR_04022024-1945')
# print (build_approximate_filename())