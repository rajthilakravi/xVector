from multiprocessing import connection
import psycopg2
import json
import os
import pandas as pd
from flask import Response,request
from sqlalchemy import create_engine

def add_data(data_name,data_path):
    try:
        PG_USER = os.getenv('PG_CUST_USER') 
        PG_PWD = os.getenv('PG_CUST_PASS')  
        PG_HOST = os.getenv('PG_CUST_IP') 
        PG_PORT = os.getenv('PG_PORT') 
        PG_DATABASE = os.getenv('PG_DB')
        
        df = pd.read_csv(data_path+"/"+data_name+".csv")
        engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(PG_USER,PG_PWD,PG_HOST,PG_PORT,PG_DATABASE))
        df.to_sql(data_name,con=engine, if_exists= 'fail', index=False )
        
        print("table created")

        return "success"
    except Exception as e:
        return str(e)

def list_data():
    try:
        PG_USER = os.getenv('PG_CUST_USER') 
        PG_PWD = os.getenv('PG_CUST_PASS')  
        PG_HOST = os.getenv('PG_CUST_IP') 
        PG_PORT = os.getenv('PG_PORT') 
        PG_DATABASE = os.getenv('PG_DB')
        
        connection = psycopg2.connect(user= PG_USER ,password= PG_PWD , host= PG_HOST ,port= PG_PORT ,database= PG_DATABASE )
        cursor = connection.cursor()

        list_q = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
        # final_query = "select json_agg(row) from ("+list_q+") row"
        # cursor.execute(final_query)
        # res = cursor.fetchall()[0][0]
        cursor.execute(list_q)
        res = cursor.fetchall()
        res = [val[0] for val in res]
        print(res)
        return res, "success"
    except Exception as e:  
        return str(e)

def data_compute(data_name,column_name,operation):
    try:
        PG_USER = os.getenv('PG_CUST_USER') 
        PG_PWD = os.getenv('PG_CUST_PASS')  
        PG_HOST = os.getenv('PG_CUST_IP') 
        PG_PORT = os.getenv('PG_PORT') 
        PG_DATABASE = os.getenv('PG_DB')
        
        connection = psycopg2.connect(user= PG_USER ,password= PG_PWD , host= PG_HOST ,port= PG_PORT ,database= PG_DATABASE )
        cursor = connection.cursor()

        opr_q = '''SELECT {}("{}") FROM {}'''.format(operation.upper(),column_name,data_name)
        cursor.execute(opr_q)
        res = cursor.fetchall()[0][0]
        print(res)
        return res,"success"

    except Exception as e:
        return str(e)

def data_plot(data_name,column_one,column_two):
    try:
        PG_USER = os.getenv('PG_CUST_USER') 
        PG_PWD = os.getenv('PG_CUST_PASS')  
        PG_HOST = os.getenv('PG_CUST_IP') 
        PG_PORT = os.getenv('PG_PORT') 
        PG_DATABASE = os.getenv('PG_DB')
        
        connection = psycopg2.connect(user= PG_USER ,password= PG_PWD , host= PG_HOST ,port= PG_PORT ,database= PG_DATABASE )
        cursor = connection.cursor()

        opr_q = '''SELECT "{}","{}" FROM {} limit 30'''.format(column_one,column_two,data_name)
        final_query = "select json_agg(row) from ("+opr_q+") row"
        cursor.execute(final_query)
        res = cursor.fetchall()[0][0]
        print(res)
        return res,"success"

    except Exception as e:
        return str(e)

def list_columns(data_name):
    return "success"