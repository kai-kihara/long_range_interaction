from fractions import Fraction
import numpy as np
from func import *
#from simulator import * 
from analysis import *

def ucu(rho:Fraction):
    if rho == Fraction(0,1): return [False]
    elif rho == Fraction(1,1): return [True]
    else:
        rho1, rho2 = decompose_ucu(rho)
        return ucu(rho1) + ucu(rho2)

def decompose_ucu(rho:Fraction):
    if rho.denominator == 1: return rho
    fracs = farey_array(qmax=rho.denominator)
    for i in range(len(fracs)):
        if rho == fracs[i]: return fracs[i-1], fracs[i+1]

def ucu_list(rho:Fraction):
    f = rho
    d = rho.denominator
    ucus = [rho]
    while d > 1:
        rho1, rho2 = decompose_ucu(rho=f)
        if not rho1 in ucus: ucus.append(rho1)
        if not rho2 in ucus: ucus.append(rho2)
        if rho1.denominator > rho2.denominator: f = rho1
        else: f = rho2
        d = f.denominator
    return ucus


def is_adjacent(rho1:Fraction, rho2:Fraction)->bool: #2つの既約分数はファレイ数列で隣接するか
    if rho1.denominator*rho2.numerator - rho1.numerator*rho2.denominator == 1: return True
    else: return False

def is_combined(rho1:Fraction, rho2:Fraction, rho:Fraction)->bool: 
    if is_adjacent(rho1, rho2) and rho1 < rho and rho2 > rho: return True
    else: return False

def combine_ucu(pattern:list, i1:int):
    l = len(pattern)
    rho1:Fraction = pattern[i1]; rho2:Fraction = pattern[(i1+1)%l]
    rho_combined = Fraction(rho1.numerator+rho2.numerator, rho1.denominator+rho2.denominator)
    del pattern[i1]
    if (i1+1)%l == 0:
        del pattern[-1]
        pattern.insert(-1, rho_combined)
    else:
        del pattern[i1]
        pattern.insert(i1, rho_combined)


def scan_pattern(channel, rho:Fraction):
    pattern = []
    for i in range(len(channel)):
        if channel[i]: pattern.append(Fraction(1,1))
        else: pattern.append(Fraction(0,1))
    while True:
        for i in range(len(pattern)-1):
            rho1:Fraction = pattern[i]; rho2:Fraction = pattern[i+1]
            if is_combined(rho1, rho2, rho):
                combine_ucu(pattern=pattern, i1=i)
                break
        else: break
    while True:
        if is_combined(rho1=pattern[-1], rho2=pattern[0], rho=rho):
            combine_ucu(pattern=pattern, i1=-1)
            break
        elif is_combined(rho1=pattern[-2], rho2=pattern[-1], rho=rho):
            combine_ucu(pattern=pattern, i1=-2)
            break
        else: break
    return pattern

if __name__ == "__main__":
    pass
    # l = 1200
    # n = 500
    # arr = np.zeros(l, dtype=bool)
    # arr[np.random.choice(l, n, replace=False)] = True
    # print(scan_pattern(channel=arr, rho=Fraction(n,l)))
    # print(is_adjacent(Fraction(0,1), Fraction(1,1)))