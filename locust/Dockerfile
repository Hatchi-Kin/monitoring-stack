FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8089

CMD ["locust", "-f", "locust_file.py", "--web-host", "0.0.0.0", "--host", "http://name-of-your-service:port", "--username", "YOUR_USERNAME", "--password", "YOUR_PASSWORD"]
