import numpy as np
import matplotlib.pyplot as plt
import time

import pyPhaseLabel
from pyPhaseLabel import Lorentz, fit_amorphous, Lorentz, EQ, BackgroundModel, evaluate_obj
from pyPhaseLabel import Gauss, Wildcard, optimize_phase, PhaseModel

q = np.load("data/test_q.npy")
y = np.load("data/test_int.npy")

y /= np.max(y)*2

w  = Wildcard([19., 40.], [.1, .05], [1., 1.], "amorphous", Gauss(),
        [.05, .05, .1, .1, .1, .1])
bg = BackgroundModel(q, EQ(), 25, 0, rank_tol=1E-3)

start = time.time()
#opt_pm = optimize_phase(pm, q, y, maxiter=1024)
opt_pm = fit_amorphous(w, bg, q, y, maxiter=1024)
print(opt_pm.wildcard)
print(time.time() - start)
plt.plot(q, y)
plt.plot(q, evaluate_obj(opt_pm, q))
plt.plot(q, evaluate_obj(opt_pm.background, q), label="Background")
plt.plot(q, evaluate_obj(opt_pm.wildcard, q), label="Wildcard")
plt.legend()
plt.show()
