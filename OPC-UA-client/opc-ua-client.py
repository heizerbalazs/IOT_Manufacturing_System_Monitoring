import asyncio
import os
from asyncua import Client
from KafkaProducer.SubscriptionHandler import SubscriptionHandler

if os.environ.get('IN_DOCKER'):
    SERVER_URL = os.environ.get('OPC_UA_SERVER_URL')
    NAMESPACE_URI = os.environ.get('NAMESPACE_URI')
else:
    SERVER_URL = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'
    NAMESPACE_URI = 'http://plant_simulation'

EVENT_TYPE_PATH = ['0:Types', '0:EventTypes', '0:BaseEventType', '2:MachineCycleEvent']
OBJECTS_PATH = ['0:Objects']

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
            await asyncio.sleep(10)
                    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_client(SERVER_URL))
    except KeyboardInterrupt:
        pass
    finally:
        loop.shutdown_asyncgens()
        loop.close()