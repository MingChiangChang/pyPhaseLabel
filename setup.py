from setuptools import setup, find_packages

setup(
    name='pyPhaseLabel',
    version='0.0.1',
    description='Python wrapper for CrystalShift.jl and CrystalTree.jl',
    author='Ming-Chiang Chang',
    author_email='mc2663@cornell.edu',
    python_requires='>=3.6.0',
    url='http://github.com/mingchianghchang/pyPhaseLabel',
    packages=find_packages(),
    include_package_data=True,
    package_data={'':['*.jl']},
    install_requires=['numpy', 'matplotlib', 'julia', 'pymatgen', 'xrayutilities']
)
