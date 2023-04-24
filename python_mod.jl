using CrystalShift
using CrystalShift: CrystalPhase, PhaseModel, optimize!, evaluate!, evaluate_residual!
using CrystalShift: OptimizationMethods, optimize_with_uncertainty!
using CrystalTree
using CrystalTree: Lazytree, search!, search_k2n!
import CrystalShift: evaluate

DEFAULT_TOL = 1e-6

function optimize(phases::AbstractVector{CrystalPhase}, x::AbstractVector, y::AbstractVector,
                   std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
                   std_θ::AbstractVector = [1., Inf, 5.];
                   method::String="LM", objective::String = "LS",
		   optimize_mode::String="Simple",
                   maxiter::Int = 32,
                   regularization::Bool = true,
                   verbose::Bool = false, tol::Float64 =DEFAULT_TOL)
    method_enum = get_method_enum(method) 
    optimize_mode_enum = get_optimize_mode_enum(optimize_mode)
    pm = PhaseModel(phases)
    pm = optimize!(pm, x, y, std_noise, mean_θ, std_θ, method=method_enum,
                objective=objective, optimize_mode=optimization_mode_enum,
		maxiter=maxiter, regularization=regularization,
                verbose=verbose, tol=tol)
    return pm.CPs
end

#function optimize_with_uncertainty(phases::Any,
#		   x::AbstractVector, y::AbstractVector,
#                   std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
#                   std_θ::AbstractVector = [1., Inf, 5.];
#                   method::String="LM", objective::String = "LS",
#		   optimize_mode::String="Simple",
#                   maxiter::Int = 32,
#                   regularization::Bool = true,
#                   verbose::Bool = false, tol::Float64 =DEFAULT_TOL)
#    method_enum = get_method_enum(method)
#    optimize_mode_enum = get_optimize_mode_enum(optimize_mode)
#    pm, uncer = optimize_with_uncertainty!(phases, x, y,
#				    std_noise, mean_θ, std_θ,
#				    method=method_enum,
#                                    objective=objective,
#				    optimize_mode=optimize_mode_enum,
#				    maxiter=maxiter,
#				    regularization=regularization,
#                                    verbose=verbose,
#				    tol=tol)
#    return pm, uncer
#end

function full_optimize(phases, x::AbstractVector, y::AbstractVector,
                   std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
                   std_θ::AbstractVector = [1., Inf, 5.];
                   method::String="LM", objective::String = "LS",
		   optimize_mode::String="Simple",
                   regularization::Bool = true,
                   loop_num::Int=8,
                   peak_shift_iter::Int = 32,
                   mod_peak_num::Int = 32,
                   peak_mod_mean::AbstractVector = [1.],
                   peak_mod_std::AbstractVector = [.5],
                   peak_mod_iter::Int=32,
                   verbose::Bool = false, tol::Float64 =DEFAULT_TOL)
    method_enum = get_method_enum(method)
    optimize_mode_enum = get_optimize_mode_enum(optimize_mode)
    pm = full_optimize!(phases, x, y, std_noise, mean_θ, std_θ, method=method_enum,
                objective=objective, regularization=regularization,
		optimize_mode=optimize_mode_enum,
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

# TODO: Should be able to generate this with metaprogramming
function get_optimize_mode_enum(optimize_mode_str::String)
    if optimize_mode_str == "Simple"
        return Simple
    elseif optimize_mode_str == "EM"
        return EM
    elseif optimize_mode_str == "WithUncer"
        return WithUncer
    end
end

function optimize(pm::PhaseModel, x::AbstractVector, y::AbstractVector,
                std_noise::Real, mean_θ::AbstractVector = [1., 1., .2],
                std_θ::AbstractVector = [1., Inf, 5.];
                method::String = "LM", objective::String = "LS",
		optimize_mode::String = "Simple",
                maxiter::Int = 32,
                regularization::Bool = true,
                verbose::Bool = false, tol::Float64=DEFAULT_TOL)
    method_enum = get_method_enum(method)
    optimize_mode_enum = get_optimize_mode_enum(optimize_mode)
    return optimize!(pm, x, y, std_noise, mean_θ, std_θ,
                method=method_enum, objective=objective,
		optimize_mode=optimize_mode_enum,
		maxiter=maxiter,
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

const search_k2n = search_k2n!
function search(LT::Lazytree, x::AbstractVector, y::AbstractVector,
                 depth::Integer=3, k::Integer=3,
		 normalization_constant::Real=.1,
		 amorphous::Bool=false,
		 background::Bool=false,
		 background_length::Real=8.,
		 std_noise::Real=0.05, mean::AbstractVector=[1., .5, .2],
		 std::AbstractVector=[0.05, 0.05, 0.05];
                 method::String = "LM", objective::String = "LS",
                 optimize_mode::String = "Simple", em_loop_num::Integer =8,
                 maxiter::Integer = 32, regularization::Bool = true,
		 verbose::Bool = false, tol::Real = DEFAULT_TOL)
    method_enum = get_method_enum(method)
    optimize_mode_enum = get_optimize_mode_enum(optimize_mode)
    search!(LT, x, y, depth, k, normalization_constant, amorphous,
            background, background_length,
            std_noise, mean, std,
            method=method_enum, objective=objective, optimize_mode=optimize_mode_enum,
            em_loop_num=em_loop_num, maxiter=maxiter, regularization=regularization,
            verbose=verbose, tol=tol)
end
#function search(LT::Lazytree, x::AbstractVector, y::AbstractVector, k::Int,
#                 std_noise::Real, mean::AbstractVector, std::AbstractVector;
#                maxiter = 32, regularization::Bool = true, tol::Real = DEFAULT_TOL)
#    search!(LT, x, y, k, std_noise, mean, std, maxiter=maxiter, regularization=regularization, tol=tol)
#end

#function search_k2n(LT::Lazytree, x::AbstractVector, y::AbstractVector, k::Int,
#                    std_noise::Real, mean::AbstractVector, std::AbstractVector;
#                maxiter = 32, regularization::Bool = true, tol::Real = DEFAULT_TO)
#    search_k2n!(LT, x, y, k, std_noise, mean, std, maxiter=maxiter, regularization=regularization, tol=tol)
#end
