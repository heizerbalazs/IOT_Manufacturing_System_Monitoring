# OPC UA Server

This is the data source of my IOT Manufacturing System Montitoring project. The plant_simulation folder contains the files wich purpose is to simulate an unreliable production machine.

## Usage

Start the plant simulation server.

```
docker build --tag opc-ua-server:1.0
docker run --publish 4840:4840 --detach --name opc-ua-server opc-ua-server:1.0
```

