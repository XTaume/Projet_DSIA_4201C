FROM python:3.12.7

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip

RUN pip install streamlit

CMD ["streamlit", "run", "/app/Projet_final/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

