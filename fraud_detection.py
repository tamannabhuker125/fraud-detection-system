import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import base64

st.set_page_config(page_title="Fraud Detection System",layout="centered")
 
def add_bg_from_local(image_file):
    with open (image_file,"rb")as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp{{
            background_image:url("date:image/jpg;base64,{encoded_string}");
            background-size:cover;
            background-position:center;
            background-repeat:no-repeat;
            background-attachment:fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
            )
     


model = joblib.load("fraud_detection_pipeline.pkl")


st.title("Fraud Detection System")
st.write("Enter The Transaction Details below to predict whether the transaction is fraudulent")
st.write("Date : ",datetime.now().strftime("%d-%m-%Y"))
st.write("time : ",datetime.now().strftime("%H-%M-%S"))
st.divider()

transaction_type =st.selectbox("Transcation type",["PAYMENT","TRANSFER","CASH_OUT","CASH_IN","DEPOSIT"])

amount=st.number_input("Amount",min_value=0.0,value=1000.0)
oldbalanceOrg=st.number_input("Sender's Previous Balance",min_value=0.0,value=1000.0)
newbalanceOrig= st.number_input("Sender New Balance",min_value=0.0,value=9000.0)
oldbalanceDest= st.number_input("Receiver Previous Balance",min_value=0.0,value=0.0)  
newbalanceDest= st.number_input("Receiver New Balance",min_value=0.0,value=0.0)

if st.button("Predict"):
    input_data = pd.DataFrame([{
        "type":transaction_type,
        "amount":amount ,
        "oldbalanceOrg":
        oldbalanceOrg,
        "newbalanceOrig":
        newbalanceOrig,
        "oldbalanceDest":
        oldbalanceDest,
        "newbalanceDest":
        newbalanceDest
    }])


    prediction=model.predict(input_data)[0]

    st.subheader(f"Prediction :{int(prediction)}")

    if prediction==1:
        st.error ("This Transaction can be Fraud")
    else:
        st.success("This Transaction looks like it is not Fraud")
    