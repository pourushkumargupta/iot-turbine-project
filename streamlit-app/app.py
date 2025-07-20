import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Wind Turbine Forecast Dashboard")

# ✅ Load trained model
with open('../models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("⛽ Wind Turbine Power Forecasting")

if st.button("Generate Forecast"):
    prediction = model.predict()
    forecast = prediction.forecast
    st.success("✅ Forecast Generated!")
    st.dataframe(forecast.head(10))

    st.line_chart(forecast)
