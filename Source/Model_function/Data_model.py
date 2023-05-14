from Source.logger import logging
from Source.exception import CustomExceptionClass
from Source.utils import save_objects_file
from dataclasses import dataclass
import os,sys
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings('ignore')

@dataclass
class DataModelConfig:
    model_trained_file=os.path.join('Assets',"Model_Trained.pkl")

class DataModelClass:
    try:
        def initiate_data_model(self,train_array,train_traget_array,test_array,test_traget_array):
            logging.info("Data Modeling initiated")

            model_DTC = DecisionTreeClassifier()
            model_DTC.fit(train_array, train_traget_array)## model fitting on training data
            logging.info("Model {} succefully trainied".format(model_DTC))
            
            save_objects_file(
                        file_path=DataModelConfig.model_trained_file,
                        object=model_DTC
                             )
    except Exception as e:
        logging.error(str(e))
        raise CustomExceptionClass(e, sys.exc_info())      