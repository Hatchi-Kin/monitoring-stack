FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8089
CMD ["locust", "-f", "locustfile.py", "--web-host", "0.0.0.0", "--host", "http://serving_api:8001"]
