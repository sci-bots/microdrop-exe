This project defines a [`py2exe`][py2exe] configuration for packaging MicroDrop
2 as a Windows application (no need for external Python/Conda environment).

# Build

In a Conda Powershell environment:

```sh
conda create -n mdi-2.21.1 -c dropbot -c microdrop-plugins -c sci-bots -c wheeler-microfluidics '"microdrop ==2.21.1"' '"python=2.7"' '"dmf-device-ui >=0.10"' '"microdrop-plugin-manager >=0.25.1"' '"pip"' '"pywin32"' '"microdrop.droplet-planning-plugin >=2.3.1"' '"microdrop.dmf-device-ui-plugin >=2.6"' '"microdrop.dropbot-plugin >=2.22.5"' '"microdrop.user-prompt-plugin >=2.3.1"' '"microdrop.step-label-plugin >=2.2.2"' '"nadamq >=0.19.3"'
activate microdrop-installer
# Explicit link is necessary since py2exe==0.6.9 is no longer available on PyPi
pip install http://nchc.dl.sourceforge.net/project/py2exe/py2exe/0.6.9/py2exe-0.6.9.zip
# Link all available plugins to enabled directory
python -m mpm.bin.api enable $(dir $env:CONDA_PREFIX\share\microdrop\plugins\available)

# Conda version of `cycler` is not compatible with py2exe.  Install PyPi version.
conda uninstall --force cycler -y
pip install cycler

# Build packaged MicroDrop Windows executable application.
python .\setup.py py2exe 2>&1 | Tee-Object -FilePath py2exe-build.log
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

# Develop

To test a built MicroDrop executable distribution, it may be helpful to **enable
all available plugins by default**:

```sh
dir $env:CONDA_PREFIX\share\microdrop\plugins\available | % { microdrop-config edit --append plugins.enabled $_.Name }
```

Note that this may also be done by running `post-install.bat` in the generated
`dist` directory.


[py2exe]: http://www.py2exe.org
