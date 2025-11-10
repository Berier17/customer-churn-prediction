# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 11:36:55 2025

@author: aliel
"""

import pickle
from flask import Flask, request, jsonify



with open('model.bin', 'rb') as f_in:
    model = pickle.load(f_in)
    
with open('dv.bin', 'rb') as f_in:
    dv = pickle.load(f_in)
    
#Create Flask app
app = Flask('churn-service')

#Create the Predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    #get the JSON data the user sent us 
    customer = request.get_json()
    #Transform the customer data with loaded Vectorizer
    x = dv.transform([customer])
    #use loaded model to get the prediction probability 
    y_pred_proba = model.predict_proba(x)[0, 1]
    #create a JSON response
    response = {
        'churn_probability': float(y_pred_proba)
        }
    #Send the response to the user
    return jsonify(response)

#Run the app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
    





