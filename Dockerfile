FROM python:3.11.1-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "start.py"]
