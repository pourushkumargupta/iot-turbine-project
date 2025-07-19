# ✅ Use lightweight Python
FROM python:3.10-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Copy ONLY app files (including model.pkl inside streamlit-app/)
COPY . /app

# ✅ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose Streamlit port
EXPOSE 8501

# ✅ Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false"]
