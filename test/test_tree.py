import numpy as np
import matplotlib.pyplot as plt

from pyPhaseLabel import PhaseModel, CrystalPhase, EQ, BackgroundModel, FixedPseudoVoigt
from pyPhaseLabel import create_phases, evaluate_obj, optimize_phase, Lorentz, PseudoVoigt
from julia.Main import Wildcard, Lazytree, search, get_probabilities, get_fraction

std_noise = .01
mean_θ = [1., 1., .2]
std_θ = [.5, .5, 1.]

with open('../sticks.csv', 'r') as f:
    t = f.read()
tt = t.split("#\n")
tt.remove("")

phases = create_phases(t, .5, FixedPseudoVoigt(0.1))
x = np.linspace(15, 55, 1024)

tree = Lazytree(phases[:4], x)

y = evaluate_obj(phases[1:4], x)
#plt.plot(x, y)
#plt.show()

result = search(tree, x, y, 3, 3, .1, False, False, 0.5,
                std_noise, mean_θ, std_θ,
                maxiter=128, regularization=True)

results = [r for subresults in result[1:] for r in subresults]
t = get_probabilities(results, x, y, std_noise, mean_θ, std_θ) 
ind = np.argmax(t)
print(get_fraction(results[ind].phase_model.CPs))

#for idx, node in enumerate(results):
#    # a = [np.linalg.norm(evaluate_obj(n.phase_model, x)-y) for n in node]
#    # ind = np.argmin(a)
#    plt.plot(x, evaluate_obj(node.phase_model, x))
#    plt.plot(x, y)
#    plt.title(f"Probability {t[idx]}")
#    plt.show()
