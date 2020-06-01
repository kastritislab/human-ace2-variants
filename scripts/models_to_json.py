"""
Recursively searches a folder for PDB files produced
by HADDOCK and creates a JSON file with some properties.

Useful together with a templating language to build
tables.
"""

import argparse
import json
import pathlib


def read_args():
	"""Read arguments from CLI"""

	ap = argparse.ArgumentParser(description=__doc__)
	ap.add_argument(
		'rootdir',
		type=pathlib.Path,
		help='Top-level folder to search for PDB files.'
	)
	ap.add_argument(
		'-o',
		'--output',
		default=pathlib.Path('models.json'),
		type=pathlib.Path,
		help='Output file name'
	)

	return ap.parse_args()


def collect_models(rootdir):
	"""Returns a list of model paths found in rootdir"""

	suffixes = set(['.pdb'])

	fullpath = rootdir.resolve(strict=True)

	for fpath in fullpath.rglob('*'):
		if 'template' in str(fpath):
			continue

		if fpath.suffix in suffixes:
			yield fpath.resolve(strict=True)


def str_to_float(v):
	return round(float(v), 2)


def process_models(pathlist):
	"""Parses information from PDB files into a dictionary."""

	jsonlist = []

	for model in pathlist:
		modeldict = {}
		modeldict['url'] = f'{model.parent.stem}/{model.name}'
		modeldict['name'] = model.stem
		modeldict['dataset'] = model.parent.stem

		with model.open('rt') as structure:
			for line in structure:
				line = line.strip()

				if line.startswith('REMARK energies:'):
					sep = line.index(':') + 1
					fields = list(map(str_to_float, line[sep:].split(',')))
					modeldict['e_vdw'] = fields[5]
					modeldict['e_elec'] = fields[6]

				elif line.startswith('REMARK Desolvation energy:'):
					sep = line.index(':') + 1
					modeldict['e_desolv'] = str_to_float(line[sep:])

				elif line.startswith('REMARK buried surface area:'):
					sep = line.index(':') + 1
					modeldict['buried_surf_area'] = str_to_float(line[sep:])

		# Calculate HS
		score = 1.0*modeldict.get('e_vdw', 0) + \
				0.2*modeldict.get('e_elec', 0) + \
				1.0*modeldict.get('e_desolv', 0)

		modeldict['haddock_score'] = str_to_float(score)
		jsonlist.append(modeldict)

	return jsonlist

if __name__ == '__main__':

	args = read_args()
	models = collect_models(args.rootdir)

	with args.output.open('wt') as handle:
		json.dump(
			process_models(models),
			handle,
			indent=4
		)
