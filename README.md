In a Conda Powershell environment:

```sh
conda create -n microdrop-installer -c microdrop-plugins -c sci-bots -c wheeler-microfluidics '"python=2.7"' '"dmf-device-ui >=0.10"' '"microdrop ==2.19"' '"microdrop-plugin-manager >=0.25.1"' '"pip"' '"pywin32"' '"microdrop.droplet-planning-plugin >=2.3.1"' '"microdrop.dmf-device-ui-plugin >=2.6"' '"microdrop.dropbot-plugin >=2.22.5"' '"microdrop.user-prompt-plugin >=2.3.1"' '"microdrop.step-label-plugin >=2.2.2"' '"nadamq >=0.19.3"'
activate microdrop-installer
python .\setup.py py2exe 2>&1 | Tee-Object -FilePath py2exe-build.log
```

This will create a `dist` output directory containing the following executable
files:

 - `microdrop-script.exe`: Launch MicroDrop
 - `runpy.exe`: Run Python module.  Equivalent to `python -m ...`
 - `jupyter-notebook.exe`: Run Jupyter notebook
 - `ipython.exe`: IPython interactive Python shell
