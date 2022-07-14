using CrystalShift
using CrystalShift: CrystalPhase, PhaseModel, optimize!, evaluate!, evaluate_residual!
using CrystalShift: OptimizationMethods
using CrystalTree
using CrystalTree: Lazytree, search!, search_k2n!
import CrystalShift: evaluate

DEFAULT_TOL = 1e-6

function optimize(phases::AbstractVector{CrystalPhase}, x::AbstractVector, y::AbstractVector,
                   std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
                   std_θ::AbstractVector = [1., Inf, 5.];
                   method::String="LM", objective::String = "LS",
                   maxiter::Int = 32,
                   regularization::Bool = true,
                   verbose::Bool = false, tol::Float64 =DEFAULT_TOL)
    method_enum = get_method_enum(method) 
    pm = PhaseModel(phases)
    pm = optimize!(pm, x, y, std_noise, mean_θ, std_θ, method=method_enum,
                objective=objective, maxiter=maxiter, regularization=regularization,
                verbose=verbose, tol=tol)
    return pm.CPs
end

function full_optimize(phases, x::AbstractVector, y::AbstractVector,
                   std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
                   std_θ::AbstractVector = [1., Inf, 5.];
                   method::String="LM", objective::String = "LS",
                   regularization::Bool = true,
                   loop_num::Int=8,
                   peak_shift_iter::Int = 32,
                   mod_peak_num::Int = 32,
                   peak_mod_mean::AbstractVector = [1.],
                   peak_mod_std::AbstractVector = [.5],
                   peak_mod_iter::Int=32,
                   verbose::Bool = false, tol::Float64 =DEFAULT_TOL)
    method_enum = get_method_enum(method)
    pm = full_optimize!(phases, x, y, std_noise, mean_θ, std_θ, method=method_enum,
                objective=objective, regularization=regularization,
		loop_num = loop_num,
                peak_shift_iter = peak_shift_iter,
                mod_peak_num = mod_peak_num,
                peak_mod_mean = peak_mod_mean,
                peak_mod_std = peak_mod_std,
                peak_mod_iter = peak_mod_iter,
                verbose=verbose, tol=tol)
    return pm
end


function get_method_enum(method_str::String)
    if method_str == "LM"
	    return LM
    elseif method_str =="Newton"
	    return Newton
    end
end

function optimize(pm::PhaseModel, x::AbstractVector, y::AbstractVector,
                std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
                std_θ::AbstractVector = [1., Inf, 5.];
                method::String = "LM", objective::String = "LS",
                maxiter::Int = 32,
                regularization::Bool = true,
                verbose::Bool = false, tol::Float64=DEFAULT_TOL)
    method_enum = get_method_enum(method)
    return optimize!(pm, x, y, std_noise, mean_θ, std_θ,
                method=method_enum, objective=objective, maxiter=maxiter,
                regularization=regularization, verbose=verbose,
                tol=tol)
end


evaluate(y, PM, x) = evaluate!(y, PM, x)

function evaluate(y::AbstractVector, PM::PhaseModel, x::AbstractVector)
    evaluate!(y, PM, x)
end

function evaluate(y::AbstractVector, PM::PhaseModel, θ::AbstractVector,
                   x::AbstractVector)
    evaluate!(y, PM, θ, x)
end

function evaluate_residual(PM::PhaseModel, θ::AbstractVector,
                            x::AbstractVector, r::AbstractVector)
    evaluate_residual!(PM, θ, x, y)
end

function evaluate_residual(PM::PhaseModel, x::AbstractVector, r::AbstractVector)
    evaluate_residual!(PM, x, r)
end

function search(LT::Lazytree, x::AbstractVector, y::AbstractVector, k::Int,
                 std_noise::Real, mean::AbstractVector, std::AbstractVector;
                maxiter = 32, regularization::Bool = true, tol::Real = DEFAULT_TOL)
    search!(LT, x, y, k, std_noise, mean, std, maxiter=maxiter, regularization=regularization, tol=tol)
end

function search_k2n(LT::Lazytree, x::AbstractVector, y::AbstractVector, k::Int,
                    std_noise::Real, mean::AbstractVector, std::AbstractVector;
                maxiter = 32, regularization::Bool = true, tol::Real = DEFAULT_TO)
    search_k2n!(LT, x, y, k, std_noise, mean, std, maxiter=maxiter, regularization=regularization, tol=tol)
end
