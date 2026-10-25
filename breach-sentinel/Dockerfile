FROM python:3.11-slim
WORKDIR /app
# The sentinel needs the data and logs from the API
COPY . .
# Sentinel requires faker for its data loading if not already present
RUN pip install faker
CMD ["python", "sentinel.py"]
