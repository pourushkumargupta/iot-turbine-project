
import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Wind Turbine Forecast Dashboard")

base_path = os.getcwd()
print(f"✅ Streamlit running at: {base_path}")

if 'streamlit-app' in base_path:
    model_path = '../models/best_model.pkl'
else:
    model_path = 'models/best_model.pkl'

# ✅ Load trained model
with open(model_path, 'rb') as f:
    model = pickle.load(f)

st.title("⛽ Wind Turbine Power Forecasting")

if st.button("Generate Forecast"):
    prediction = model.predict()
    forecast = prediction.forecast
    st.success("✅ Forecast Generated!")
    st.dataframe(forecast.head(10))
    st.line_chart(forecast)
# minor comment added
# minor comment_1 added
# minor comment added
