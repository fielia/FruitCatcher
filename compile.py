'''
Analyzes relative python imports and compiles them into a single file.
Written by Jadon L. (@koerismo)
Licensed under CC-BY 4.0
'''

from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser('compiler', 'Analyzes relative python imports and compiles them into a single file.')
parser.add_argument('-i', '--input', help='The root input file.', type=str, required=True)
parser.add_argument('-o', '--output', help='The target output file.', type=str, required=True)
parser.add_argument('--trace', help='Allow intercepting error traceback messages.', action='store_true')
args = parser.parse_args()

DEFINE = '__define__'
ROOT = '__root__'
TRACE_IMPORTS = 'from io import StringIO\nfrom sys import print_exception\nfrom re import match\nfrom sys import exit\n'
HEADER = f'''# Packed by compile.py
{TRACE_IMPORTS if args.trace else ''}
__ModuleCache__ = {{}}
class __ModuleNamespace__():
	def __init__(self, kwargs):
		for name in kwargs:
			setattr(self, name, kwargs[name])
	def __contains__(self, key):
		return key in self.__dict__
	def __iter__(self):
		return self.__dict__.__iter__()
'''

def compile():

	compiled_modules = []
	compiled_module_set = set()

	def moduleify(path: Path, name_override: str|None=None):
		''' Creates a module from a file. '''
		print('Including module', path)

		module_name = str(path.with_suffix('')).replace('/', '_').replace('\\', '_')
		module_dir = path.parent
		module_classes = []
		out = f'def {DEFINE}{module_name}():\n'

		out += f'\tif "{module_name}" in __ModuleCache__: return __ModuleCache__["{module_name}"]\n'
		
		if name_override: out += f'\t__name__ = "{name_override}"\n'
		else: out += f'\t__name__ = "__{module_name}__"\n'

		if not path.exists():
			return None

		with open(path, 'r') as file:
			for line in file.readlines():
				line = line.removesuffix('\n')
				sline = line.strip()

				if sline.startswith('import'):
					submodule_scriptname = line.removeprefix('import ').strip()
					submodule_path = './' + submodule_scriptname.replace('.', '/') + '.py'

					submodule_name = moduleify(module_dir / submodule_path)
		
					if submodule_name != None:
						out += f'\t{submodule_scriptname} = {DEFINE}{submodule_name}()\n'
					else:
						out += '\t' + line + '\n'

				elif sline.startswith('from '):
					submodule_path, submodule_imports = line.removeprefix('from ').split('import')

					if submodule_path.strip() == 'vex':
						continue

					submodule_path = './' + submodule_path.strip().replace('.', '/') + '.py'
					submodule_imports = [x.strip() for x in submodule_imports.split(',')]
					submodule_name = moduleify(module_dir / submodule_path)

					if submodule_name != None:
						out += f'\t{ROOT}{submodule_name} = {DEFINE}{submodule_name}()\n'

						if submodule_imports[0] == '*':
							out += f'\tfor k in {ROOT}{submodule_name}: locals()[k] = {ROOT}{submodule_name}[k]\n'
						else:
							for imp in submodule_imports:
								out += f'\t{imp} = {ROOT}{submodule_name}.{imp}\n'
					else:
						out += '\t' + line + '\n'

				elif line.startswith('class'):
					module_classes.append(sline.removeprefix('class ').split('(')[0].removesuffix(':'))
					out += '\t' + line + '\n'
				
				elif line.startswith('def'):
					module_classes.append(sline.removeprefix('def ').split('(')[0].removesuffix(':'))
					out += '\t' + line + '\n'

				elif sline.startswith('global'):
					out += '\t' + line.replace('global', 'nonlocal', 1) + '\n'

				else:
					if line.count('=') == 1:
						vname = line.split('=', 1)[0]
						if not (vname.startswith('\t') or vname.startswith(' ') or vname.startswith('#')):
							module_classes.append(vname.strip())

					out += '\t' + line + '\n'

		out += '\n\tl = locals()\n'
		for cls in module_classes:
			out += f'\tl["{cls}"] = {cls}\n'
		out += f'\t__ModuleCache__["{module_name}"] = __ModuleNamespace__(l)\n'
		out += f'\treturn __ModuleCache__["{module_name}"]\n'
		compiled_modules.append({ "name": module_name, "value": out, "path": path })
		return module_name


	main_name = moduleify(Path(args.input), '__main__')
	if main_name == None:
		raise Exception('Input does not exist!')
	
	with open(args.output, 'w') as out:
		out.write(HEADER)
		compile_length = HEADER.count('\n')+1
		module_start_dict = {}

		for mod in compiled_modules:
			if mod['name'] in compiled_module_set: continue
			module_start_dict[str(mod['path'])] = compile_length + 4
			compiled_module_set.add(mod['name'])
			out.write(mod['value'] + '\n')
			compile_length += mod['value'].count('\n')+1

		module_start_dict['<module>'] = compile_length-1

		if (args.trace == False):
			out.write(f'{DEFINE}{main_name}()\n')
			return

		out.write(f'try: {DEFINE}{main_name}()\n')
		module_start_dict_str = ','.join([f'({module_start_dict[x]},"{x}")' for x in module_start_dict])
		out.write(f'except Exception as e:\n\ts = [{module_start_dict_str}]')
		out.write(r'''
	def f(x: str):
		if not x.startswith('  File'): return x
		l = int(match('.+line (\\d+),.+', x).group(1))
		for i in range(len(s)):
			if s[i][0] > l: return '  File {} line {} ({})'.format(s[i-1][1], l-s[i-1][0], l)
		return '  File {} line {} ({})'.format(s[-1][1], l-s[-1][0], l)
	buf = StringIO()
	print_exception(e, buf)
	print('\n'.join([f(x) for x in buf.getvalue().split("\n")]))
	exit(1)
''')

compile()
print('Compiled modules successfully!')
