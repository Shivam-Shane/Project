import os
import sys
from Source.exception import CustomExceptionClass# Exception class
from Source.logger import logging# logging module
from dataclasses import dataclass
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

@dataclass
class DataIngestionCreationClass:
    data_path:str=os.path.join('Assets',"data.csv")## data
# This class helps in initializing instances of the DataIngestionCreation class

class DataIngestionClass:
    def __init__(self):
        # Creating an instance of the DataIngestionCreation class and assigning it to a property
        self.data_ingestion=DataIngestionCreationClass()
        
    def data_ingestion_initiated(self):
        # Method to indicate that data ingestion has been initiated

        logging.info("Data Ingestion started")    
        try:
            dataset=pd.read_csv('D:\Shane\Projects\Dataset\Consumer_Complaints_train.csv')
            ## reading data from source: database, dataware house, aws etc
            os.makedirs(os.path.dirname(self.data_ingestion.data_path),exist_ok=True)# making directory if not exist
            dataset.to_csv(self.data_ingestion.data_path,index=False,header=True)# saving data to csv
            logging.info("Data stored successfully at location {}".format(os.path.join(os.getcwd(),self.data_ingestion.data_path)))
            
        except Exception as e:
            logging.error(str(e))
            raise CustomExceptionClass(str(e),sys.exc_info())  
        logging.info("Data Ingestion successfuly completed") 

        return(
            self.data_ingestion.data_path 
        )            