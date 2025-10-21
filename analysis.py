from scipy.special import digamma, zeta
import numpy as np
import math
import heapq
import matplotlib.pyplot as plt
from fractions import Fraction
import neighbor_approximation as na

#from simulator import *

def dE(n):
    return -1 + 2*digamma(1)/n - 2/n*digamma(1/n) - np.pi/n/np.tan(np.pi/n)

def q_max(beta:float)->int:
    inf_betas = [0,200]
    for inf_qmax, inf_beta in enumerate(inf_betas):
        if beta < inf_beta:
            return inf_qmax

def irreducible(m, n):
    if m == 1: return True
    for k in range(2,m+1):
        if m%k==0 and n%k==0:
            return False
    return True

def dE_limit(n):
    return 2 * zeta(3) / n**3

def farey_array(qmax:int, half:bool=False):
    nodes = [Fraction(0,1)]
    if not half: nodes.append(Fraction(1,1))
    for n in range(1,qmax+1):
        for m in range(1,n):
            if irreducible(m,n) and ((not half) or 2*m<=n):
                nodes.append(Fraction(m,n))
    sorted_nodes = sorted(nodes)
    return sorted_nodes

def approx_fdiagram(qmax:int):
    nodes = farey_array(qmax=qmax)
    rhos = [0]
    hoprates = [0]
    for i in range(1,len(nodes)):
        rho1 = nodes[i-1]; rho2 = nodes[i]
        rho = np.linspace(rho1, rho2, 100)[1:] #重複しないようにm1/n1は含めない
        p, L_normalized = calc_scale_factor(rho1=rho1, rho2=rho2, rho=rho)
        hoprate = L_normalized*p*(1-p)
        rhos += rho.tolist(); hoprates += hoprate.tolist()
    return rhos, hoprates

def approx_ssep(qmax:int, rho:Fraction):
    rho1, rho2 = select_sub_pattern(rho=rho, qmax=qmax)
    p, ld = calc_scale_factor(rho1=rho1, rho2=rho2, rho=rho)
    return ld*p*(1-p)

def select_sub_pattern(rho:Fraction, qmax:int)->tuple[Fraction,Fraction]:
    fs = farey_array(qmax=qmax)
    for i in range(0,len(fs)-1):
        rho1:Fraction = fs[i]; rho2:Fraction = fs[i+1]
        if rho1<rho and rho<rho2:
            return (rho1, rho2)
        elif rho1 == rho or rho2 == rho:
            return (rho, rho)

def calc_scale_factor(rho1:Fraction, rho2:Fraction, rho:Fraction)->tuple[float,float]:
    q1 = rho1.denominator; r1 = rho1.numerator
    q2 = rho2.denominator; r2 = rho2.numerator
    if rho1 == rho2: p = 1 #rho1に統一
    else: p = (r2-rho*q2)/(rho*(q1-q2)-(r1-r2))
    ld = 1/(p*q1+(1-p)*q2)
    return p, ld

def simplify_fraction(frac):
    gcd = math.gcd(frac[0], frac[1])
    return Fraction(round(frac[0]/gcd), round(frac[1]/gcd))


def UCU_neighbor_each(beta:float, rho:Fraction)->float:
    qmax = q_max(beta)
    rho1, rho2 = select_sub_pattern(rho,qmax)
    #if rho1 == rho2: return 0
    if qmax == 1: rho_break = 0
    elif qmax == rho1.denominator: rho_break = 1
    elif qmax == rho2.denominator: rho_break = 2
    else: rho_break = 0
    p, ld = calc_scale_factor(rho1, rho2, rho) #pはrho1の割合
    l = 600
    if p > 0.5:n = round(l*(1-p))
    else:
        n = round(l*p)
        if rho_break > 0: rho_break = rho_break%2 + 1
    J_break = 2*math.exp(-beta*dE(qmax)/2)
    J = na.hop_rate_with_err(l=l,n=n,dE=dE(rho1.denominator+rho2.denominator),beta=beta,num=rho_break,J_break=J_break)*ld
    return J

def UCU_neighbor(beta:float, qmax:int)->float:
    fs = farey_array(qmax=qmax)
    l_tot = 600
    # l = 500
    # dnum:int = 100
    # ns = [round(l/dnum)*i for i in range(dnum)]
    rhos = []
    Js = []
    for i in range(len(fs)-1):
        rho1 = fs[i]; rho2 = fs[i+1]
        q = rho1.denominator + rho2.denominator
        ns = [rho1.denominator*i for i in range(round(l_tot/rho2.denominator/rho1.denominator))] #rho2の個数
        rhoqmax = 0
        if qmax == 1: rhoqmax = 0
        elif qmax == rho1.denominator: rhoqmax = 1
        elif qmax == rho2.denominator: rhoqmax = 2
        for n in ns:
            l = n + round((l_tot - n*rho2.denominator)/rho1.denominator)
            rhot = Fraction(l-n,l) #rho1の割合
            ld = 1/(rhot*rho1.denominator+(1-rhot)*rho2.denominator) #粗視化率
            J_break = 2*math.exp(-beta*dE(qmax)/2)
            if 2*n > l:
                n_dash = l - n
                if rhoqmax == 2: UCU_broken = 1
                elif rhoqmax == 1: UCU_broken = 2
            else: n_dash = n; UCU_broken = rhoqmax
            #if UCU_broken > 0: print(UCU_broken, rho1, rho2)
            dU = dE(q)
            #dU = 1/(q-1)-1/q
            #J = na.hop_rate(l=l,n=n_dash,dE=dU, beta=beta) * ld# + ld * rhoqmax * 2 * np.exp(-beta*dE(n=qmax)/2)
            J = na.hop_rate_with_err(l=l,n=n_dash,dE=dU,beta=beta,num=UCU_broken,J_break=J_break)*ld
            rho = (rhot*rho1.numerator+(1-rhot)*rho2.numerator)/(rhot*rho1.denominator+(1-rhot)*rho2.denominator)
            Js.append(J)
            rhos.append(rho)
            #print(n,l,rho1,rho2)
    rhos.append(1); Js.append(0)
    return rhos, Js

def adjacent_rate(rho:Fraction, qmax:int, beta_range:tuple):
    l = 600
    n = round(rho*l)
    rho1, rho2 = select_sub_pattern(rho=rho, qmax=qmax)
    rs = []
    betas = list(range(beta_range[0], beta_range[1]+1))
    for beta in betas:
        r = na.adjacent_rate(l,n,0.5,beta)#dE(rho1.denominator+rho2.denominator)+2*np.log(2)-4/3,beta)
        rs.append(r)
    return betas, rs


if __name__ == '__main__':
    print(dE(1))


    