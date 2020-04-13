import asyncio
import random

import random
import time

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
        return 'scrap' if self.scrap_rate > random.uniform(0,1) else 'ok'
    
    async def run(self):
        while True:
            await asyncio.sleep(self.operation_time)
            self.advance_state()
            print(f'The {self.machine_name} is: {self.get_status()}'
                + (f', and produced: 1 {self.produce()}' if self.state else ''))

if __name__ == "__main__":
    pm1 = ProductionMachine('Production Machine 1', 0.1, 0.6, 1)
    pm2 = ProductionMachine('Production Machine 2', 0.1, 0.6, 2)
    
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(pm1.run())
        loop.create_task(pm2.run())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
