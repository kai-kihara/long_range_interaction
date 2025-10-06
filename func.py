import pickle
import os
from copy import deepcopy
from fractions import Fraction

from params import *


def save_pickle(object, directory_path:str, file_name:str): #pickleファイルを保存
    with open(f'{directory_path}/{file_name}', 'wb') as f:
        pickle.dump(object, f)

def load_pickle(file_name:str, directory_path:str): #pickleファイルを読み込む
    with open(f'{directory_path}/{file_name}', 'rb') as f:
        object = pickle.load(f)
    return object

def create_directory(path): #データを保存するディレクトリの作成
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created successfully.")
    else:
        print(f"Directory '{path}' already exists.")

def create_name(params:dict): #保存するファイル名を決める
    def frac_to_str(frac:Fraction):
        return str(frac.numerator) + '_' + str(frac.denominator)
    name = ''
    sorted_params = dict(sorted(params.items()))
    for key, val in sorted_params.items():
        if not name == '': name += '_'
        name += key + frac_to_str(val)
    return name

def is_match(params:dict, params_fixed:dict):
    for key in params_fixed.keys():
        if params[key] != params_fixed[key]:
            return False
    return True

def to_fracs(arr:list[float]): #リスト内の有理数をFractionクラスに置き換える
    fracs =[]
    for val in arr:
        frac = Fraction(val).limit_denominator()
        fracs.append(frac)
    return fracs

if __name__ == '__main__':
    fracs = to_fracs([0,1/3,26/40,1])
    print(fracs)




