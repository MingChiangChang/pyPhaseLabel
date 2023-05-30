from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from pyPhaseLabel import PhaseModel, CrystalPhase, EQ, BackgroundModel
from pyPhaseLabel import create_phases, evaluate_obj, optimize_phase, Lorentz, PseudoVoigt 

with open(Path(__file__).parent / 'sticks.csv', 'r') as f:
    t = f.read()

phases = create_phases(t, 0.1, PseudoVoigt(0.5))
for idx, phase in enumerate(phases):
    print(idx, phase.name)

x = np.linspace(6, 55, 1024)
y = np.zeros(1024)
new_phase = CrystalPhase(phases[2], [4.5, 1.0, 0.15, 0.4])
t = evaluate_obj(phases[2], x) 


test_data = (evaluate_obj(new_phase, x) 
             + 0.2*np.sin(x/10) 
             + 0.1*np.random.randn(1024)+0.2)
bg = BackgroundModel(x, EQ(), 20, 100)
p = PhaseModel(phases[2], bg)
pm, uncer = optimize_phase(p, x, test_data, maxiter=512, optimize_mode="WithUncer",
        verbose=True)
print(f"uncer: {uncer}")
plt.plot(x, t, label="Original Phase")
plt.plot(x, test_data, label="Test data")
plt.plot(x, evaluate_obj(pm, x), label="Optimized result", linewidth=3)
plt.plot(x, evaluate_obj(pm.background, x), label="Fitted background")
plt.legend()
plt.xlabel("q ($nm^{-1}$)")
plt.ylabel("(a.u.)")
plt.show()

from julia.Main import get_fraction
print(get_fraction(phases[1:3]))
