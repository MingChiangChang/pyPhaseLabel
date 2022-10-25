import os
from multiprocessing import cpu_count
os.environ["JULIA_NUM_THREADS"] = str(cpu_count())


from .wrapper import evaluate_obj, optimize_phase, create_phases, fit_amorphous, optimize_all

from julia.Main import CrystalPhase, PhaseModel, BackgroundModel, EQ, Wildcard # Important structs 
from julia.Main import Lorentz, Gauss, PseudoVoigt, FixedPseudoVoigt           # Peak Profile objects 
from julia.Main import FixedBackground

