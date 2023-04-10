from Source.logger import logging
from Source.exception import CustomException
import os, sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
import nltk,string
nltk.download('stopwords')
nltk.download('wordnet')

from nltk import wordpunct_tokenize,WordNetLemmatizer,PorterStemmer
from nltk.corpus import stopwords

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler,FunctionTransformer

def issue_column(column):
        relevant_text_train = column
        tokenized_data_train = relevant_text_train.apply(lambda x: wordpunct_tokenize(x.lower()))
        def remove_punctuation(text):
            no_punctuation = []
            for w in text:
                if w not in string.punctuation:
                    no_punctuation.append(w)
            return no_punctuation
        no_punctuation_data_train = tokenized_data_train.apply(lambda x: remove_punctuation(x))

        stop_words = stopwords.words('english')
        filtered_sentence_train = [w for w in no_punctuation_data_train if not w in stop_words]
        filtered_sentence_train = pd.Series(filtered_sentence_train)

        def lemmatize_text(text):
            lem_text = [WordNetLemmatizer().lemmatize(w,pos = 'v') for w in text]
            return lem_text
        lemmatized_data_train = filtered_sentence_train.apply(lambda x:lemmatize_text(x))
        def stem_text(text):
            stem_text = [PorterStemmer().stem(w) for w in text]
            return stem_text
        stemmed_data_train = lemmatized_data_train.apply(lambda x:stem_text(x))
        def word_to_sentence(text):
            text_sentence = " ".join(text)
            return text_sentence
        clean_data_train = stemmed_data_train.apply(lambda x:word_to_sentence(x))

@dataclass
class data_transofrmation_config:
    pass

class data_transform:

    def get_data_transformation(self):
        numerical_column=[]
        categorical_Column=['Product','Timely response?','Company response to consumer','Submitted via']
        date_time_column=['Date received','Date sent to company']
        data_NLP_transfor=['Issue']
        
        num_pipeline=Pipeline(
                steps=[
                        ("inputer",SimpleImputer(strategy='most_frequent'))
                        ("Scaler",StandardScaler())
                      ]
                )
        
        cat_pipeline=Pipeline(
            steps=[
            ("imputer",SimpleImputer(strategy='median'))
            ('onehot',OneHotEncoder())
            ("scler",StandardScaler())
            ]
        )
        preprocessor=ColumnTransformer(
            [
            ("Num_Transformer",num_pipeline,numerical_column)
            ("col_Num_Transformer",cat_pipeline,categorical_Column)
            ("NLP_transformer",FunctionTransformer(issue_column),data_NLP_transfor)
            ]
        )
        return preprocessor
    
    def initiate_data_transformation(self,train_path,test_path):
        train_dataframe=pd.read_csv(train_path)
        test_dataframe=pd.read_csv(test_path)

        preprocessor_object=self.get_data_transformation()
        target_column='Consumer disputed?'
        pass