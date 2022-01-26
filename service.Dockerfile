FROM python:3
WORKDIR /transfer-app
COPY . .
RUN pip install -r requirements.txt