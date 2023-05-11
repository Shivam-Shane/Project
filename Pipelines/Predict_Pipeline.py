import os
import sys


import pandas as pd

from Source.exception import CustomExceptionClass
from Source.logger import logging
from Source.utils import load_obj_file


class PredictPipelineClass:
    def __init__(self):
        pass

    def predict_dataset(self,feature):

        try:
            logging.info("Starting prediction on data{}".format(feature))

            model_path=os.path.join('Assets',"Model_Trained.pkl")
            logging.info("Storing the model path for importing pickle file{}".format(model_path))

            preprocessor_path = os.path.join('Assets',"Data_Transformation.pkl")
            logging.info("Storing the preprocessor path for importing pickle file{}".format(preprocessor_path))

            logging.info("Stating loading preprocessor pickel file")
            data_transformtion=load_obj_file(file_path=preprocessor_path)
            logging.info("Loading Transformation file succeesfully done")

            logging.info("Stating loading model pickel file")
            model=load_obj_file(file_path=model_path)
            logging.info("Loading model pickel file succeesfuly done")
            print(feature,feature.shape,type(feature))
            data_scaled = data_transformtion.transform(feature)
            print(data_scaled.shape)
            logging.info("Starting prediction on dataset")
            result=model.predict(data_scaled)
            logging.info("Succeefully predicted{}".format(result*100))

        except Exception as e:
                logging.error(str(e))
                result=None
                raise CustomExceptionClass(str(e),sys.exc_info())
        logging.info("Returing result")
        if result==0:
            return 'Consumer not disputed'
        else:
            return 'Consumer disputed'
        
          


class CustomDataClass:
    def __init__(self,Date_Received,Product_Name,Issue_Detail,Submitted_Via, Date_sent_to_company,Company_Responce,Timely_Responce):
        self.Date_Received=Date_Received
        self.Product_Name=Product_Name
        self.Issue_Detail=Issue_Detail
        self.Submitted_Via=Submitted_Via
        self.Date_sent_to_company=Date_sent_to_company
        self.Company_Responce=Company_Responce
        self.Timely_Responce=Timely_Responce
    def get_data_as_dataframe(self):
        try:
            logging.info("Get data as Dataframe started")
            custom_data_input={
               "Date received":[self.Date_Received],
               "Product":[self.Product_Name],
               "Issue":[self.Issue_Detail],
               "Submitted via":[self.Submitted_Via],
               "Date sent to company":[self.Date_sent_to_company],
               "Company response to consumer":[self.Company_Responce],
               "Timely response?":[self.Timely_Responce]}
            
        except Exception as e:
            logging.error(str(e))
            raise CustomExceptionClass(str(e),sys.exc_info())  
        logging.info("Done creating Data from dataframe") 
        dataframe_data= pd.DataFrame(custom_data_input)
        dataframe_data.to_csv("D:\Shane\Projects\erow.csv")
        return dataframe_data

        