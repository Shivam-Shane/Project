from Source.logger import logging
from Source.exception import CustomException
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
class Data_Model_config:
    model_trained_file=os.path.join('Assets',"Model_Trained.pkl")

class Data_Model:
    try:
        def Initiate_Data_Model(self,train_array,test_array):
            logging.info("Data Modeling initiated")
            
            # x_train,y_train,x_test,y_test=(train_array[:,:-1].toarray(),train_array[:,-1].toarray(),test_array[:,:-1].toarray(),test_array[:,-1].toarray())
            # x_train,y_train,x_test,y_test=(train_array.todense()[:,:-1],train_array.todense()[:,-1],test_array.todense()[:,:-1],test_array.todense()[:,-1])
            x_train = np.asarray(train_array.todense()[:,:-1])
            y_train = np.asarray(train_array.todense()[:,-1])
            x_test = np.asarray(test_array.todense()[:,:-1])
            y_test = np.asarray(test_array.todense()[:,-1])


            logging.info("Model Training data seprated")

            model_DTC = DecisionTreeClassifier()
            model_DTC.fit(x_train, y_train)## model fitting on training data

            y_pred = model_DTC.predict(x_test)### prediction on validation set Validation set

            val_accuracy = accuracy_score(y_test, y_pred)## accuracy score on validation set
            save_objects_file(
                        file_path=Data_Model_config.model_trained_file,
                        object=model_DTC

            )
            return val_accuracy

            
    except Exception as e:
        raise CustomException(e,sys.exc_info())     