#!/bin/bash

# Add package path to site-package (remember to be in virtualenv if you usually work in it
echo "Adding package path to python site-package..."
SITEDIR=$(python -c 'import site; print(site.getsitepackages()[0])')
CUR_PATH=$(pwd)
echo "$(dirname "$CUR_PATH")" > "$SITEDIR/somelib.pth"

# Install pyJulia
echo "Installing PyJulia..."
python3 -m pip install --user julia
python -c 'import julia; julia.install()'

# Install Required packages
echo "Install Required Packages.."
python install.py
