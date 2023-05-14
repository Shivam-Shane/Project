from flask import Flask,request,render_template
import pandas as pd
from Source.logger import logging
from Pipelines.Predict_Pipeline import PredictPipelineClass
from Pipelines.Predict_Pipeline import CustomDataClass
import warnings
warnings.filterwarnings('ignore')

logging.info("Starting application")
application=Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/predict_data',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomDataClass(
                Date_Received=pd.to_datetime(request.form.get('Date_Received')),
                Product_Name=request.form.get('Product_Name'),
                Issue_Detail=request.form.get('Issue_Detail'),
                Submitted_Via=request.form.get('Submitted_Via'),
                Date_sent_to_company=pd.to_datetime(request.form.get('Date_sent_to_company')),
                Company_Responce=request.form.get('Company_Responce'),
                Timely_Responce=request.form.get('Timely_Responce') )
        
        logging.info("Starting prediction on data{}".format(data))

        Prediction_dataframe=data.get_data_as_dataframe()

        Predict_pipeline_object=PredictPipelineClass()
        
        result=Predict_pipeline_object.predict_dataset(Prediction_dataframe)
        logging.info("Rendering the result to webpage")
        return render_template('home.html',result=result)

if __name__=="__main__":
        application.run(host="0.0.0.0",port=8080)
    
