from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from datetime import datetime
from Source.logger import logging


logging.info("importing file")
from Pipelines.Predict_Pipeline import PredictPipeline
from Pipelines.Predict_Pipeline import CustomData


logging.info("Starting application")
application=Flask(__name__)

app=application

## route for home page
logging.info("Starting index html")
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict_data',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('Home.html')
    else:
        data=CustomData(
                Date_Received=pd.to_datetime(request.form.get('Date_Received')),
                Product_Name=request.form.get('Product_Name'),
                Issue_Detail=request.form.get('Issue_Detail'),
                Submitted_Via=request.form.get('Submitted_Via'),
                Date_sent_to_company=pd.to_datetime(request.form.get('Date_sent_to_company')),
                Company_Responce=request.form.get('Company_Responce'),
                Timely_Responce=request.form.get('Timely_Responce') )
        
        logging.info("Stating prediction on data{}".format(data))

        Prediction_dataframe=data.get_data_as_dataframe()

        Predict_pipeline_object=PredictPipeline()

        
        result=Predict_pipeline_object.predict_dataset(Prediction_dataframe)
        logging.info("rendering the result to webpage")
        return render_template('home.html',result=result[0])
logging.info("Its done")

if __name__=="__main__":
        app.run(host="0.0.0.0",debug=True)
    
