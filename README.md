# Bank Customer Churn Prediction

This project is an end-to-end machine learning solution to predict customer churn for a bank. The model is trained on the [Kaggle Churn Modelling dataset](https://www.kaggle.com/datasets/sharmilacharity/churn-modelling) and deployed as a live web service using Flask, Docker, and Google Cloud Run.



**Live Service URL:** `https://churn-service-app-300316357465.us-central1.run.app/predict`

## 1. Problem Description

The goal of this project is to build a model that can predict which customers are at high risk of "exiting" (churning) their bank accounts. Identifying these at-risk customers allows the bank to proactively engage them with retention offers and incentives.

This service provides a "churn probability" for any given customer, helping the bank reduce customer attrition and protect its revenue. The dataset is imbalanced, so the model is evaluated using the AUC-ROC metric.

## 2. Exploratory Data Analysis (EDA)

My analysis (in `notebook.ipynb`) was performed to find the key drivers of churn. After cleaning the data, I used **Mutual Information (MI)** to get a quantitative score for each feature's importance against the `churn` target.

The top predictors are, by a large margin, financial and personal factors:

| Feature | Mutual Information Score |
| :--- | :--- |
| **estimated_salary** | **0.505** |
| **balance** | **0.360** |
| **age** | **0.074** |
| **num_of_products** | **0.069** |
| credit_score | 0.026 |
| geography | 0.014 |
| ... | ... |
| tenure | 0.0007 |
| has_cr_card | 0.0000 |

**Key Insights:**
* **Top Drivers:** The most powerful predictors are `estimated_salary` and `balance`. The relationship is complex, as simple box plots showed that customers who churned actually had a *higher* median balance.
* **Useless Features (Noise):** `tenure` and `has_cr_card` showed a near-zero MI score. These features were dropped from the model to reduce noise and improve performance.
* **Behavioral Signal:** Customers with **3 or 4 products** had a *dramatically* higher churn rate than those with 1 or 2, making this a key high-risk group.

## 3. Model Training & Selection

I trained and evaluated four different classification models. Since the dataset is imbalanced, I used the **ROC-AUC score** for evaluation on the validation set.

| Model | Validation AUC |
| :--- | :--- |
| **Random Forest** | **0.8549** |
| XGBoost | 0.8448 |
| Decision Tree | 0.8294 |
| Logistic Regression | 0.6871 |

The `RandomForestClassifier` was the clear winner. I then tuned its hyperparameters using `GridSearchCV` and found the optimal settings to be:
* `max_depth`: 10
* `min_samples_leaf`: 5
* `n_estimators`: 200

The final model, trained on the full 80% of the data (train + validation), achieved an **AUC score of 0.8696 on the final 20% test set.**

## 4. Reproducibility & Deployment

This project is fully reproducible and deployable.

### To Train the Model:
This will create `model.bin` and `dv.bin` from scratch using the best parameters.
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

# A sample customer from the bank dataset
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
{ "churn_probability": 0.26235239052245984 }
