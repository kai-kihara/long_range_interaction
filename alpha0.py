from simulator import *
from params import SystemParams
import func

import matplotlib.pyplot as plt

rhos = func.to_fracs([1/i for i in range(2,6)])
alphas = func.to_fracs([0.01*i for i in range(1,201)])
system_params = SystemParams(L=1200, t_max=1, dt=1)

for rho in rhos:
    dEs = []
    for alpha in alphas:
        params = {"rho":rho, "beta":0, "alpha":alpha, "K":1}
        simulator = Simulator(params=params, system_params=system_params, options=[])
        simulator.initial_setting()
        dE = simulator.potential_change(i=system_params.L-1, d=1)
        dEs.append(dE)
    plt.plot(alphas, dEs, label=r"$\rho=$"+str(rho))
plt.legend()
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$U_{\rm int}$")
plt.savefig("tmp", dpi=300)
