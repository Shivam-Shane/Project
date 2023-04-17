from Source.logger import logging
from Source.exception import CustomException
from dataclasses import dataclass
import os,sys
import pandas as pd
import numpy as np

import time
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Data_Model_config:
    pass

class Data_Model:
    try:
        def Initiate_Data_Model(self,train,test):
            logging.info("Data Modeling initiated")
            data_train=train
            data_test=test
            print(data_train)
    except Exception as e:
        raise CustomException(e,sys.exc_info())     