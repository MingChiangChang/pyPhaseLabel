import os
from pathlib import Path

import julia
from julia import Julia
sys_path = Path(os.environ["JULIA_SYS_IMG_PATH"]) / "sys.so"
Julia(sysimage=str(sys_path))

from julia import Pkg

Pkg.add(Pkg.PackageSpec(url = "https://github.com/MingChiangChang/CrystalShift.jl"))
Pkg.add(Pkg.PackageSpec(url = "https://github.com/MingChiangChang/CrystalTree.jl"))
Pkg.add("CovarianceFunctions")
Pkg.add("BackgroundSubtraction")
