from simulator import *
from merge_data import *
from analysis import *
from func import *

import numpy as np
import matplotlib.pyplot as plt

results:Results = load_pickle(file_name="fitting.pkl", directory_path="data")
betas = to_fracs([i for i in range(200,241)])
MSEs = []
qmax = 4

for beta in betas:
    SEs = []
    for sim_data in results.data:
        sim_data:SimulationData
        if sim_data.params["beta"] == beta:
            Jth = approx_ssep(qmax=qmax, rho=sim_data.params["rho"])
            SE = (np.mean(sim_data.values["hop_rate"])-Jth)**2
            SEs.append(SE)
            if beta == Fraction(60,1): print(sim_data.params["rho"], Jth, SE)
    MSE = np.mean(SEs)
    MSEs.append(MSE)

plt.plot(betas, MSEs)
plt.savefig("tmp.png")




