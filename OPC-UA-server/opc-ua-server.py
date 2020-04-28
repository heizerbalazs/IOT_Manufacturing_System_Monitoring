import asyncio
import logging
import os
from asyncua import ua
from asyncua.server import Server, EventGenerator
from plant_simulation.machine import ProductionMachine

SERVER_URL = f'opc.tcp://0.0.0.0:{os.environ.get(OPC_UA_SERVER_PORT)}'
NAMESPACE_URI = os.environ.get('NAMESPACE_URI')
OBJECT_TYPES_PATH = ['0:Types', '0:ObjectTypes', '0:BaseObjectType']

async def generate_event(prod_machine, event_generator, event_loop):
    output = await prod_machine.run()
    event_generator.event.Severity = 1
    event_generator.event.MachineName = output['machine_name']
    event_generator.event.MachineState = output['state']
    event_generator.event.CycleProduct = output['product']
    event_generator.trigger()
    loop.create_task(generate_event(prod_machine, event_generator, event_loop))

async def create_server(machine_count):
    # Instantiate server and set up namespace
    server = Server()
    await server.init()
    server.set_endpoint(SERVER_URL)
    idx = await server.register_namespace(NAMESPACE_URI)

    # Create machine object type
    types =  server.get_node(ua.ObjectIds.BaseObjectType)
    super_opject_type = await server.get_root_node() \
                            .get_child(OBJECT_TYPES_PATH)
    machine_object_type = await types.add_object_type(idx, 'MachineType')

    # Create event type
    machine_cycle_event = await server.create_custom_event_type(
        idx, 'MachineCycleEvent', ua.ObjectIds.BaseEventType,
        [('MachineName', ua.VariantType.String),
         ('MachineState', ua.VariantType.String),
         ('CycleProduct', ua.VariantType.String)]
    )

    # Create machine object instances
    evgens = []
    objects = server.get_objects_node()
    for i in range(machine_count):
        machine = await objects.add_object(idx,
                                        f'ProductionMachine{i}',
                                        machine_object_type)
        evgen = await server.get_event_generator(machine_cycle_event,machine)
        evgens.append(evgen)

    await server.start()
    return server, evgens

if __name__ == '__main__':
    machines = []
    machines.append(ProductionMachine('Production Machine 1', 0.1, 0.6, 1))
    machines.append(ProductionMachine('Production Machine 2', 0.1, 0.6, 3))
    machines.append(ProductionMachine('Production Machine 3', 0.1, 0.6, 2))

    loop = asyncio.get_event_loop()
    server, evgens = loop.run_until_complete(create_server(len(machines)))
    try:
        # Recursively create tasks for loop
        [loop.create_task(generate_event(machine, evgen, loop))
                for machine, evgen in zip(machines, evgens)]
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.shutdown_asyncgens()
        loop.close()