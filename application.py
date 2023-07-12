from flask import Flask, request, render_template
import pandas as pd
from Source.logger import logging
from Pipelines.Predict_Pipeline import PredictPipelineClass
from Pipelines.Predict_Pipeline import CustomDataClass

# Logging a message to indicate the start of the application
logging.info("Starting application")

# Creating a Flask application instance
application = Flask(__name__)

# Route for the home page
@application.route('/')
def index():
    return render_template('index.html')

# Route for predicting data
@application.route('/predict_data', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # Extracting data from the request form
        data = CustomDataClass(
            Date_Received=pd.to_datetime(request.form.get('Date_Received')),
            Product_Name=request.form.get('Product_Name'),
            Issue_Detail=request.form.get('Issue_Detail'),
            Submitted_Via=request.form.get('Submitted_Via'),
            Date_sent_to_company=pd.to_datetime(request.form.get('Date_sent_to_company')),
            Company_Responce=request.form.get('Company_Responce'),
            Timely_Responce=request.form.get('Timely_Responce')
        )
        
        # Logging the data for prediction
        logging.info("Starting prediction on data {}".format(data))

        # Converting the data into a pandas DataFrame
        Prediction_dataframe = data.get_data_as_dataframe()

        # Creating an instance of the prediction pipeline class
        Predict_pipeline_object = PredictPipelineClass()
        
        # Performing the prediction on the dataset
        result = Predict_pipeline_object.predict_dataset(Prediction_dataframe)

        # Logging the result
        logging.info("Rendering the result to the webpage")

        # Rendering the result to the home page
        return render_template('home.html', result=result) # return value is specified in home.html page

if __name__ == "__main__":
    # Running the Flask application on local host and port 1000
    application.run(host="0.0.0.0", port=1000,debug=True)
