from random import uniform
import time

class ProductionMachine():

    states = ['down', 'up']

    def __init__(self,
                p_failure = 0.01,
                p_repair = 0.1,
                operation_time = 1,
                scrap_rate = 0.05,
                state = 1):
        self.p_failure = p_failure
        self.p_repair = p_repair
        self.operation_time = operation_time
        self.scrap_rate = scrap_rate
        self.state = state

    def advance_state(self):
        self.state = 1 if self.p_repair/(self.p_failure+self.p_repair) > uniform(0, 1) else 0

    def get_status(self):
        return self.states[self.state]

    def produce(self):
        return 'scrap' if self.scrap_rate > uniform(0,1) else 'ok'
    
    def run(self):
        print('Starting the machine...')
        time.sleep(self.operation_time)
        while True:
            self.advance_state()
            print(f'The machine is: {self.get_status()}'
                + (f', and produced: 1 {self.produce()}' if self.state else ''))
            time.sleep(self.operation_time)