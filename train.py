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
from sklearn.ensemble import RandomForestClassifier

#Parameters
N_ESTIMATORS = 200
MAX_DEPTH = 10
MIN_SAMPLES_LEAF = 5
test_size = 0.2
output_file = 'model.bin'
dv_file = 'dv.bin'


#Data loading
df = pd.read_csv("Churn_Modelling.csv")

#Data Preparation
df.columns = df.columns.str.lower()
df = df.rename(columns={
    'rownumber': 'row_number',
    'customerid': 'customer_id',
    'creditscore': 'credit_score',
    'estimatedsalary': 'estimated_salary',
    'numofproducts': 'num_of_products',
    'hascrcard': 'has_cr_card',
    'isactivemember': 'is_active_member'
})
df['churn'] = df['exited']
df = df.drop(columns=['row_number', 'customer_id', 'surname', 'exited'])
df = df.drop(columns=['tenure', 'has_cr_card'])

#Model Training
df_full_train, df_test = train_test_split(df, test_size=test_size, random_state=42)
y_train = df_full_train['Churn'].values
y_test = df_test['Churn'].values 


#Fit the DictVectorizer
dv = DictVectorizer(sparse=False)
train_dict = df_full_train.to_dict(orient='records')
x_train = dv.fit_transform(train_dict)

#Train the Model
model = RandomForestClassifier(
    n_estimators=N_ESTIMATORS,
    max_depth=MAX_DEPTH,
    min_samples_leaf=MIN_SAMPLES_LEAF,
    random_state=1,
    n_jobs=-1
)
#Saving the Model and Vectorizer
with open(dv_file, 'wb') as f_out:
    pickle.dump(dv, f_out)
    
with open(output_file, 'wb') as f_out:
    pickle.dump(model, f_out)

     


























