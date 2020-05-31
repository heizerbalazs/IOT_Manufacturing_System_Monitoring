import asyncio
import os
import json
from asyncua import Client
from kafka import KafkaProducer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

SERVER_URL = os.environ.get('OPC_UA_SERVER_URL')
NAMESPACE_URI = os.environ.get('NAMESPACE_URI')
EVENT_TYPE_PATH = ['0:Types', '0:EventTypes', '0:BaseEventType', '2:MachineCycleEvent']
OBJECTS_PATH = ['0:Objects']

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda value: json.dumps(value).encode('utf-8'),
    )

class SubscriptionHandler:
    
    def event_notification(self, event):
        event = dict([(str(k), v) for k, v in event.__dict__.items() if k not in event.internal_properties])
        event = {
            'Timestamp': str(event['Time']),
            'MachineName': event['MachineName'],
            'MachineState': event['MachineState'],
            'CycleProduct': event['CycleProduct'],
        }
        producer.send(KAFKA_TOPIC, value=event)

async def run_client(url):
    async with Client(url) as client:
        root = client.get_root_node()
        print(root)
        idx = await client.get_namespace_index(NAMESPACE_URI)

        subscription_handler = SubscriptionHandler()
        subscription = await client.create_subscription(1, subscription_handler)
        handles = []

        event_type = await root.get_child(EVENT_TYPE_PATH)
        server_objects = await root.get_child(OBJECTS_PATH)

        for machine in await server_objects.get_children():
            name = await machine.get_browse_name()
            if name.NamespaceIndex == idx:
                handle = await subscription.subscribe_events(machine, event_type)
                handles.append(handle)

        while True:
            await asyncio.sleep(1)
                    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_client(SERVER_URL))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.shutdown_asyncgens()
        loop.close()