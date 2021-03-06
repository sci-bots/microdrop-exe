from distutils.core import setup

import matplotlib
import path_helpers as ph
import ruamel.yaml as yaml

from py2exe_helpers import (apply_patches, conda_collector, get_excludes,
                            get_dll_excludes, get_data_files,
                            group_data_files, get_console_scripts,
                            get_windows_exes, get_includes, get_packages,
                            fix_init)


environment_ = yaml.load(open('environment.yaml', 'r'),
                         Loader=yaml.loader.Loader)
package_specs = environment_['dependencies']

apply_patches('patches')

# Create missing `__init__` files.
fix_init(package_specs)

setup(windows=get_windows_exes(package_specs),
      console=get_console_scripts(package_specs),
      cmdclass={'py2exe': conda_collector(package_specs)},
      # See http://www.py2exe.org/index.cgi/ListOfOptions
      options={'py2exe': {'compressed': False,
                          # Insert MICRODROP_PYTHONPATH paths into sys.path
                          'custom_boot_script': 'custom_boot_script.py',
                          'dll_excludes': get_dll_excludes(package_specs),
                          'excludes': get_excludes(package_specs) +
                          ['asyncio_helpers.async_py3'],
                          'includes': get_includes(package_specs) +
                          ['joypad_control_plugin'],
                          'packages': get_packages(package_specs),
                          'skip_archive': False,
                          'unbuffered': False}},
      # See http://www.py2exe.org/index.cgi/MatPlotLib
      data_files=matplotlib.get_py2exe_datafiles() +
      group_data_files(get_data_files(package_specs)) +
      # Copy README, custom scripts, etc.
      group_data_files(sorted([(str(ph.path('src').relpathto(p.parent)),
                                str(p))
                               for p in ph.path('src').walkfiles()])))
