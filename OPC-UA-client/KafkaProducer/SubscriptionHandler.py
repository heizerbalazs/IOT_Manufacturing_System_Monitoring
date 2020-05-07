class SubscriptionHandler:
    # TODO: change handler to forward the incoming data to a Kafka topic
    def event_notification(self, event):
        event = dict([(str(k), v) for k, v in event.__dict__.items() if k not in event.internal_properties])        
        print(f"New event recieved: Time={event['Time']}, Machine={event['MachineName']}, State={event['MachineState']}, Product={event['CycleProduct']}")
