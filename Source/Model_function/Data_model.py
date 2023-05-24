from Source.logger import logging
from Source.exception import CustomExceptionClass
from Source.utils import save_objects_file
from dataclasses import dataclass
import os
import sys
from sklearn.tree import DecisionTreeClassifier

@dataclass
class DataModelConfig:
    model_trained_file=os.path.join('Assets',"Model_Trained.pkl")# directory for saving model pickle file\

class DataModelClass:
    try:
        def initiate_data_model(self,data_array,data_traget_array):# data 
            logging.info("Data modeling initiated")

            model_DTC = DecisionTreeClassifier()
            model_DTC.fit(data_array, data_traget_array)## model fitting on data
            logging.info("Model {} successfully trained".format(model_DTC))
            
            save_objects_file(
                        file_path=DataModelConfig.model_trained_file,
                        object=model_DTC #model object
                             )
    except Exception as e:
        logging.error(str(e))
        raise CustomExceptionClass(e, sys.exc_info())      