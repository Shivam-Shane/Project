from Source.logger import logging
from Source.exception import CustomExceptionClass
from Source.utils import save_objects_file
from dataclasses import dataclass

import os,sys
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

import time
import warnings
warnings.filterwarnings('ignore')


@dataclass
class DataModelConfig:
    model_trained_file=os.path.join('Assets',"Model_Trained.pkl")

class DataModelClass:
    try:
        def initiate_data_model(self,train_array,train_traget_array,test_array,test_traget_array):
            logging.info("Data Modeling initiated")
            

            print(train_array.shape,type(train_array),train_traget_array.shape,type(train_traget_array))
            logging.info("Model Training data seprated")

            model_DTC = DecisionTreeClassifier()
            model_DTC.fit(train_array, train_traget_array)## model fitting on training data

            save_objects_file(
                        file_path=DataModelConfig.model_trained_file,
                        object=model_DTC

            )
            

            
    except Exception as e:
        logging.error(str(e))
        raise CustomExceptionClass(e, sys.exc_info())      