import os
import sys
import pandas as pd
from Source.exception import CustomExceptionClass
from Source.logger import logging
from Source.utils import load_obj_file
import warnings
warnings.filterwarnings('ignore')

class PredictPipelineClass:
    def __init__(self):
        pass
    def predict_dataset(self,feature):
        try:
            logging.info("Starting prediction on data{}".format(feature))

            preprocessor_path = os.path.join('Assets',"Data_Transformation.pkl")# get the path of the data transformation object
            model_path        = os.path.join('Assets',"Model_Trained.pkl")# get the path of the pre-trained model
                      
            logging.info("Starting loading transformation pickel file")
            data_transformtion=load_obj_file(file_path=preprocessor_path)
            logging.info("Transformation file succeesfully fetched")

            logging.info("Starting loading model pickel file")
            model=load_obj_file(file_path=model_path)# load the pre-trained model
            logging.info("Model pickel file succeesfully fetched")
            
            logging.info("Starting transformation on dataset")
            data_scaled = data_transformtion.transform(feature)
            
            logging.info("Starting prediction on dataset")
            result=model.predict(data_scaled)# predict the consumer dispute status using the pre-trained model
            logging.info("Succeefully predicted{}".format(result*100))

        except Exception as e:
                logging.error(str(e))
                result=None
                raise CustomExceptionClass(str(e),sys.exc_info())
        logging.info("Returing result {}".format(result))
        if result==0:
            return 'Consumer not disputed'# return the prediction as a string
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
                                "Timely response?":[self.Timely_Responce]
                               }        

            dataframe_data= pd.DataFrame(custom_data_input)# create a dataframe from the dictionary
            
            directory_path = os.path.join(os.getcwd(), "user_data")
            os.makedirs(directory_path, exist_ok=True)

            # Define the file path
            file_path = os.path.join(directory_path, "user_data.csv")
            with open(file_path, mode='a', newline='') as file:
                dataframe_data.to_csv(file,header=False, index=False)

        except Exception as e:
            logging.error(str(e))
            raise CustomExceptionClass(str(e),sys.exc_info())  
        logging.info("Done creating Data from dataframe") 
        return dataframe_data

        