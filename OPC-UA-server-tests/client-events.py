import asyncio
import logging
from asyncua import Client

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def event_notification(self, event):
        _logger.info("New event received: %r \n", event)


async def task():
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    # url = "opc.tcp://admin@localhost:4840/freeopcua/server/"  #connect using a user

    async with Client(url=url) as client:
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        _logger.info("Objects node is: %r", root)

        # Now getting a variable node using its browse path
        obj = await root.get_child(["0:Objects", "2:MyObject"])
        _logger.info("MyObject is: %r", obj)

        myevent = await root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:MyFirstEvent"])
        _logger.info("MyFirstEventType is: %r", myevent)

        msclt = SubHandler()
        sub = await client.create_subscription(100, msclt)
        handle = await sub.subscribe_events(obj, myevent)

        myevent2 = await root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:MySecondEvent"])
        _logger.info("MySecondEventType is: %r", myevent)
        sub2 = await client.create_subscription(100, msclt)
        handle2 = await sub.subscribe_events(obj, myevent2)

        await asyncio.sleep(10)
        await sub.unsubscribe(handle)
        await sub.delete()
        await sub2.unsubscribe(handle2)
        await sub2.delete()


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(task())
    loop.close()


if __name__ == "__main__":
    main()


# INFO:asyncua:New event received: Event([
# 'MyNumericProperty:39.0',
# 'MyStringProperty:Property 39',
# "EventId:b'e46210b97e364cd3b6e99a67c9696140'",
# 'EventType:NumericNodeId(ns=2;i=2)',
# 'SourceNode:NumericNodeId(ns=2;i=1)',
# 'SourceName:MyObject',
# 'Time:2020-04-11 15:18:12.870507',
# 'ReceiveTime:2020-04-11 15:18:12.870515',
# 'LocalTime:TimeZoneDataType(Offset:120, DaylightSavingInOffset:True)',
# 'Message:LocalizedText(Encoding:2, Locale:None, Text:MyFirstEvent 39)',
# 'Severity:39'])