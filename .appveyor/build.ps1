Set-PSDebug -Trace 1
Set-ExecutionPolicy RemoteSigned

# Set version number based on git tag
$x = git describe --tags
if (!$?){ $prevTag="v0.0-0"
} else  { $prevTag = $x.Split("-")[0] + "-" + $x.Split("-")[1] }

$buildTag = $prevTag + "+" + $(Get-Date -Format FileDateTime)
Write-Host "Build Tag: $buildTag"
Update-AppveyorBuild -Version $buildTag

activate.ps1 $env:APPVEYOR_PROJECT_NAME

conda env create --file environment-template.yaml

# Link all available plugins to enabled directory
python -m mpm.bin.api enable $(dir $env:CONDA_PREFIX\share\microdrop\plugins\available)

# Build packaged MicroDrop Windows executable application.
python .\setup.py py2exe

# Rename `dist` directory to `microdrop-<version>`.
$dist_dir = "microdrop-$($x.Substring(1))"
mv dist $dist_dir

# Create self-extracting 7zip archive
7za a -bd -sfx"7z.sfx" -r "$dist_dir.7z" $dist_dir

# Prepend platform (i.e., `win-32`, `win-64`, `noarch`) to each package filename
# and collect package files in `artifacts` directory.
md artifacts
mv "$dist_dir.7z" artifacts
