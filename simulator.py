import numpy as np
import math
from copy import deepcopy

from params import *
from func_ucu import ucu
from dataclasses import dataclass
from fractions import Fraction


class Simulator:
    def __init__(self, params:dict, system_params:SystemParams, options:list):
        self.params = params
        self.system_params = system_params
        self.data = {}
        self.data_ps = {'current':[], 'hop_rate':[]}
        self.options = options
        # for key, val in params.items():
        #     self.params[key] = float(val)

    def initial_setting(self):
        U = ucu(rho=self.params["rho"])
        self.channel = U * round(self.system_params.L/len(U))

    def step(self):
        current = 0; hop_num = 0
        event_num = 2*self.system_params.L #トータルのイベント数
        for _ in range(event_num):
            i = np.random.randint(0, self.system_params.L)
            d = np.random.choice([1,-1])
            if self.channel[i] and not self.channel[(i+d)%self.system_params.L]: #サイトiに粒子がおり隣には粒子がいなければ
                dE = self.potential_change(i=i, d=d)
                if self.prob(dE)*self.system_params.dt > np.random.random(): #確率で遷移するか決める
                    self.channel[i] = False
                    self.channel[(i+d)%self.system_params.L] = True
                    current += d; hop_num += 1
        self.data_ps['current'].append(current/event_num/self.system_params.dt)
        self.data_ps['hop_rate'].append(hop_num/event_num/self.system_params.dt)

    def potential_change(self, i:int, d:int): #遷移確率の定義
        channel_after_hop = deepcopy(self.channel)
        channel_after_hop[i] = False
        channel_after_hop[(i+d)%self.system_params.L] = True
        org_potential = self.potential(r=self.particle_distances(channel=self.channel, j=i))
        new_potential = self.potential(r=self.particle_distances(channel=channel_after_hop, j=(i+d)%self.system_params.L))
        dE = new_potential - org_potential
        return dE
    
    def prob(self, dE:float):
        if "real_time" in self.options:
            return np.exp(-self.params["beta"]*dE/2)
        else:
            if dE > 0: return np.exp(-self.params["beta"]*dE)
            else: return 1

    def potential(self, r):
        if "yukawa" in self.options:
            return float(self.params["K"])*sum(np.exp(-float(self.params["kappa"])*r)/r)
        elif "spring" in self.options:
            return float(self.params["K"])*sum(r**2)/self.system_params.L**2
        else:
            return float(self.params["K"])*sum(1/r**float(self.params["alpha"]))
    
    def particle_distances(self, channel:list, j:int):
        return np.array([dist for i, particle in enumerate(channel) if particle and i != j for dist in (abs(j - i), self.system_params.L - abs(j - i))])
    
    def run(self):
        self.initial_setting()
        for _ in range(self.system_params.t_max):
            self.step()

        
if __name__=='__main__':
    params = {'beta':10, "rho":Fraction(1,2), "kappa":1,  "K":1}
    system_params = SystemParams(
        L=12,
        t_max=100,
        dt=1
    )
    simulator = Simulator(params=params, system_params=system_params,options=["yukawa"])
    #simulator.initial_setting()
    #print(simulator.particle_distances(channel=simulator.channel, j=1))
    simulator.run()