FROM python:3.12
RUN mkdir /fastapi_3
WORKDIR /fastapi_3
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
WORKDIR /fastapi_3

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]