import julia

from julia import Pkg

Pkg.add(Pkg.PackageSpec(url = "https://github.com/MingChiangChang/CrystalShift.jl"))
Pkg.add("CovarianceFunctions")
