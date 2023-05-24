import sys
from Source.exception import CustomExceptionClass
from Source.logger import logging
from Source.Model_function import Data_Ingestion,Data_transformation
from Source.Model_function import Data_model

class TrainingPipelineClass:
    try:
        def trainingpipeline(self):
            logging.info("Training pipeline started")
            obj=Data_Ingestion.DataIngestionClass()
            data_path=obj.data_ingestion_initiated()

            data_transformation_obj=Data_transformation.DataTransformClass()
            
            data_attr,data_target_attr=data_transformation_obj.initiate_data_transformation(data_path)

            data_modeleling=Data_model.DataModelClass()

            data_modeleling.initiate_data_model(data_attr,data_target_attr)

    except Exception as e:
        logging.error(str(e))
        raise CustomExceptionClass(str(e),sys.exc_info())  
    
if __name__=="__main__":
        obj=TrainingPipelineClass()
        obj.trainingpipeline()