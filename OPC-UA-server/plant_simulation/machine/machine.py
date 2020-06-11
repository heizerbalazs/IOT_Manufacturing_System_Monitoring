import random
import asyncio

class ProductionMachine():

    states = ['down', 'up']

    def __init__(self,
                machine_name,
                p_failure = 0.01,
                p_repair = 0.1,
                ideal_cycle_time = 1,
                lambda_cycle_time = 2,
                scrap_rate = 0.05):
        self.machine_name = machine_name
        self.p_failure = p_failure
        self.p_repair = p_repair
        self.ideal_cycle_time = ideal_cycle_time
        self.lambda_cycle_time = lambda_cycle_time
        self.scrap_rate = scrap_rate
        self.state = 0

    def advance_state(self):
        self.state = 1 if self.p_repair/(self.p_failure+self.p_repair) > random.uniform(0, 1) else 0

    def get_status(self):
        return self.states[self.state]

    def produce(self):
        if self.state:
            return 'scrap' if self.scrap_rate > random.uniform(0,1) else 'ok'
        return ''
    
    def get_real_cycle_time(self):
        if self.state:
            return random.expovariate(self.lambda_cycle_time) + self.ideal_cycle_time
        return self.ideal_cycle_time
    
    async def run(self):
        self.advance_state()
        await asyncio.sleep(self.get_real_cycle_time())
        output = {
            'machine_name': self.machine_name,
            'state': self.get_status(),
            'product': self.produce(),
            'ideal_cycle_time': self.ideal_cycle_time
        }
        return output