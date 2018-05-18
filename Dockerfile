FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code_monitor
WORKDIR /code_monitor
ADD . /code_monitor/
RUN pip install -r requirements.txt