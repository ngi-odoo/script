import regex
from datetime import datetime

DT_FORMAT = '%Y-%m-%d %H:%M:%S'

fin_name = 'odoo.log'
# fout_name, light = 'odoo_light_parsed.log', True
fout_name, light = 'odoo_parsed.log', False
fout = open(fout_name, 'w+')


def write(fout, out_buffer):
    if out_buffer[~0] != '\n':
        out_buffer += '\n'
    fout.write(out_buffer)
    return ''

def odoo2pgbadger(line):
    line_match = '^(?P<dt>.{19}).*\[(?P<timer>.+) ms\] query:(?P<query>.+)$'
    match = regex.match(line_match, line)
    if not match:
        return ''
    return '%s [1]: LOG:  duration: %s ms  statement: %s' % (
        match['dt'],
        float(match['timer']),
        match['query'],
    )

def startswithdate(line):
    try:
        datetime.strptime(line[:19], DT_FORMAT)
        return True
    except ValueError as e:
        return False
    except Exception as e:
        raise(e)


c, pl = 0, 0
out_buffer = ''
with open(fin_name, 'r') as fin:
    for line in fin:
        c += 1
        if not c%100000:
            if light:
                break
            print('Processed %s lines...' % c)

        if out_buffer:
            if startswithdate(line):
                pl += 1
                out_buffer = write(fout, out_buffer)
            else:
                out_buffer += ' %s' % line.strip()

        if not out_buffer:
            out_buffer += odoo2pgbadger(line)

if out_buffer:
    pl += 1
    fout.write(out_buffer)

print('Total Lines: %s' % c)
print('Parsed Lines: %s' % pl)
print('pgbadger odoo_parsed.log -f stderr')
