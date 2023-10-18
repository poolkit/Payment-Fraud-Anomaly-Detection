import streamlit as st
import requests
import json

st.title("Payment-Fraud-Detection")

# User input
col1, col2 = st.columns(2)

time_step = col1.text_input('Time Stamp')
t_id = col2.text_input("Transaction Id")
sender_id = col1.text_input('Sender Id')
sender_account = col2.text_input("Sender Account")
sender_country = col1.text_input('Sender Country')
sender_sector = col2.number_input("Sender Sector")
sender_lob = col1.text_input('Sender LOB')
bene_id = col2.text_input("Bene Id")
bene_account = col1.text_input('Bene Account')
bene_country = col2.text_input('Bene Country')
usd_amount = col1.number_input("USD Amount")
t_type = col2.text_input('Transaction Type')

input_data = {
    "Time_step": time_step,
    "Transaction_Id": t_id,
    "Sender_Id": sender_id,
    "Sender_Account": sender_account,
    "Sender_Country": sender_country,
    "Sender_Sector": sender_sector,
    "Sender_lob": sender_lob,
    "Bene_Id": bene_id,
    "Bene_Account": bene_account,
    "Bene_Country": bene_country,
    "USD_amount": usd_amount,
    "Transaction_Type": t_type
}

user_input = json.dumps(input_data)

if st.button("Get Prediction"):
    # Send user input to FastAPI for prediction
    fastapi_url = "http://backend:8000/predict"  # Replace with your FastAPI server URL

    try:
        response = requests.post(fastapi_url, data=user_input)
        if response.status_code == 200:
            prediction = response.json()["Output"]
            st.success(f"Prediction: {prediction}")
        else:
            st.error("Error making the prediction.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to FastAPI: {e}")
