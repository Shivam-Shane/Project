
FROM python:3.7-slim-buster
WORKDIR /app
COPY . /app
RUN apt update -y
RUN apt-get update && pip install -r requirements.txt
EXPOSE 8080:8080
RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
CMD ["python3", "application.py"]

