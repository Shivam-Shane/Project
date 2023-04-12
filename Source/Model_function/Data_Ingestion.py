import os,sys
from Source.exception import CustomException
from Source.logger import logging
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from Data_transformation import data_transform

@dataclass
class DataIngestionCreation:
    train_data_path:str=os.path.join('Assets',"train.csv")## train data
    test_data_path:str=os.path.join('Assets',"test.csv")## test data
    raw_data_path:str=os.path.join('Assets',"raw.csv")## unseen data
# This class helps in initializing instances of the DataIngestionCreation class

class  DataIngestion:
    def __init__(self):
        # Creating an instance of the DataIngestionCreation class and assigning it to a property
        self.DataIngestion=DataIngestionCreation()
        
    def DataIngestion_initiated(self):
        # Method to indicate that data ingestion has been initiated

        logging.info("Data Ingestion started")    
        try:
            dataset=pd.read_csv('D:\Shane\study material\CSV\Consumer_Complaints_train1.csv')
            os.makedirs(os.path.dirname(self.DataIngestion.raw_data_path),exist_ok=True)
            dataset.to_csv(self.DataIngestion.raw_data_path,index=False,header=True)
            logging.info("Data stored successfully at location {}".format(os.path.join(os.getcwd(),self.DataIngestion.raw_data_path)))
        except Exception as e:
            logging.info(str(e))
            raise CustomException(str(e),sys.exc_info())
        try:
            logging.info("Train and test data Split initiated")
            try:
                # Split dataset into train and test data
                train_data,test_data=train_test_split(dataset,random_state=40,test_size=0.2)
                # Create directory if not exists
                logging.info("Creating directory")
                os.makedirs(os.path.dirname(self.DataIngestion.train_data_path),exist_ok=True)
                os.makedirs(os.path.dirname(self.DataIngestion.test_data_path),exist_ok=True)
                logging.info("Created directory successfully")
                # Store train and test data in given paths
                logging.info("Store Train and test data into given path")
                train_data.to_csv(self.DataIngestion.train_data_path,index=False,header=True)
                test_data.to_csv(self.DataIngestion.test_data_path,index=False,header=True)
                logging.info("Train and test data stored succesfully")
            except Exception as e:
                    logging.info(str(e))
                    raise CustomException(str(e),sys.exc_info())  

            return(
                self.DataIngestion.train_data_path,
                self.DataIngestion.test_data_path  
            )        
            logging.info("Data ingestion successfuly completed")            
        except Exception as e:
                logging.info(e)
                raise CustomException(str(e),sys.exc_info())
            

if __name__=="__main__":
    obj=DataIngestion()
    train_path,test_path=obj.DataIngestion_initiated()

    data_transformation=data_transform()
    
    data_transformation.initiate_data_transformation(train_path,test_path)

    