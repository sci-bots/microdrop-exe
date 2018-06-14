# See: http://www.py2exe.org/index.cgi/win32com.shell?action=show&redirect=WinShell
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass


from distutils.core import setup
import itertools as it
import os
import pkg_resources
import runpy
import site
import sys

from py2exe.build_exe import py2exe as build_exe
import jsonschema
import microdrop
import gst
import gtk
import notebook
import nbformat
import path_helpers as ph
import pint
import matplotlib
import teensy_minimal_rpc
import zmq
import whichcraft


# Add MicroDrop plugins directory to import path.
conda_prefix = ph.path(os.environ['CONDA_PREFIX'])
microdrop_plugins_dir = conda_prefix.joinpath('etc', 'microdrop', 'plugins',
                                              'enabled')
sys.path.append(microdrop_plugins_dir)

# PlatformIO shared files
platformio_share_dir = conda_prefix.joinpath('share', 'platformio')


def walk_dll(dll_name):
    for p in [ph.path(p).expand() for p in os.environ['PATH'].split(';')]:
        if p.isdir():
            for f in p.files(dll_name):
                yield f


def resource_modules(root_module):
    return sorted(set(['.'.join((root_module, p.namebase))
                       for p in map(ph.path,
                                    pkg_resources
                                    .resource_listdir(root_module, ''))
                       if p.namebase != '__init__' and not
                       pkg_resources.resource_isdir(root_module, p) and
                       p.ext.startswith('.py')]))


site_packages = ph.path([p for p in site.getsitepackages()
                         if p.endswith('site-packages')][0])

# `__init__.py` is missing for:
#  - [`google` module in `google.protobuf`][1].
#  - `ruamel` module in `ruamel.yaml`
#  - `pyutilib`
#
# [1]: http://www.py2exe.org/index.cgi/GoogleProtobuf
for p in (('pyutilib', ), ('pyutilib', 'component'), ('google', ),
          ('ruamel',)):
    init_i = site_packages.joinpath(*(p + ('__init__.py', )))
    if not init_i.isfile():
        print 'Created missing `%s`.' % init_i
        init_i.touch()


class JsonSchemaCollector(build_exe):
    """
    This class Adds jsonschema files draft3.json and draft4.json to
    the list of compiled files so it will be included in the zipfile.
    """
    def copy_extensions(self, extensions):
        build_exe.copy_extensions(self, extensions)
        collect_dir = ph.path(self.collect_dir)

        for path_i, module_i in ((ph.path(notebook.__path__[0]),
                                  ('templates', )),
                                 (ph.path(jsonschema.__path__[0]),
                                  ('schemas', )),
                                 (ph.path(nbformat.__path__[0]),
                                  ('v4', )),
                                 (ph.path(pint.__path__[0]),  # pint data files
                                  ('', )),
                                 (ph.path(microdrop.__path__[0]),  # microdrop glade files, icon
                                  ('', )),
                                 (ph.path(teensy_minimal_rpc.__path__[0]),  # ADC configs CSV
                                  ('', )),
                                 ):
            data_path = path_i.joinpath(*module_i)

            # Copy the template files to the collection dir. Also add the copied
            # file to the list of compiled files so it will be included in the
            # zipfile.
            # self.collect_dir.joinpath(rel_path_i).makedirs_p()

            for file_j in data_path.walkfiles():
                if file_j.ext.startswith('.py'):
                    continue
                rel_path_j = path_i.parent.relpathto(file_j)
                collected_j = collect_dir.joinpath(rel_path_j)
                collected_j.parent.makedirs_p()
                self.copy_file(file_j, collected_j)
                self.compiled_files.append(rel_path_j)


# libzmq.dll is in same directory as zmq's __init__.py

os.environ["PATH"] += (os.path.pathsep +
                       os.path.pathsep.join([os.path.split(zmq.__file__)[0],
                                             # GStreamer DLLs
                                             ph.path(gst.__file__).parent
                                             .joinpath('plugins'),
                                             ph.path(gst.__file__).parent
                                             .joinpath('bin')]))


def data_files():
    '''
    Collect data files for packages that are not supported out of the box.
    '''
    # Seems like `libzmq.pyd` needs to be copied to `dist` directory, *even
    # though* it is already automatically copied by `py2exe` to the name
    # `zmq.libzmq.pyd`.
    # data_files_ = [('', [ph.path(zmq.__path__[0]).joinpath('libzmq.pyd')])]
    data_files_ = [('', ph.path(gst.__path__[0]).joinpath('bin').files('*.dll'))]

    # Jupyter notebook templates and static files cannot be accessed within the
    # zip file, so need to be copied.
    # The `nbformat` package contains a `jsonschema` file which cannot be
    # accessed within the zip file, so it also needs to be copied.
    for path_i, module_i in ((ph.path(notebook.__path__[0]), ('templates', )),
                             (ph.path(notebook.__path__[0]), ('static', )),
                             (ph.path(nbformat.__path__[0]), tuple())):
        data_path = path_i.joinpath(*module_i)

        # Copy the template files to the collection dir. Also add the copied
        # file to the list of compiled files so it will be included in the
        # zipfile.
        files = sorted([file_j for file_j in data_path.walkfiles()])
        for parent_i, files_i in it.groupby(files, lambda x: x.parent):
            data_files_ += [(path_i.parent.relpathto(parent_i),
                             list(files_i))]

    # Add Intel Math Kernel Library DLLs for `numpy`, `pandas`, etc.
    data_files_ += [('', list(walk_dll('mkl_*.dll')) +
                     list(walk_dll('MSVCP90.dll')) +
                     list(walk_dll('libiomp5md.dll')))]

    # gtk theme
    runtime_path = ph.path(gtk.__file__).parent.parent.joinpath('gtk_runtime')
    rc_path = runtime_path.joinpath('share', 'themes', 'MS-Windows', 'gtk-2.0',
                                    'gtkrc')
    engines_path = runtime_path.joinpath('lib', 'gtk-2.0', '2.10.0', 'engines')
    icons_path = runtime_path.joinpath('share', 'icons', 'hicolor')
    data_files_ += [(r'etc/gtk-2.0', [rc_path]),
                    (runtime_path.relpathto(engines_path),
                     list(engines_path.files('*.dll'))),
                    (runtime_path.relpathto(icons_path),
                     list(icons_path.walkfiles())),
                    # Add wrapper to emulate running in a Conda environment.
                    (r'Scripts/wrappers/conda', ['run-in.bat']),
                    # Make PlatformIO entry point wrapper to `pio-script.exe`
                    (r'Scripts', ['pio.bat']),
                    ]
    return data_files_


scripts_dir = ph.path(sys.prefix).joinpath('Scripts')

runpy_file = os.path.join(os.path.split(runpy.__file__)[0], 'runpy.py')
microdrop_file = scripts_dir.joinpath('microdrop-script.py')
pip_file = scripts_dir.joinpath('pip-script.py')
pio_file = scripts_dir.joinpath('pio-script.py')

setup(console=['jupyter-notebook.py', 'ipython.py', runpy_file] +
      map(str, (pip_file, pio_file, microdrop_file)),
      cmdclass={"py2exe": JsonSchemaCollector},
      # See http://www.py2exe.org/index.cgi/ListOfOptions
      options={'py2exe': {'unbuffered': True,
                          'excludes': ['jinja2.asyncsupport',
                                       'conda_helpers._async_py35',
                                       'base_node_rpc._async_py36',
                                       'asyncserial._asyncpy3'],
# Work around 'api-ms-win-core-registry-l1-1-0.dll' not found:
# https://stackoverflow.com/a/40090641/345236
"dll_excludes": [
'MSVCP90.dll',
'IPHLPAPI.DLL',
'NSI.dll',
'WINNSI.DLL',
'WTSAPI32.dll',
'SHFOLDER.dll',
'PSAPI.dll',
'MSVCR120.dll',
'MSVCP120.dll',
'CRYPT32.dll',
'GDI32.dll',
'ADVAPI32.dll',
'CFGMGR32.dll',
'USER32.dll',
'POWRPROF.dll',
'MSIMG32.dll',
'WINSTA.dll',
'MSVCR90.dll',
'KERNEL32.dll',
'MPR.dll',
'Secur32.dll',
],
                          # 'dll_excludes': ['MSVFW32.dll',
                                           # 'AVIFIL32.dll',
                                           # 'AVICAP32.dll',
                                           # 'ADVAPI32.dll',
                                           # 'CRYPT32.dll',
                                           # 'WLDAP32.dll'],
                          'includes': ['matplotlib', 'numpy', 'pandas',
                                       'matplotlib.backends.backend_wxagg',
                                       'cycler', 'IPython',
                                       'cairo', 'gio', 'pango', 'pangocairo', 'atk',  # gtk
                                       'pyutilib.component.core', 'pyutilib.component.config', 'pyutilib.component.loader',  # pyutilib
                                       # microdrop
                                       'lxml.etree',
                                       'lxml._elementpath',
                                       'win32com.shell',
                                       'pkg_resources.py31compat',
                                       'pkg_resources._vendor.appdirs',
                                       'pkg_resources._vendor.packaging.markers',
                                       'pkg_resources._vendor.packaging.requirements',
                                       'pkg_resources._vendor.packaging.specifiers',
                                       'pkg_resources._vendor.packaging.utils',
                                       'pkg_resources._vendor.packaging.version',
                                       'pkg_resources._vendor.packaging._compat',
                                       'pkg_resources._vendor.packaging._structures',
                                       'pkg_resources._vendor.packaging.__about__',
                                       'pkg_resources._vendor.pyparsing',
                                       'pkg_resources._vendor.six',

                                       'zmq',
                                       'zmq.utils',
                                       'zmq.utils.jsonapi',
                                       'zmq.utils.strtypes']}},
      # See http://www.py2exe.org/index.cgi/MatPlotLib
      data_files=matplotlib.get_py2exe_datafiles() +
      data_files())
