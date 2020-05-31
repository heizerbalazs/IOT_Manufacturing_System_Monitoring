FROM python:3.7.6

WORKDIR /usr/app

RUN python -m pip install --upgrade pip
ADD ./requirements.txt ./
RUN python -m pip install -r requirements.txt
RUN git clone https://github.com/dpkp/kafka-python
RUN python -m pip install ./kafka-python
ADD ./opc-ua-client.py ./

CMD ["python", "opc-ua-client.py"]