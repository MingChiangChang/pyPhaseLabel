import os
import platform
from pathlib import Path
import numpy as np
from julia import Julia

_os = platform.system()
package_path = Path(__file__).parent
dir_path = Path(os.environ["JULIA_SYS_IMG_PATH"])

Julia(sysimage=str(dir_path / "sys.so"))

from julia import Main 
from pathlib import Path

Main.include(str(package_path / "python_mod.jl"))
Main.include(str(package_path / "startup.jl"))

from julia.Main import CrystalPhase, Lorentz, PhaseModel, evaluate
from julia.Main import optimize, PseudoVoigt, full_optimize
from julia.Main import get_fraction

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
                optimize_mode: str = "Simple",   
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
                optimize_mode: Simple does normal refinement,
                               EM uses expectation maximization to estimate std_noise,
                               WithUncer gives uncertainty estimates
                maxiter: maximum number of iteration for optimization 
                regularization: boolean, whether regularize it  
                verbose: boolean, whether to print debug information 
                tol: float = DEFAULT_TOL)

    return: PhaseModel object (optimized)
    """
    assert method in METHOD_LST 
    assert objective in OBJ_LST
    return optimize(phasemodels, x, y, std_noise, mean_θ, std_θ,
                method=method, objective=objective, optimize_mode=optimize_mode,
                maxiter=maxiter, 
                regularization=regularization,
                verbose=verbose, tol=tol) 

def fit_amorphous(wildcard, background, x, y,
                  std_noise: float = .01,
                  objective: str = "LS",
                  method: str = "LM",
                  maxiter: int = 32,
                  regularization: bool = True,
                  verbose: bool = False,
                  tol: float = DEFAULT_TOL):
    '''
    This function assumes that amorphous are formed by wildcard phase that has few wide week peaks and
    a smooth background.


    '''
    pm = PhaseModel(wildcard, background)
    opt_pm = optimize_phase(pm, x, y, std_noise, [1., 1., 1.], [1., 1., 1.], objective,
                            method=method, maxiter=maxiter, regularization=regularization,
                            verbose=verbose, tol=tol)
    return opt_pm 


def optimize_all(phases, x, y, std_noise, mean_θ, std_θ,
                 objective: str = "LS",
                 method: str = "LM",
                 optimize_mode: str = "Simple",
                 regularization: bool = True,
                 loop_num: int=8,
                 peak_shift_iter: int = 32,
                 mod_peak_num: int = 32,
                 peak_mod_mean = [1.],
                 peak_mod_std = [.5],
                 peak_mod_iter:int =32,
                 verbose: bool = False,
                 tol: float = DEFAULT_TOL):
    assert method in METHOD_LST
    assert objective in OBJ_LST
    return full_optimize(phases, x, y, std_noise, mean_θ, std_θ,
              method=method, objective=objective,
              regularization=regularization,
              optimize_mode=optimize_mode,
              loop_num=loop_num,
              mod_peak_num = mod_peak_num,
              peak_mod_mean = peak_mod_mean,
              peak_mod_std = peak_mod_std,
              peak_mod_iter = peak_mod_iter,
              verbose=verbose, tol=tol)
