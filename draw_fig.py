import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from fractions import Fraction

from merge_data import *
from simulator import *
import func
from params import *
import plt_func

class DrawFig:
    def __init__(self, file:str):
        self.results:Results = load_pickle(file_name=file+'.pkl', directory_path='data')
        self.directory = file
        self.params_def = self.results.data[0].params
        self.cmap = {'rho':'jet', 'beta':'Reds', "kappa":"Greys"}
        self.xlabel = {'rho':'Density', "beta":"Inverse temperature"}
        self.label = {'beta':r'$\beta$', "kappa":r"$\kappa$", "rho":r"$\rho$"}
        self.ylabel = {'hop_rate':'Hop rate'}

    def set_params_def(self, params:dict):
        for key, val in params.items():
            self.params_def[key] = Fraction(val).limit_denominator()

    def set_params_fixed(self, ects:list[str]):
        params_fixed = deepcopy(self.params_def)
        for ect in ects:
            del params_fixed[ect]
        return params_fixed

    def save(self, fig:matplotlib.figure.Figure, name, style:str='png'):
        plt_func.save_fig(fig, directory=self.directory, file_name=name, style=style)

    def extract_value(self, value_name, xaxis, label):
        params_fixed = self.set_params_fixed(ects=[xaxis, label])
        value_arr = [] #[value, params_ect]
        for result in self.results.data:
            result:SimulationData
            if is_match(params=result.params, params_fixed=params_fixed):
                value_arr.append({'mean':np.mean(result.values[value_name]), 'std':np.std(result.values[value_name]), 'xaxis':result.params[xaxis], 'label':result.params[label]})
        sorted_value_arr = sorted(value_arr, key=lambda x: (x['label'], x['xaxis']))
        value_tot = [] # list[dict{value_list, xaxis_list, label}]
        for i, value_set in enumerate(sorted_value_arr):
            l = value_set['label']
            if i == 0: value_tot.append({'mean':[], 'std':[], 'xaxis':[], 'label':l})
            elif l != sorted_value_arr[i-1]['label']:value_tot.append({'mean':[], 'std':[], 'xaxis':[], 'label':l})
            for key in ['mean', 'std', 'xaxis']:
                value_tot[-1][key].append(value_set[key])
        return value_tot
            
    def draw_value(self, xaxis, label, value_name, label_vals=[], yscale:str="linear", approx:bool=False):
        fig, ax = plt_func.create_subplots()
        value_tot = self.extract_value(value_name=value_name, xaxis=xaxis, label=label)
        cmap = plt.get_cmap(self.cmap[label])
        if len(label_vals) > 0: label_num = len(label_vals)
        else: label_num = len(value_tot)
        i = 1
        for value_arr in value_tot:
            if label_vals == [] or value_arr['label'] in label_vals:
                ax.errorbar(value_arr['xaxis'], value_arr['mean'], yerr=value_arr['std'], marker='o', capthick=1, capsize=2, label=self.label[label]+f'={value_arr['label']}', color=cmap(i/label_num))
                if approx:
                    rhos, Js = analysis.approx_fdiagram(qmax=i+1)
                    ax.plot(rhos, Js, color=cmap(i/label_num), linestyle="dashed")
                i+=1
        ax.legend()
        ax.set_yscale(yscale)
        ax.set_xlabel(self.xlabel[xaxis])
        ax.set_ylabel(self.ylabel[value_name])
        #ax.set_title(self.label["beta"]+f"={self.params_def["beta"]}")
        name = value_name + f'_vs_{xaxis}_{label}'
        self.save(fig=fig, name=name)

if __name__ == '__main__':
    file_name = 'yukawa_plus'
    func.create_directory(path='image/'+file_name)
    plt_func.plt_setting()
    df = DrawFig(file=file_name)
    #df.params_def["rho"] = Fraction(1,3)
    df.draw_value(xaxis='rho', label='beta', value_name='hop_rate')
