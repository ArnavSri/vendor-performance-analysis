import pandas as pd 
import os
import time
from sqlalchemy import create_engine
import logging
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine=create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    '''This functio will ingest the dataframe into table'''
    df.to_sql(
        table_name,
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=1000
    )

def load_raw_data():
    ''' this function will load the csv into dataframes and ingest into db'''
    start=time.time()
    for file in os.listdir('Data'):
         if '.csv' in file:
             df=pd.read_csv('Data/'+file)
             logging.info(f'Ingesting {file} in db')
             ingest_db(df, file[:-4], engine)
    end=time.time()
    total_time = (end - start)/60
    logging.info('-------------------Ingestion Completed-------------------------') 
    logging.info('\nTotal time Taken:{total_time} minutes')

if __name__ == '__main__':
    load_raw_data()