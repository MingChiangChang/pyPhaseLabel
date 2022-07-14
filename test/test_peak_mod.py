import numpy as np
import matplotlib.pyplot as plt

from pyPhaseLabel import PhaseModel, CrystalPhase, EQ, BackgroundModel, FixedPseudoVoigt
from pyPhaseLabel import create_phases, evaluate_obj, optimize_phase, Lorentz, PseudoVoigt
from pyPhaseLabel import optimize_all
from julia.Main import Wildcard, Lazytree, search, get_free_params, PeakModCP

std_noise = .01
mean_θ = [1., 1., .2]
std_θ = [.5, .5, 1.]

with open('../sticks.csv', 'r') as f:
    t = f.read()
tt = t.split("#\n")
tt.remove("")
x = np.linspace(8, 60, 512)
phases = create_phases(t, .5, FixedPseudoVoigt(0.1))

pmcp = PeakModCP(phases[1], x, 10)
pmcp = PeakModCP(pmcp, (0.5+0.5*np.random.rand(10))*get_free_params(pmcp))

test_data = evaluate_obj(pmcp, x)
t = optimize_all(phases[1:2], x, test_data, std_noise, mean_θ, std_θ)

plt.plot(x, evaluate_obj(t, x))
plt.plot(x, test_data) 
plt.show()
