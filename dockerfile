FROM python:3

ADD main.py /
ADD secrets.json /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./main.py"]