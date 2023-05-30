#!/bin/bash

# Add package path to site-package (remember to be in virtualenv if you usually work in it
# echo "Adding package path to python site-package..."
# SITEDIR=$(python -c 'import site; print(site.getsitepackages()[0])')
# CUR_PATH=$(pwd)
# echo "$(dirname "$CUR_PATH")" > "$SITEDIR/somelib.pth"

# Install pyJulia
echo "Installing PyJulia..."
cd ..
git clone https://github.com/JuliaPy/pyjulia
cd pyjulia
pip install .
cd ../pyPhaseLabel 
python -c 'import julia; julia.install()'
python3 -m julia.sysimage sys.so

# Install Required packages
echo "Install Required Packages.."
python pyPhaseLabel/install.py
