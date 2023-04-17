import os
import sys
import dill
from Source.exception import CustomException
from Source.logger import logging

def save_objects_file(file_path, object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        logging.info("Object directory initiated")
        with open(file_path, "wb") as file:
            logging.info("File opened")
            dill.dump(object, file)
    except Exception as e:
        logging.info(CustomException(e, sys.exc_info()))
        raise CustomException(e, sys.exc_info())
