# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:38:06 2025

@author: aliel
"""

import requests

url = "https://churn-service-app-300316357465.us-central1.run.app/predict"


customer = {
    'gender': 'female',
    'seniorcitizen': 0,
    'partner': 'yes',
    'dependents': 'no',
    'tenure': 1,
    'phoneservice': 'no',
    'multiplelines': 'no_phone_service',
    'internetservice': 'dsl',
    'onlinesecurity': 'no',
    'onlinebackup': 'yes',
    'deviceprotection': 'no',
    'techsupport': 'no',
    'streamingtv': 'no',
    'streamingmovies': 'no',
    'contract': 'month-to-month',
    'paperlessbilling': 'yes',
    'paymentmethod': 'electronic_check',
    'monthlycharges': 29.85,
    'totalcharges': 29.85
    }


response = requests.post(url, json=customer)

print(response.json())




