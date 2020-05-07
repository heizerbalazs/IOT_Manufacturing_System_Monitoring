FROM python:3.7.6

WORKDIR /usr/app

RUN python -m pip install --upgrade pip
ADD ./requirements.txt ./
RUN python -m pip install -r requirements.txt
ADD ./KafkaProducer ./KafkaProducer
ADD ./opc-ua-client.py ./

CMD ["python", "opc-ua-client.py"]