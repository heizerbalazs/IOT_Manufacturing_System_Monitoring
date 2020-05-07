FROM python:3.7.6

WORKDIR /usr/app

RUN python -m pip install --upgrade pip
ADD ./plant_simulation ./plant_simulation
ADD ./opc-ua-server.py ./
ADD ./requirements.txt ./
RUN python -m pip install -r requirements.txt

CMD ["python", "opc-ua-server.py"]