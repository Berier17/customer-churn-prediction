# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 11:08:44 2025

@author: aliel
"""

#Impoerting Modules
import pandas as pd 
import numpy as np
import pickle 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

#Parameters
C = 0.1
test_size = 0.2
output_file = 'model.bin'
dv_file = 'dv.bin'


#Data loading
df = pd.read_csv("D:/Telco-Customer-Churn.csv")

#Data Preparation
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(0)

df['Churn'] = df['Churn'].replace({'Yes': 1, 'No': 0})

df = df.drop('customerID', axis=1)

#Model Training
df_full_train, df_test = train_test_split(df, test_size=test_size, random_state=42)
y_train = df_full_train['Churn'].values
y_test = df_test['Churn'].values 


#Fit the DictVectorizer
dv = DictVectorizer(sparse=False)
train_dict = df_full_train.to_dict(orient='records')
x_train = dv.fit_transform(train_dict)

#Train the Model
model = LogisticRegression(C=C, solver='liblinear', random_state=42)
model.fit(x_train, y_train)

#Saving the Model and Vectorizer
with open(dv_file, 'wb') as f_out:
    pickle.dump(dv, f_out)
    
with open(output_file, 'wb') as f_out:
    pickle.dump(model, f_out)

     


























