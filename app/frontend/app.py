import streamlit as st
import requests
import json

st.title("FastAPI and Streamlit Integration")

# User input
user_input = st.text_area("Enter Data:")

if st.button("Get Prediction"):
    # Send user input to FastAPI for prediction
    fastapi_url = "http://127.0.0.1:8000/predict"  # Replace with your FastAPI server URL

    try:
        response = requests.post(fastapi_url, json=user_input)
        if response.status_code == 200:
            prediction = response.json()["Output"]
            st.success(f"Prediction: {prediction}")
        else:
            st.error("Error making the prediction.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to FastAPI: {e}")
