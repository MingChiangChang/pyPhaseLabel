import platform
from pathlib import Path
import numpy as np
from julia import Julia

_os = platform.system()
dir_path = Path( __file__ ).parent

if _os == "Linux" or _os == "Windows":
    Julia(sysimage=str(dir_path / "sys.so"))

from julia import Main 
from pathlib import Path

Main.include(str(dir_path / "python_mod.jl"))
Main.include(str(dir_path / "startup.jl"))

from julia.Main import CrystalPhase, Lorentz, PhaseModel, evaluate, optimize, PseudoVoigt

DEFAULT_TOL = 1E-5
METHOD_LST  = ["LM", "Newton"]
OBJ_LST     = ["LS", "KL"]

def create_phases(input_str: str, width_init: float, profile):
    """
    Create phases from the input file generated using ...script
    the profile should be a Profile object(Lorentz, PseudoVoight...)
    """
    input_list = input_str.split('#\n')
    return [CrystalPhase(input, width_init, profile) for input in input_list[:-1]]

def evaluate_phases(phase, x):
    y = np.zeros(x.shape)
    if phase is list:
       return evaluate(y, [PhaseModel(p) for p in phase], x) 
    else:
       return evaluate(y, PhaseModel(phase), x)

def evaluate_phasemodel(phasemodel, x):
    y = np.zeros(x.shape)
    return evaluate(y, phasemodel, x)

def evaluate_obj(obj, x):
    """
    evaluate_obj(obj: {CrystalPhase(s), PhaseModel(s), BackgroundModel}, x: np.array)

    This function can evaluate all custom objects in the module and reconstruct its pattern
    with the given x (which are array of Q values)
    It automatically handles single or list of object using Julia's multiple dispatch feature.
    """
    y = np.zeros(x.shape)
    return evaluate(y, obj, x)

def phasemodel(phases, background = None):
    """ Python-wrapped PhaseModel constructor"""
    return PhaseModel(phases, background)

def optimize_phase(phasemodels, x, y, 
                std_noise = .01, mean_θ = [1., 1., .2],
                std_θ = [1., .5, 5.],
                objective: str = "LS",
                method: str = "LM",
                maxiter: int = 32,
                regularization: bool = True,
                verbose: bool = False, tol: float = DEFAULT_TOL):
    """
    optimize_phase(phasemodels, x, y,
                std_noise: Real number, indicating the expected level of peak-to-noise ratio in this data
                mean_θ: Array of length three, represents the expected mean of [lattice shift, activation, peak_width]
                std_θ:  Array of length three, represents the expected std of [lattice shift, activation, peak_width]
                objective: fitting objective, can be either "LS" (least square) or "KL" (KL-divergence)
                method: fitting method, can be either "LM" (Levenberg method) or "Newton" (Saddle-free Newton) 
                maxiter: maximum number of iteration for optimization 
                regularization: boolean, whether regularize it  
                verbose: boolean, whether to print debug information 
                tol: float = DEFAULT_TOL)

    return: PhaseModel object (optimized)
    """
    assert method in METHOD_LST 
    assert objective in OBJ_LST
    return optimize(phasemodels, x, y, std_noise, mean_θ, std_θ,
              method=method, objective=objective, maxiter=maxiter, 
              regularization=regularization,
              verbose=verbose, tol=tol) 
