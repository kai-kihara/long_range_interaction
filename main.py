import itertools
import multiprocessing as mp
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
import os

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
        self.MAX_PER_POOL = 60

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
        file_name = func.create_name(params=params)+f'_{n}'
        if file_name + ".pkl" in os.listdir(f"data_raw/{self.directory}"): return
        simulator = self.run_under_(params=params)
        #file_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        func.save_pickle(object=simulator, directory_path='data_raw/'+self.directory, file_name=file_name+'.pkl')
        print(".",end="")

    def run_chunk(self, chunk):
        with ThreadPoolExecutor(max_workers=8) as ex:
            return list(ex.map(self.run_and_save, chunk))

    def run(self):
        self.set_param_combinations_total()
        t = tqdm(total=len(self.param_combinations))
        # chunks = []
        # for i in range(math.ceil(mp.cpu_count()/self.MAX_PER_POOL)):
        #     chunks.append(self.param_combinations[self.MAX_PER_POOL*i:min(self.MAX_PER_POOL*(i+1),len(self.param_combinations))])
        with mp.Pool(processes=mp.cpu_count()) as pool:
            process_iterable = pool.imap_unordered(self.run_and_save, self.param_combinations) #並列計算
            #process_iterable = pool.imap_unordered(self.run_chunk, chunks)
            for _ in process_iterable:
                t.update()
    
    def run_and_save_process(self, param_combinations:list, queue:mp.Queue):
        self.run_and_save(param_combinations=param_combinations)
        queue.put(1)
    
    def run_processes(self):
        self.set_param_combinations_total()
        print(len(self.param_combinations))
        print('.'*len(self.param_combinations))
        max_concurrent_processes = 180
        process_list = []
        for param_combination in self.param_combinations:
            p = mp.Process(target=self.run_and_save, args=(list(param_combination),))
            p.start()
            process_list.append(p)
            while len([p for p in process_list if p.is_alive()]) >= max_concurrent_processes: time.sleep(1)
        for p in process_list: p.join()

    def run_processes_tqdm(self):
        self.set_param_combinations_total()
        print("a")
        queue = mp.Queue()
        n_tasks = len(self.param_combinations)
        with tqdm(total=n_tasks, desc="Processing") as pbar:
        # 進捗監視プロセス
            def listener():
                completed = 0
                while completed < n_tasks:
                    queue.get()  # 終了通知を受信
                    completed += 1
                    pbar.update(1)
            monitor = mp.Process(target=listener)
            monitor.start()
            max_concurrent_processes = 180
            process_list = []
            for param_combination in self.param_combinations:
                p = mp.Process(target=self.run_and_save_process, args=(list(param_combination),queue))
                p.start()
                process_list.append(p)
                while len([p for p in process_list if p.is_alive()]) >= max_concurrent_processes: time.sleep(1)
            for p in process_list: p.join()
            monitor.join()
        


if __name__=='__main__':
    directory = 'fitting_alpha025'
    func.create_directory(path='data_raw/'+directory)
    system_params = SystemParams(
        L=1200,
        t_max=10000,
        dt=1
    )
    params_range = {
        'beta':func.to_fracs([32+i for i in range(11)]+[85+i for i in range(11)]+[145+i for i in range(11)]),
        'rho': analysis.farey_array(qmax=5, half=True),#func.to_fracs([i/60 for i in range(61)]),
        "alpha":func.to_fracs([0.25]),
        #"kappa":func.to_fracs([1]),
        "K":func.to_fracs([1])
    }
    total_simulator = TotalSimulator(
        system_params=system_params,
        params_range=params_range,
        directory=directory,
        num=1,
        options=[]
    )
    #print(params_range)
    #total_simulator.run()
    total_simulator.run_processes()
    #func.save_pickle(total_simulator, directory_path='data_raw/'+directory, file_name='total_simulator.pkl')