# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:38:06 2025

@author: aliel
"""

import requests

url = "https://churn-service-app-300316357465.us-central1.run.app/predict"


customer = {
    'credit_score': 619,
    'geography': 'France',
    'gender': 'Female',
    'age': 42,
    'balance': 0.0,
    'num_of_products': 1,
    'is_active_member': 1,
    'estimated_salary': 101348.88
}

response = requests.post(url, json=customer)

print(response.json())




