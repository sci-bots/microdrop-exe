# microdrop-exe

[![Build status](https://ci.appveyor.com/api/projects/status/pjxh5g91jpbh7t84?svg=true)](https://ci.appveyor.com/project/SciBots/microdrop-exe)
  
[![Build history](https://buildstats.info/appveyor/chart/SciBots/microdrop-exe)](https://ci.appveyor.com/project/SciBots/microdrop-exe/history)


<!-- vim-markdown-toc GFM -->

* [Build](#build)
    * [Configuring Conda for Powershell](#configuring-conda-for-powershell)
* [Develop](#develop)

<!-- vim-markdown-toc -->

------------------------------------------------------------------------

This project defines a [`py2exe`][py2exe] configuration for packaging MicroDrop
2 as a Windows application (no need for external Python/Conda environment).

# Build

In a Windows 32-bit Python 2.7 Conda Powershell environment (see
[below](#configuring-conda-for-powershell)) run:

```sh
conda env create --file environment.yaml
conda activate microdrop-exe
# Link all available plugins to enabled directory
python -m mpm.bin.api enable $(dir $env:CONDA_PREFIX\share\microdrop\plugins\available)

# Build packaged MicroDrop Windows executable application.
python .\setup.py py2exe 2>&1 | Tee-Object -FilePath py2exe-build.log
```

Or, in a Windows 32-bit Python 2.7 Conda `cmd.exe` environment run:

```sh
conda env create --file environment.yaml
conda activate microdrop-exe
# Link all available plugins to enabled directory
for /f "usebackq delims=|" %f in (`dir /b "%CONDA_PREFIX%\share\microdrop\plugins\available"`) do python -m mpm.bin.api enable %f

# Build packaged MicroDrop Windows executable application.
python .\setup.py py2exe
```

This will create a `dist` output directory containing the following files:

| Name                    | Description                                      |
|-------------------------|--------------------------------------------------|
| `dropbot-upload.exe`    | Flash DropBot firmware                           |
| `jupyter-notebook.exe`  | Run Jupyter notebook                             |
| `microdrop-config.exe`  | Display/modify MicroDrop configuration           |
| `microdrop-console.exe` | **(Debug app)** Run MicroDrop as console app     |
| `MicroDrop.exe`         | **(Default app)** Run MicroDrop GUI              |
| `pio.exe`               | PlatformIO app                                   |
| `post-install.bat`      | Run post-install actions (e.g., enable plugins)  |
| `python.exe`            | Emulate `-m ...`, `<script>` support (no shell)  |
| `README.md`             | **Usage instructions**                           |
| `runpy.exe`             | Run Python module. Equivalent to `python -m ...` |

## Configuring Conda for Powershell

Conda 4.6 introduced [official support for Powershell console
environments][conda-4.6]. To enable Powershell support, execute the following
from within an existing Conda environment:

```sh
# Modify default Powershell profile to add Conda support
conda init powershell
```

The next time you launch a Powershell console, the base (i.e. `root`) Conda
environment will be activated automatically.  Other environments may then be
activated using `conda activate <environment name>`.

[conda-4.6]: https://www.anaconda.com/blog/developer-blog/conda-4-6-release/

# Develop

To test a built MicroDrop executable distribution, it may be helpful to **enable
all available plugins by default**:

```sh
dir $env:CONDA_PREFIX\share\microdrop\plugins\available | % { microdrop-config edit --append plugins.enabled $_.Name }
```

Or in a `cmd.exe` shell:

```sh
for /f "usebackq delims=|" %f in (`dir /b "%CONDA_PREFIX%\share\microdrop\plugins\available"`) do microdrop-config edit --append plugins.enabled %f
```

Note that this may also be done by running `post-install.bat` in the generated
`dist` directory.


[py2exe]: http://www.py2exe.org
[conda4.6]: https://www.anaconda.com/blog/developer-blog/conda-4-6-release/
