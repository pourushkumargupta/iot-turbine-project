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

    # ✅ Safely convert forecast to simple Pandas DataFrame to avoid pyarrow dependency
    forecast_df = pd.DataFrame(forecast)

    st.success("✅ Forecast Generated!")
    st.write("🔍 Preview of Forecast:")
    st.write(forecast_df.head(10))

    # ✅ Plot only if numeric columns exist
    try:
        st.line_chart(forecast_df.select_dtypes(include='number'))
    except Exception as e:
        st.warning(f"⚠️ Could not plot line chart: {e}")


# minor comment added 8
