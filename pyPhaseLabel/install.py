import julia
from julia import Julia
Julia(sysimage="sys.so")

from julia import Pkg

Pkg.add(Pkg.PackageSpec(url = "https://github.com/MingChiangChang/CrystalShift.jl"))
Pkg.add(Pkg.PackageSpec(url = "https://github.com/MingChiangChang/CrystalTree.jl"))
Pkg.add("CovarianceFunctions")
