import os
import sys

from pyutilib.component.core import PluginGlobals
import path_helpers as ph


# Add backwards compatibility for `pyutilib<5.0`
if not hasattr(PluginGlobals, 'push_env') and \
        hasattr(PluginGlobals, 'add_env'):
    PluginGlobals.push_env = PluginGlobals.add_env

MICRODROP_PYTHONPATH = [ph.path(p)
                        for p in os.environ.get('MICRODROP_PYTHONPATH',
                                                '').split(';')
                        if p.strip() and ph.path(p).realpath().exists]

for p in MICRODROP_PYTHONPATH[::-1]:
    sys.path.insert(0, p)
