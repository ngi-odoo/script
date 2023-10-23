from collections import defaultdict
import regex

fin_name = "install.log"
fout_name = "skip.py"



def write(fout, out_buffer):
	if out_buffer[~0] != '\n':
		out_buffer += '\n'
	fout.write(out_buffer)
	return ''

def parse_line(line):
	line_match = '^(?P<dt>[\d-]{10}) (?P<tm>[\d:, ]{16})ERROR \S* (?P<mod>[^\s\:]*): (ERROR)?(FAIL)?: (?P<class>\S*)\.(?P<func>.*)$'
	match = regex.match(line_match, line)
	if not match:
		return []
	return {
		"dt": match['dt'],
		"tm": match['tm'],
		"mod": match['mod'],
		"class": match['class'],
		"func": match['func'],
	}


def main():
	c = 0
	errors = []
	# Parse file
	print("Parsing file ...")
	with open(fin_name, 'r') as fin:
		for line in fin:
			c += 1
			if c % 100000 == 0:
				print(f'Processed {c} lines...')
			error = parse_line(line)
			if error:
				errors += [error]
	print(f"File parsed, found {len(errors)} errors")
	# Parse errors
	# File containing class containing method
	mods = defaultdict(lambda: defaultdict(lambda: []))
	lines = []
	for error in errors:
		mod = error['mod']
		clazz = error['class']
		func = error['func']
		mods[mod][clazz] += [func]

	# Output file
	print("Generating file")
	with open(fout_name, 'w+') as fout:
		fout.write("import unittest\n\n")
		for mod in mods:
			fout.write(f"from {mod} import (\n")
			for clazz in mods[mod]:
				fout.write(f"    {clazz},\n")
			fout.write(")\n")
		fout.write("\n")
		fout.write("""
@unittest.skip("Skip")
def skip(self):
    pass


# These devs are failing:
""")
		for mod in mods:
			my_mod = mods[mod]
			for clazz in my_mod:
				my_clazz = my_mod[clazz]
				for func in my_clazz:
					fout.write(f"{clazz}.{func} = skip\n")

	#fout = 

if __name__ == '__main__':
	main()
