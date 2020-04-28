import asyncio
import os
from asyncua import Client

SERVER_URL = os.environ.get('OPC_UA_SERVER_URL')
NAMESPACE_URI = os.environ.get('NAMESPACE_URI')
EVENT_TYPE_PATH = ['0:Types', '0:EventTypes', '0:BaseEventType', '2:MachineCycleEvent']
OBJECTS_PATH = ['0:Objects']

class SubscriptionHandler:
    # TODO: change handler to forward the incoming data to a Kafka topic
    def event_notification(self, event):
        event = dict([(str(k), v) for k, v in event.__dict__.items() if k not in event.internal_properties])        
        print(f"New event recieved: Time={event['Time']}, Machine={event['MachineName']}, State={event['MachineState']}, Product={event['CycleProduct']}")

async def create_client(url):
    async with Client(url) as client:
        root = client.get_root_node()
        print(root)
        idx = await client.get_namespace_index(NAMESPACE_URI)

        subscription_handler = SubscriptionHandler()
        subscriptions, handles = [], []

        event_type = await root.get_child(EVENT_TYPE_PATH)
        server_objects = await root.get_child(OBJECTS_PATH)

        try:
            for machine in await server_objects.get_children():
                name = await machine.get_browse_name()
                if name.NamespaceIndex == idx:
                    sub = await client.create_subscription(1, subscription_handler)
                    subscriptions.append(sub)
                    handle = await sub.subscribe_events(machine, event_type)
                    handles.append(handle)
            while True:
                await asyncio.sleep(10)
        except KeyboardInterrupt:
            for sub, handle in zip(subscriptions, handles):
                await sub.unsubscribe(handle)
                await sub.delete()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(create_client(SERVER_URL))
    except KeyboardInterrupt:
        pass
    finally:
        loop.shutdown_asyncgens()
        loop.close()