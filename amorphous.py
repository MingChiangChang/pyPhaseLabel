import numpy as np
import matplotlib.pyplot as plt
import time

import pyPhaseLabel
from pyPhaseLabel import Lorentz, fit_amorphous, Lorentz, EQ, BackgroundModel, evaluate_obj
from pyPhaseLabel import Gauss, Wildcard

q = np.load("data/test_q.npy")
y = np.load("data/test_int.npy")

y /= np.max(y)*2

w  = Wildcard([10., 19.], [1., 1.], [2., 1.], "amorphous", Lorentz(),  [1., 1., 1., 1., 1., 1.])
bg = BackgroundModel(q, EQ(), 15, rank_tol=1E-3)

start = time.time()
opt_pm = fit_amorphous(None, bg, q, y, maxiter=256)
print(time.time() - start)
plt.plot(q, y)
plt.plot(q, evaluate_obj(opt_pm, q))
plt.show()
