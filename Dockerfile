FROM python:2.7.14-slim-jessie
MAINTAINER Graha "grahaindia@gmail.com"
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install Flask
CMD ["python","app.py"]
