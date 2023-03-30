from copy import deepcopy
from distutils.core import setup

import matplotlib
import path_helpers as ph
import ruamel.yaml as yaml

from py2exe_helpers import (
    DEFAULT_INCLUDES,
    DEFAULT_STATIC_PACKAGES,
    apply_patches,
    conda_collector,
    fix_init,
    get_console_scripts,
    get_data_files,
    get_dll_excludes,
    get_excludes,
    get_includes,
    get_packages,
    get_windows_exes,
    group_data_files,
)


environment_ = yaml.load(open('environment.yaml', 'r'),
                         Loader=yaml.loader.Loader)
package_specs = environment_['dependencies']

apply_patches('patches')

# Create missing `__init__` files.
fix_init(package_specs)

static_packages = deepcopy(DEFAULT_STATIC_PACKAGES)
static_packages["mr-box-peripheral-board"] = {"module": "mr_box_peripheral_board"}
static_packages["pymunk"] = {}

package_includes = deepcopy(DEFAULT_INCLUDES)
package_includes["microdrop.joypad-control-plugin"] = [
      "joypad_control_plugin",
]

setup(
    windows=get_windows_exes(package_specs),
    console=get_console_scripts(package_specs),
    cmdclass={"py2exe": conda_collector(package_specs, static_packages)},
    # See http://www.py2exe.org/index.cgi/ListOfOptions
    options={
        "py2exe": {
            "compressed": False,
            # Insert MICRODROP_PYTHONPATH paths into sys.path
            "custom_boot_script": "custom_boot_script.py",
            "dll_excludes": get_dll_excludes(package_specs),
            "excludes": get_excludes(package_specs)
            + [
                "asyncio_helpers.async_py3",
                "conda_helpers._async_py35",
            ],
            "includes": get_includes(package_specs, package_includes),
            "packages": get_packages(package_specs),
            "skip_archive": False,
            "unbuffered": False,
        }
    },
    # See http://www.py2exe.org/index.cgi/MatPlotLib
    data_files=matplotlib.get_py2exe_datafiles()
    + group_data_files(get_data_files(package_specs))
    +
    # Copy README, custom scripts, etc.
    group_data_files(
        sorted(
            [
                (str(ph.path("src").relpathto(p.parent)), str(p))
                for p in ph.path("src").walkfiles()
            ]
        )
    ),
)
