from scipy.special import hyp2f1, comb
import math
import matplotlib.pyplot as plt

def distribution_function(l:int,n:int,k:float)->float: #なぜか2n>lで動作しない
    z = l/n*comb(l-n-1,n-1)*hyp2f1(1-n,-n,l-2*n+1,math.exp(-k))
    return z

def weight_c(l:int,n:int,k:float,c:int)->float:
    return comb(n-1, n-1-c)*comb(l-n-1,n-1-c)*math.exp(-k*c)*l/(n-c)

def hop_weight_c(l:int,n:int,k:float,c:int)->float:
    return comb(n-2, n-2-c)*comb(l-n-2,n-2-c)*(2*math.exp(-k/2)+(l-2)/(n-c-1)-2)*math.exp(-k*c)

def hop_rate(l:int,n:int,dE:float,beta:float)->float:
    if n == 0 or n == l: return 0
    elif n == 1: return n/l
    k = beta*dE
    s = 0
    for c in range(n-1): s += hop_weight_c(l=l,n=n,k=k,c=c)
    return s/distribution_function(l,n,k)

def hop_rate_with_err(l:int,n:int,dE:float,beta:float,num:int,J_break:float) ->float: #num=1->粒子がbreakする, num=2->空セルがbreakする
    #nはrho2の数
    k = beta*dE
    s = 0
    #J_break = 2*ld*math.exp(-beta*dE(1/ld)/2)
    if n == 0:
        if num == 1: return J_break
        else: return 0
    elif n == l: 
        if num == 2: return J_break
        else: return 0
    elif n == 1:
        if num == 1: return 1/l + (l-1)/l*J_break
        else: return 1/l
    for c in range(n-1):
        s += hop_weight_c(l=l,n=n,k=k,c=c)
        if num == 1: s += max(0,l-2*n+c)/l*J_break*weight_c(l,n,k,c)
        elif num == 2: s += c/l*J_break*weight_c(l,n,k,c)
    return s/distribution_function(l,n,k)

def adjacent_rate(l:int,n:int,dE:float,beta:float)->float:
    k = beta*dE
    return math.exp(-k)*comb(l-n-1,n-2)*hyp2f1(1-n,2-n,l-2*n+2,math.exp(-k))/distribution_function(l,n,k)*l/n


if __name__ == "__main__":
    l = 50
    n = 30
    print(hop_rate(l,n,0.3,10))
    