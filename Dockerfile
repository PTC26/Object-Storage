FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install boto3 python-dotenv

CMD ["python", "main.py"]