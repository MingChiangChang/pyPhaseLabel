# A python wrapper of [CrystalShift.jl](https://github.com/MingChiangChang/CrystalShift.jl)

## Installation (only tested for Macs)
1. Install Julia
2. Clone this repo by
`git clone https://github.com/MingChiangChang/pyPhaseLabel`
3. Then do
```console
cd pyPhaseLabel
chmod 755 install.sh
./install.sh
```
The only part that can go wrong is when installing pyJulia. This can give error when the julia is not installed in default location. In such case, edit the install.sh at line 12 to:
`python -c 'import julia; julia.install(julia=$PATH_TO_JULIA_BINARY)'`

## Usage
After installation, you should be able to use the package as following
```console
$ python
>>> from pyPhaseLabel import evaluate_obj, optimize_phases, create_phases
>>>
```
 
These are also the main functions that you would be interfacing with.
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
