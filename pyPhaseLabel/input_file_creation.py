from pathlib import Path, PurePath

from cif_to_input_file import cif_to_input

home = Path.home()

path = home / 'Downloads' / 'cifs'
cif = list(path.glob('*.cif'))

cif_to_input(cif, PurePath(), (0,66))
