import os
import sys
from Source.logger import logging
from Source.exception import CustomExceptionClass
from Source.utils import save_objects_file
from dataclasses import dataclass
import pandas as pd
import numpy as np
import time
import nltk,string
nltk.download('stopwords')
nltk.download('wordnet')
from nltk import WordNetLemmatizer,PorterStemmer,wordpunct_tokenize
from nltk.corpus import stopwords
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,MinMaxScaler,MaxAbsScaler,FunctionTransformer


class CustomFunctionsClass:

    def cat_function(cat_data):
        cat_data['Product']=np.where(cat_data['Product'].isin(['Money transfers','Payday loan','Other financial service','Prepaid card','Virtual currency']),'Other currency',cat_data['Product'])
        return cat_data
    
    def nlp_function(nlp_data):
        nlp_data = nlp_data['Issue'] 
        tokenized_data = nlp_data.apply(lambda x: wordpunct_tokenize(x.lower()))# tokenizing the data

        def remove_punctuation(text):
            return [w for w in text if w not in string.punctuation]
        no_punctuation_data = tokenized_data.apply( lambda x: remove_punctuation(x))# removing punctuations from tokenized data

        Stop_words = stopwords.words('english')
        Removed_Stopwords = [w for w in no_punctuation_data if not w in Stop_words]
        Removed_Stopwords = pd.Series(Removed_Stopwords)# removing stopwords

        def lemmatize_text(text):
            lem_text = [WordNetLemmatizer().lemmatize(w,pos = 'v') for w in text]
            return lem_text
        lemmatized_data = Removed_Stopwords.apply(lambda x:lemmatize_text(x)) #lemmatizing the data

        def stem_text(text):
            stem_text = [PorterStemmer().stem(w) for w in text]
            return stem_text
        stemmed_data = lemmatized_data.apply(lambda x:stem_text(x))# stemming the lemmatized data

        cleaned_data=[" ".join(x) for x in stemmed_data]
        logging.info("Text preprocessing succesfully done")
        logging.info("Returnnig preprocessed data")
        return cleaned_data
    
    def date_time_function(datetime_data):
        datetime_data['Date received']=pd.to_datetime(datetime_data['Date received'])
        datetime_data['Date sent to company']=pd.to_datetime(datetime_data['Date sent to company'])
        datetime_data['days_held']=(datetime_data['Date sent to company']-datetime_data['Date received']).dt.days
        return datetime_data['days_held'].values.reshape(-1,1)

@dataclass
class Data_transformation_config:
    data_transformation_file=os.path.join('Assets',"Data_Transformation.pkl")# path for stroing pickle file

class DataTransformClass:
    try:
        
        def get_data_transformation(self):
            start=time.time()
            logging.info("Data transformation started")
            
            Categorical_Column=['Product','Timely response?','Company response to consumer','Submitted via']
            NLP_Column=['Issue']
            Date_Time_Column=['Date sent to company','Date received']

            logging.info("Categorical pipeline initiated")
            Cat_pipeline=Pipeline( steps=[ #categorical pipeline
                                         ("Categorical_function",FunctionTransformer(CustomFunctionsClass.cat_function,validate=False))
                                        ,("Categorical_Imputer",SimpleImputer(strategy='most_frequent'))
                                        ,('Categorical_Onehot',OneHotEncoder(sparse=False,drop='first'))
                                        ,("Categorical_Scaler",MinMaxScaler())
                                        ]) 
            logging.info("Nlp pipeline initiated")
            Nlp_pipline=Pipeline( steps=[#NLP pipeline
                                        ("Nlp_extration",FunctionTransformer(CustomFunctionsClass.nlp_function,validate=False))
                                        ,("CountVector",CountVectorizer())
                                        ,("NLP_Scaler",MaxAbsScaler())
                                        ])
            logging.info("Date_time pipeline initiated")
            Date_time_pipeline=Pipeline(steps=[#Datetime pipeline
                                        ("Date_time_transformer",FunctionTransformer(CustomFunctionsClass.date_time_function,validate=False))
                                        ,("Date_time_Scaler",MinMaxScaler())
                                        ])

            logging.info("ColumnTransformer started running pipelines")    
            # Column Transformer for pipeline
            column_preprocessor=ColumnTransformer( 
                                        [
                                        ("Categorical_Transformer",Cat_pipeline,Categorical_Column)
                                        ,('NLP_Transformer',Nlp_pipline,NLP_Column)
                                        ,("Date_time_Transfomer",Date_time_pipeline,Date_Time_Column)
                                        ]
                                        ,remainder='passthrough')# untoched column that are not transformed   
            logging.info("ColumnTransformer initiated pipelines succesfully") 
            end=time.time()
            logging.info("Data transformation initited succesfully in: {:.2f} seconds".format(end - start))
            return column_preprocessor

    except Exception as e:
          logging.error(str(e))
          raise CustomExceptionClass(e,sys.exc_info()) 

    try:
        
        def initiate_data_transformation(self,data_path):
            start = time.time()

            logging.info("Data transformation initiated")
            data_dataframe=pd.read_csv(data_path)
            logging.info("Dataset successfully stored for transformatiom")

            Column_Preprocessor_Object=self.get_data_transformation()# calling transformer object
            
            Data_features=data_dataframe.drop(columns=['Consumer disputed?'],axis=1)
            Data_target_feature=data_dataframe['Consumer disputed?']

            logging.info("Dataset successfully coupled")

            Label_encoder_object = LabelEncoder()
            logging.info("Starting column transformation on the dataset")
            Data_features_attr=Column_Preprocessor_Object.fit_transform(Data_features)
            
            end = time.time()
           
            logging.info("Dataset transformation succesfully done transforming our dataset in: {:.2f} seconds".format(end - start))

            logging.info("Transforming our target data column")
            Data_target_attr = Label_encoder_object.fit_transform(Data_target_feature)
            logging.info("Target column transforming successfully done ")

            logging.info("Saving the object file")
            save_objects_file( # saving object and transformation file
                file_path=Data_transformation_config.data_transformation_file,
                object=Column_Preprocessor_Object
            )

            return(Data_features_attr,Data_target_attr) # returing independent and dependent feature

    except Exception as e:
          logging.error(str(e))
          raise CustomExceptionClass(e,sys.exc_info()) 