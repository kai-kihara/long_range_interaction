import itertools
import multiprocessing as mp
from tqdm import tqdm
from datetime import datetime

from params import *
from simulator import *
import func
import analysis

class TotalSimulator:
    def __init__(self, system_params:SystemParams, params_range:dict, directory:str, num:int, options:list):
        self.system_params = system_params
        self.params_range = params_range
        self.directory = directory
        self.num = num
        self.options = options

    def set_param_combinations_total(self):
        self.param_combinations = list(itertools.product(
            *self.params_range.values(),
            list(range(self.num))
            ))
        
    def run_under_(self, params:dict)->Simulator:
        simulator = Simulator(params=params, system_params=self.system_params, options=self.options)
        simulator.run()
        return simulator
    
    def run_and_save(self, param_combinations:list):
        params = {}
        for i, key in enumerate(self.params_range.keys()):
            params[key] = param_combinations[i]
        n = param_combinations[-1]
        #params_ft = {k:float(v) for k, v in params.items()}
        simulator = self.run_under_(params=params)
        file_name = func.create_name(params=params)+f'_{n}'
        #file_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        func.save_pickle(object=simulator, directory_path='data_raw/'+self.directory, file_name=file_name+'.pkl')

    def run(self):
        self.set_param_combinations_total()
        t = tqdm(total=len(self.param_combinations))
        with mp.Pool(processes=mp.cpu_count()) as pool:
            process_iterable = pool.imap_unordered(self.run_and_save, self.param_combinations) #並列計算
            for _ in process_iterable:
                t.update()

if __name__=='__main__':
    directory = 'fitting'
    func.create_directory(path='data_raw/'+directory)
    system_params = SystemParams(
        L=1200,
        t_max=10000,
        dt=1
    )
    params_range = {
        'beta':func.to_fracs([10*i for i in range(21)]),
        'rho':analysis.farey_array(qmax=5),#func.to_fracs([0,1/10,2/10,3/10,4/10,5/10,6/10,7/10,8/10,9/10,10/10]),
        "alpha":func.to_fracs([2]),
        #"kappa":func.to_fracs([1]),
        "K":func.to_fracs([1])
    }
    total_simulator = TotalSimulator(
        system_params=system_params,
        params_range=params_range,
        directory=directory,
        num=1,
        options=["yukawa"]
    )
    total_simulator.run()
    #func.save_pickle(total_simulator, directory_path='data_raw/'+directory, file_name='total_simulator.pkl')