import os
from copy import deepcopy
import numpy as np

from func import *
from simulator import *
from main import *

class SimulationData: #複数回シミュレーションしたときに統合する用
    def __init__(self, params:dict):
        self.params = params
        self.simulators = []
        self.values = {} #dict{list}

    def extract_from_simulator(self, simulator:Simulator):
        for key, value in simulator.data.items():
            if key not in self.values.keys():
                self.values[key] = [value]
            else: self.values[key].append(value)

class Results:
    def __init__(self, directory, t_discard, data_file:list=[]):
        self.directory = directory
        self.data = data_file
        self.t_discard = t_discard
        self.params_prev = []
        for data in data_file:
            data:SimulationData
            self.params_prev.append(data.params)
    
    def extract_data(self):
        for file in os.listdir(f'data_raw/{self.directory}'):
            file_pkl = load_pickle(file_name=file, directory_path=f'data_raw/{self.directory}')
            if type(file_pkl) == Simulator:
                params = file_pkl.params
                #if not params["rho"].denominator in [1,2,3,4,5,6,10,12,15,20,30,60]: continue
                values = self.calc_mean(simulator=file_pkl, values=file_pkl.data_ps)
                for simulation_data in self.data:
                    simulation_data:SimulationData
                    if params == simulation_data.params:
                        if not params in self.params_prev: #前のデータと重複するものは省く
                            self.add_simulation_data(simulation_data=simulation_data, values=values)
                        break
                else:
                    simulation_data = SimulationData(params=params)
                    self.add_simulation_data(simulation_data=simulation_data, values=values)
                    self.data.append(simulation_data)

            elif type(file_pkl) == TotalSimulator:
                self.system_params = file_pkl.system_params

    def add_simulation_data(self, simulation_data:SimulationData, values:dict):
        for key, val in values.items():
            if key not in simulation_data.values: simulation_data.values[key] = [val]
            else: simulation_data.values[key].append(val)

    def calc_mean(self, simulator:Simulator, values:dict):
        for key, value in simulator.data_ps.items():
            values[key] = np.mean(value[self.t_discard:])
        return values

    def save(self, name):
        create_directory(path="data")
        save_pickle(object=self, directory_path='data', file_name=name)

    def run(self, name=''):
        if name == '': name = self.directory + '.pkl'
        self.extract_data()
        self.save(name)
            
if __name__ == '__main__':
    #results_prev:Results = load_pickle(file_name='fitting_yukawa.pkl', directory_path='data')
    results = Results(directory='yukawa', t_discard=1000)
    results.run()
