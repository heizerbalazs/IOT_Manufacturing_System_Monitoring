import random
import asyncio

class ProductionMachine():

    states = ['down', 'up']

    def __init__(self,
                machine_name,
                p_failure = 0.01,
                p_repair = 0.1,
                operation_time = 1,
                scrap_rate = 0.05,
                state = 1):
        self.machine_name = machine_name
        self.p_failure = p_failure
        self.p_repair = p_repair
        self.operation_time = operation_time
        self.scrap_rate = scrap_rate
        self.state = state

    def advance_state(self):
        self.state = 1 if self.p_repair/(self.p_failure+self.p_repair) > random.uniform(0, 1) else 0

    def get_status(self):
        return self.states[self.state]

    def produce(self):
        if self.state:
            return 'scrap' if self.scrap_rate > random.uniform(0,1) else 'ok'
        return ''
    
    async def run(self):
        await asyncio.sleep(self.operation_time)
        self.advance_state()
        output = {
            'machine_name': self.machine_name,
            'state': self.get_status(),
            'product': self.produce()
        }
        return output