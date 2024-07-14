import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from joblib import Memory

# Set up caching directory
cache_dir = './cache'
memory = Memory(cache_dir, verbose=0)

def take_user_data():
    # Take the user data
    a = int(input("Enter Your Limit Balance: "))
    b = int(input("Enter Your Gender (1 for male, 2 for female): "))
    c = int(input("Enter Your Education (1 to 4): "))
    d = int(input("Are You Married? (1 for married, 2 for single, 3 for others): "))
    e = int(input("Enter Your Age: "))
    f = int(input("Enter Your Pay_0: "))
    g = int(input("Enter Your Pay_2: "))
    h = int(input("Enter Your Pay_3: "))
    i = int(input("Enter Your Pay_4: "))
    j = int(input("Enter Your Pay_5: "))
    k = int(input("Enter Your Pay_6: "))
    l = int(input("Enter Your Bill Amount 1: "))
    m = int(input("Enter Your Bill Amount 2: "))
    n = int(input("Enter Your Bill Amount 3: "))
    o = int(input("Enter Your Bill Amount 4: "))
    p = int(input("Enter Your Bill Amount 5: "))
    q = int(input("Enter Your Bill Amount 6: "))
    r = int(input("Enter Your Pay Amount 1: "))
    s = int(input("Enter Your Pay Amount 2: "))
    t = int(input("Enter Your Pay Amount 3: "))
    u = int(input("Enter Your Pay Amount 4: "))
    v = int(input("Enter Your Pay Amount 5: "))
    w = int(input("Enter Your Pay Amount 6: "))

    # Create dictionary
    X_sample = {
        "LIMIT_BAL": a, "SEX": b, "EDUCATION": c, "MARRIAGE": d, "AGE": e,
        "PAY_0": f, "PAY_2": g, "PAY_3": h, "PAY_4": i, "PAY_5": j, "PAY_6": k,
        "BILL_AMT1": l, "BILL_AMT2": m, "BILL_AMT3": n, "BILL_AMT4": o, "BILL_AMT5": p, "BILL_AMT6": q,
        "PAY_AMT1": r, "PAY_AMT2": s, "PAY_AMT3": t, "PAY_AMT4": u, "PAY_AMT5": v, "PAY_AMT6": w
    }
    return X_sample

@memory.cache
def train_model():
    data = pd.read_csv("Fault_Dataset.csv")
    X = data.drop(labels=["default payment next month"], axis=1)
    y = data["default payment next month"]

    # Data Split
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=50)

    # Preprocessing steps
    train_scaler = StandardScaler()
    scaled_train_data = train_scaler.fit_transform(x_train)
    
    # GNB Classifier
    clf = GaussianNB()
    clf.fit(scaled_train_data, y_train)
    
    return clf, train_scaler

def process_and_predict_fault():
    x_sample = take_user_data()
    
    clf, scaler = train_model()
    
    # Process the user data
    x_data = pd.DataFrame([x_sample])
    scaled_x_data = scaler.transform(x_data)
    
    # Make prediction
    X_sample_GNB_predict = clf.predict(scaled_x_data)
    if X_sample_GNB_predict == 1:
        print("Congratulations, No Fault.")
    else:
        print("Fault Found!")

# Call the main function to run the process
process_and_predict_fault()
