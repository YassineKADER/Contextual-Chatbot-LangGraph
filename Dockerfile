FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

CMD ["python", "src/main.py"]
