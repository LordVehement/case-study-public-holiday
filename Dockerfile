FROM python:3.8.1

ADD app.py .

RUN pip install pandas flask

CMD [ "python", "./app.py" ]