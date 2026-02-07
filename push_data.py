import os 
import sys
import json

# Add the parent directory to sys.path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
print(MONGO_DB_URI)

import certifi
ce=certifi.where()
print(ce)


import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URI,tlsCAFile=certifi.where())
            self.db = self.client["Network_Security_Project"]
            self.collection = self.db["network_data"]
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def cv_to_json_converter(self, file_path:str)->list:
        try:
            df = pd.read_csv(file_path)
            json_data = json.loads(df.to_json(orient="records"))
            return json_data
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI,tlsCAFile=certifi.where())
            self.database = self.mongo_client[self.database]
            self.collection = self.db[self.collection]
            self.collection.insert_many(self.records)

            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
# ...existing code...
if __name__=="__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(BASE_DIR, "network_data", "phisingData.csv")
    DATABASE="BHARATH"
    COLLECTION="network_data"
    networkobj=NetworkDataExtract()
    networkobj.cv_to_json_converter(file_path=FILE_PATH)
    no_of_rrecords=networkobj.insert_data_to_mongodb(
        records=networkobj.cv_to_json_converter(file_path=FILE_PATH),
        database=DATABASE,
        collection=COLLECTION
    )
    print(f"Number of records inserted to MongoDB: {no_of_rrecords}")