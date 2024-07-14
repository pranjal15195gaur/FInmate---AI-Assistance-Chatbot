import time

from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from joblib import Memory

# Set up caching directory
cache_dir = './cache'
memory = Memory(cache_dir, verbose=0)

# app = Flask(__name__)


@memory.cache
def load_and_preprocess_data():
    # loading the dataset to pandas DataFrame
    loan_data = pd.read_csv('dataset.csv')

    # dropping the missing values
    loan_data = loan_data.dropna()

    # label encoding
    loan_data.replace({"Loan_Status": {'N': 0, 'Y': 1}}, inplace=True)

    # replacing the value of 3+ to 4
    loan_data = loan_data.replace(to_replace='3+', value=4)

    # convert categorical columns to numerical values
    loan_data.replace({'Married': {'No': 0, 'Yes': 1}, 'Gender': {'Male': 1, 'Female': 0},
                       'Self_Employed': {'No': 0, 'Yes': 1}, 'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2},
                       'Education': {'Graduate': 1, 'Not Graduate': 0}}, inplace=True)

    # separating the data and label
    X = loan_data.drop(columns=['Loan_ID', 'Loan_Status'], axis=1)
    Y = loan_data['Loan_Status']

    # splitting the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

    return X_train, X_test, Y_train, Y_test


@memory.cache
def train_model(X_train, Y_train):
    # creating the SVM classifier
    classifier = svm.SVC(kernel='linear')

    # training the Support Vector Machine model
    classifier.fit(X_train, Y_train)

    return classifier


def predict_loan_status(data):
    X_train, X_test, Y_train, Y_test = load_and_preprocess_data()
    classifier = train_model(X_train, Y_train)

    # convert dictionary to dataframe and predict the loan status
    x_sample_predict = classifier.predict(pd.DataFrame([data]))
    if x_sample_predict == 1:
        newdict = {}
        newdict['message'] = "You are eligible for the loan"
        newdict['status'] = True
        return newdict
    else:
        newdict = {}
        newdict['message'] = "Sorry, you are not eligible for the loan"
        newdict['status'] = False
        return newdict


# @app.route('/check_loan_eligibility', methods=['POST'])
# def check_loan_eligibility():
#     try:
#         # Get JSON payload
#         data = request.get_json()
#
#         # Validate payload
#         if not isinstance(data, dict):
#             return jsonify({"error": "Invalid payload format"}), 400
#
#         # Predict loan status
#         result = predict_loan_status(data)
#
#         # Return the result as a JSON response
#         return jsonify({"message": result})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(port=5001)
# start = time.time()
#
# print(predict_loan_status(
# {
#            "Gender": 1,
#            "Married": 1,
#            "Dependents": 0,
#            "Education": 1,
#            "Self_Employed": 0,
#            "ApplicantIncome": 5000,
#            "CoapplicantIncome": 0,
#            "LoanAmount": 200,
#            "Loan_Amount_Term": 360000,
#            "Credit_History": 1,
#            "Property_Area": 2
#          }
# ))
#
# end = time.time()
# print('Time taken',end - start)