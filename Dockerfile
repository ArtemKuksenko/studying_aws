FROM python:3.11.1-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD ["python3", "start.py"]
