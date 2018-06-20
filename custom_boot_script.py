import os
import sys

import path_helpers as ph


MICRODROP_PYTHONPATH = [ph.path(p)
                        for p in os.environ.get('MICRODROP_PYTHONPATH',
                                                '').split(';')
                        if p.strip() and ph.path(p).realpath().exists]

for p in MICRODROP_PYTHONPATH[::-1]:
    sys.path.insert(0, p)
