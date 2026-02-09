FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p db logs
EXPOSE 5000
CMD ["python", "main.py"]