import asyncio
import os
from asyncua import Client
from KafkaProducer.SubscriptionHandler import SubscriptionHandler

SERVER_URL = os.environ.get('OPC_UA_SERVER_URL')
print(SERVER_URL)
NAMESPACE_URI = os.environ.get('NAMESPACE_URI')
print(NAMESPACE_URI)
SERVER_URL = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'
NAMESPACE_URI = 'http://plant_simulation'
EVENT_TYPE_PATH = ['0:Types', '0:EventTypes', '0:BaseEventType', '2:MachineCycleEvent']
OBJECTS_PATH = ['0:Objects']

async def create_client(url):
    async with Client(url) as client:
        root = client.get_root_node()
        print(root)
        idx = await client.get_namespace_index(NAMESPACE_URI)

        subscription_handler = SubscriptionHandler()
        subscriptions, handles = [], []

        event_type = await root.get_child(EVENT_TYPE_PATH)
        server_objects = await root.get_child(OBJECTS_PATH)

        
        for machine in await server_objects.get_children():
            name = await machine.get_browse_name()
            if name.NamespaceIndex == idx:
                sub = await client.create_subscription(1, subscription_handler)
                subscriptions.append(sub)
                handle = await sub.subscribe_events(machine, event_type)
                handles.append(handle)
        
        return (subscriptions, handles)

async def tear_down(subscriptions, handles):
    for sub, handle in zip(subscriptions, handles):
            await sub.unsubscribe(handle)
            await sub.delete()
            
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        subscriptions, handles = loop.run_until_complete(create_client(SERVER_URL))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(tear_down(subscriptions, handles))
    finally:
        loop.shutdown_asyncgens()
        loop.close()