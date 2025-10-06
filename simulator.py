import numpy as np
import math

from params import *
from dataclasses import dataclass


class Simulator:
    def __init__(self, params:dict, system_params:SystemParams):
        self.params = params
        self.system_params = system_params
        self.data = {}
        self.data_ps = {'current':[], 'hop_rate':[]}
        # for key, val in params.items():
        #     self.params[key] = float(val)

    def initial_setting(self):
        self.channel = np.zeros(self.system_params.L, dtype=bool)
        N = round(self.params['rho'] * self.system_params.L)
        places = np.random.choice(list(range(self.system_params.L)), size=N, replace=False)
        self.channel[places] = True

    def step(self):
        current = 0; hop_num = 0
        event_num = 2*self.system_params.L #トータルのイベント数
        for _ in range(event_num):
            i = np.random.randint(0, self.system_params.L)
            d = np.random.choice([1,-1])
            if self.channel[i] and not self.channel[(i+d)%self.system_params.L]: #サイトiに粒子がおり隣には粒子がいなければ
                if self.prob(d)*self.system_params.dt > np.random.random(): #確率で遷移するか決める
                    self.channel[i] = False
                    self.channel[(i+d)%self.system_params.L] = True
                    current += d; hop_num += 1
        self.data_ps['current'].append(current/event_num/self.system_params.dt)
        self.data_ps['hop_rate'].append(hop_num/event_num/self.system_params.dt)

    def prob(self, d:int): #遷移確率の定義
        return math.exp(-self.params['beta']*(self.params['Ea']+self.params['f']*d))

    def run(self):
        self.initial_setting()
        for _ in range(self.system_params.t_max):
            self.step()

        
if __name__=='__main__':
    params = {'N':10, 'beta':1}
    system_params = SystemParams(
        L=10
    )
    simulator = Simulator(params=params, system_params=system_params)
    simulator.run()