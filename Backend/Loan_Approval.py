import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from joblib import Memory

# Set up caching directory
cache_dir = './cache'
memory = Memory(cache_dir, verbose=0)

def take_user_data():
    # data input from the user
    print("Enter the person's details")
    a = int(input("Enter Your Gender (0 for Female, 1 for Male): "))
    b = int(input("Enter Your Marriage Status (0 for No, 1 for Yes): "))
    c = int(input("Enter the Number Your Dependents: "))
    d = int(input("Enter Your Education (0 for Not Graduate, 1 for Graduate): "))
    e = int(input("Are You Self Employed? (0 for No, 1 for Yes): "))
    f = int(input("Enter Your Income: "))
    g = int(input("Enter Your Co-Income: "))
    h = int(input("Enter Your Loan Amount: "))
    i = int(input("Enter Your Loan Amount Term: "))
    j = int(input("Enter Your Credit History (0 or 1): "))
    k = int(input("Enter Your Property Area (0 for Rural, 1 for Semiurban, 2 for Urban): "))
    
    # creating a dictionary from the user input
    x_sample = {"Gender": a, "Married": b, "Dependents": c, "Education": d, "Self_Employed": e, 
                "ApplicantIncome": f, "CoapplicantIncome": g, "LoanAmount": h, 
                "Loan_Amount_Term": i, "Credit_History": j, "Property_Area": k}
    return x_sample

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

def process_and_predict_loan_status():
    x_sample = take_user_data()
    
    X_train, X_test, Y_train, Y_test = load_and_preprocess_data()
    
    classifier = train_model(X_train, Y_train)
    
    # convert dictionary to dataframe and predict the loan status
    x_sample_predict = classifier.predict(pd.DataFrame([x_sample]))
    if x_sample_predict == 1:
        print("You're eligible for the loan")
    else:
        print("Sorry, you're not eligible for the loan")

# Call the main function to run the process
process_and_predict_loan_status()
