# Manufacturing System Monitoring

A month ago (2020 March) I completed the Data Streaming Nanodegree by Udacity. The course was very comprehensive, the only thing I really missed was the capstone project from the end. For that reason I decided to build something, using technologies I learnt. In this project I will build a data pipeline to monitor the production in a manufacturing system, and to do this I will integrate the following components:

1. **Data Source:** OPC-UA server running unreliable machine simulations. ✅
2. **Buffer:** Kafka ✅
    - Kafka producer: OPC-UA client subscribed to machine events.
3. **Stream Processing:** KSQL 
    - KPIs: Availability, Performance, Quality, OEE
    - [Cycle Time](https://observablehq.com/@troymagennis)
    - [OEE](https://www.oee.com/calculating-oee.html)
4. **Data Store:** PostgreSQL
5. **Visiualisations:** Cube.js

## Usage:

At the current state of the project I developed the OPC-UA server and client.
Both of these applications has their own Docker containers. To run the server and the client, execute the following commands:

1. create a network in docker
```
$ docker network create OPC-UA
```

2. run the kafka compose file
```
$ docker-compose -f docker-compose.kafka.yml up
```

3.  run the main compose file
```
$ docker-compose up
```

4. check the content of production.cycles topic
```
$ docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic production.cycles --from-beginning
```

At this point you should see the events on the console.

5. Start the ksqldb-cli and check the production.cycles topic
```
$ docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```
```
ksql> SHOW TOPICS;
ksql> SET 'auto.offset.reset' = 'earliest';
ksql> print 'production.cycles';
```

## Resources

- https://www.teamdatascience.com/post/how-to-learn-building-big-data-pipelines-on-any-platform
- http://tutorials.jenkov.com/data-streaming/index.html
- https://github.com/FreeOpcUa/opcua-asyncio
- http://documentation.unified-automation.com/uasdkc/1.8.0/html/index.html
- https://florimond.dev/blog/articles/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/
- https://www.slideshare.net/OndejVesel2/python-queue-solution-with-asyncio-and-kafka
