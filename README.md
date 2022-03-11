# A python wrapper of [CrystalShift.jl](https://github.com/MingChiangChang/CrystalShift.jl)
Currently only support Linux and Macs. Window installation is under testing.
## Installation (tested for Linux and Macs)
1. Install Julia
Add julia to path by adding this line in `~/.bashrc` (for linux/mac)
```console
export PATH="$PATH:path/to/julia/folder/bin"
```
where `path/to/julia/folder` is where you put the extracted julia folder (likely `/usr/local/bin/julia-$version/`)

2. Clone this repo by
`git clone https://github.com/MingChiangChang/pyPhaseLabel`
3. Then do
```console
cd pyPhaseLabel
chmod 755 install.sh
./install.sh
```
The only part that can go wrong is when installing pyJulia. This can give error when the julia is not installed in default location. In such case, edit the install.sh at line 16 to:
```
python -c 'import julia; julia.install(julia=$PATH_TO_JULIA_BINARY)'
```

## Usage
After installation, you should be able to use the package as following
```console
$ python
>>> from pyPhaseLabel import evaluate_obj, optimize_phases, create_phases
>>>
```
### Generate input files
The algorithm take a candidate phase and try to optimize it to fit a pattern by modifying its lattice parameters without changing the symmetry. The `cif_to_input_file.py` takes a list of cif file paths and generate a `sticks.csv` input file that contains the necessary information for the optimization. The `create_phases` function can take this input file and generate an array of `CrystalPhase` object.
 
Next, these are also the main functions that you would be interfacing with.
### Custom objects
- `CrystalPhase` contains the lattice information and a list of peak indices and intensities that is required to simulate the x-ray diffraction pattern. The optimization will optimize the lattice parameters under the assumption that no symmetry is broken.
- `BackgroundModel` uses the q value and a kernel function (see allowed list in [CovariaceFunctions.jl](https://github.com/SebastianAment/CovarianceFunctions.jl)) to simulate the background. EQ (exponential quadratic) is usually a good starting point.
- `PhaseModel` wraps an array of `CrystalPhase` and a optional `BackgroundModel` into a object that can be optimized together to fit the given spectrum.

### Functions
- `create_phases` create `CrystalPhase` objects from a given input file.
- `evaluate_obj` evaluates custom objects and return the reconstructed x-ray pattern.
- `optimize_phases` takes a `PhaseModel` object, q vector, the given pattern and other parameters (see code comments) as input. It optimize the lattice parameters and the background to get an optimal result with the given error metric.


## Example
This is the output of the `example.py`

![Example](example.png)

As you can see from the figure, this code can fit the lattice distortion while fitting the background at once.
