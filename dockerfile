FROM python:3.11-slim-buster
LABEL image="consumer_disputed_project_by_shivam"
WORKDIR /app
COPY . /app
RUN apt update -y
RUN apt-get update && pip install -r requirements.txt
EXPOSE 1000:1000
CMD ["python3", "/app/application.py"]