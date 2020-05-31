# Manufacturing System Monitoring

A month ago (2020 March) I completed the Data Streaming Nanodegree by Udacity. The course was very comprehensive, the only thing I really missed was the capstone project from the end. For that reason I decided to build something, using technologies I learnt. In this project I will build a data pipeline to monitor the production in a manufacturing system, and to do this I will integrate the following components:

1. **Data Source:** OPC-UA server running unreliable machine simulations. ✅
2. **Buffer:** Kafka
    - Kafka producer: OPC-UA client subscribed to machine events.
    - [Cycle Time](https://observablehq.com/@troymagennis)
    - [OEE](https://www.oee.com/calculating-oee.html)
3. **Stream Processing:** KSQL
    - KPIs: Availability, Performance, Quality, OEE
4. **Data Store:** PostgreSQL
5. **Visiualisations:** Cube.js

## Usage:

At the current state of the project I developed the OPC-UA server and client.
Both of these applications has their own Docker containers. To run the server and the client, execute the following commands:

1. create a network in docker
```
$ docker network create OPC-UA
```

2.  run the main compose file
```
$ docker-compose up
```

At this point you should see the events on the console.


```
$ docker-compose -f docker-compose.kafka.yml up
$ docker-compose -f docker-compose.kafka.yml logs broker | grep started
```
