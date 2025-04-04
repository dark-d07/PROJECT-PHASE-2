import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_excel('balanced_symptom_data.xlsx')
print(df['label'].value_counts())

X = df.drop('label', axis=1).values
y = df['label'].values

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

def get_user_input():
    print("Please enter the following details about your condition:")
    try:
        days_of_fever = int(input("How many days have you had a fever (0 if no fever)? "))
        temperature = float(input("What is your temperature in Fahrenheit (e.g., 98.6)? "))
        previous_issues = int(input("Do you have any previous health issues (1 = Yes, 0 = No)? "))
        vomiting = int(input("Are you experiencing vomiting (1 = Yes, 0 = No)? "))
        cold = int(input("Do you have a cold (1 = Yes, 0 = No)? "))
        fatigue = int(input("Are you feeling fatigued or unusually tired (1 = Yes, 0 = No)? "))
        cough = int(input("Do you have a cough (1 = Yes, 0 = No)? "))
        body_pain = int(input("Do you have body pain (1 = Yes, 0 = No)? "))
        user_data = [days_of_fever, temperature, previous_issues, vomiting, cold, fatigue, cough, body_pain]
        return user_data
    except ValueError:
        print("Invalid input. Please enter the correct values.")
        return get_user_input()

def predict_new_case(model, user_data):
    user_data_scaled = scaler.transform(np.array(user_data).reshape(1, -1))
    prediction = model.predict(user_data_scaled)
    
    if prediction >= 2: 
        print("\n!!! Serious condition detected! !!!")
        print("It is advisable to consult a doctor immediately.")
    elif 1 <= prediction < 2: 
        print("\n!!! It seems like a mild case. !!!")
        print("Consider home remedies.")
        print("- Get plenty of rest and avoid strenuous activity.")
        print("- Maintain good hygiene by washing your hands regularly.")
    else:  
        print("\n!!! Normal condition detected. !!!")
        print("No action needed. If symptoms persist or worsen, please consult a doctor.")

def main():
    print("Welcome to the Symptom Checker!")
    user_data = get_user_input()
    predict_new_case(model, user_data)

if __name__ == "__main__":
    main()
