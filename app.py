import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Prediction", layout="centered")
st.title("Customer Churn Prediction")

with st.form("churn_form"):
    gender = st.selectbox("Gender", ["Male", "Female"], index=1)
    senior = st.selectbox("Senior Citizen", ["No", "Yes"], index=0)
    partner = st.selectbox("Partner", ["Yes", "No"], index=0)
    dependents = st.selectbox("Dependents", ["Yes", "No"], index=1)
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=70.35, step=0.01)
    total_charges = st.number_input("Total Charges", min_value=0.0, value=1397.47, step=0.01)

    submitted = st.form_submit_button("Predict Churn")

if submitted:
    data = {
        "gender": gender,
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
    }

    try:
        response = requests.post('http://127.0.0.1:5000/predict', json=data)
        response.raise_for_status()
        result = response.json()

        churn_prediction = result['churn_prediction']
        churn_probability = result['churn_probability']
        retention_advice = result['retention_advice']

        if churn_prediction == 1:
            st.error(f"Churn Prediction: Yes\nProbability of churn: {churn_probability:.2%}\nRetention advice: {retention_advice}")
        else:
            st.success(f"Churn Prediction: No\nProbability of churn: {churn_probability:.2%}\nRetention advice: {retention_advice}")

    except Exception as e:
        st.error(f"Error during prediction: {e}")
