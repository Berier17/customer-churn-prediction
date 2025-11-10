# customer-churn-prediction
End-to-end machine learning project to predict customer churn. Includes a model trained on the Telco dataset and deployed as a web service using Flask, Docker, and Google Cloud Run.
# Customer Churn Prediction Project

This project is an end-to-end machine learning solution to predict customer churn for a telecommunications company. The model is trained on the [Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) and deployed as a live web service.

**Live Service URL:** `https://churn-service-app-300316357465.us-central1.run.app/predict`

## 1. Problem Description

The goal of this project is to build a model that can predict which customers are at high risk of "churning" (leaving the company). In the competitive telecom industry, retaining existing customers is far more cost-effective than acquiring new ones.

This service provides a "churn probability" for any given customer, allowing the business to:
* Identify high-risk customers.
* Target them with special retention offers, discounts, or improved customer service.
* Reduce overall churn and increase revenue.

The provided dataset is imbalanced (73.5% not churn, 26.5% churn), which requires the use of metrics like AUC-ROC instead of accuracy.

## 2. Exploratory Data Analysis (EDA)

My analysis (in `notebook.ipynb`) was performed to find the key drivers of churn. After cleaning the data, I used **Mutual Information (MI)** to get a quantitative score for each feature's importance.

The top predictors are, by far, the financial and contract-related features:

| Feature | Mutual Information Score |
| :--- | :--- |
| **TotalCharges** | **0.537** |
| **MonthlyCharges** | **0.173** |
| **Contract** | **0.098** |
| **tenure** | **0.079** |

**Key Insights:**
* **Financials are Key:** The MI scores show that `TotalCharges` is the strongest predictor. This is logical, as it's highly correlated with `tenure`—customers who have been with the company longer (and thus have higher total charges) are much less likely to churn.
* **Actionable Drivers:** The most important *actionable* drivers are `MonthlyCharges` and `Contract`. My visual analysis confirmed that customers on "Month-to-month" contracts churn at a *dramatically* higher rate (over 40%) compared to those on "Two year" contracts (under 3%).

## 3. Model Training & Selection

I trained and evaluated four different classification models. Since the dataset is imbalanced, I used the **ROC-AUC score** for evaluation on the validation set.

| Model | Validation AUC |
| :--- | :--- |
| **Logistic Regression (Baseline)** | **0.8371** |
| Decision Tree | 0.8146 |
| Random Forest | 0.8133 |
| XGBoost | 0.8265 |

The baseline `LogisticRegression` model performed the best. I then tuned its `C` (regularization) parameter and found the optimal value to be `C=0.1`.

The final model, trained on the full 80% of the data (train + validation), achieved an **AUC score of 0.8616 on the final 20% test set.**

## 4. Reproducibility & Deployment

This project is fully reproducible and deployable.

### To Train the Model:
This will create `model.bin` and `dv.bin` from scratch.
1.  Set up a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the training script:
    ```bash
    python train.py
    ```

### To Run the Web Service Locally:
1.  Make sure you have the `.bin` files and all dependencies.
2.  Run the Flask app:
    ```bash
    python predict.py
    ```
3.  From another terminal, send a request (see `test.py` for an example).

### To Run with Docker:
1.  Build the container image:
    ```bash
    docker build -t churn-service .
    ```
2.  Run the container:
    ```bash
    docker run -p 9696:9696 churn-service
    ```

## 5. Testing the Deployed Service

You can test the live service by sending a `POST` request to the public URL with a customer's JSON data.

**Service URL:** `https://churn-service-app-300316357465.us-central1.run.app/predict`

**Example `test.py`:**
```python
import requests

# This is the public URL for the deployed service
url = '[https://churn-service-app-300316357465.us-central1.run.app/predict](https://churn-service-app-300316357465.us-central1.run.app/predict)'

# A sample customer
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

# Expected Output: {'churn_probability': 0.4545...}
