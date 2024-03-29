FROM python:3.10.4

WORKDIR /home/muchori/projects/fastApi

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

