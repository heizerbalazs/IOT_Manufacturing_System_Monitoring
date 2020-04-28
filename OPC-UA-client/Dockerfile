FROM python:3.7.6

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN python -m pip install -r requirements.txt
ADD ./opc-ua-client.py ./

CMD ["python", "opc-ua-client.py"]