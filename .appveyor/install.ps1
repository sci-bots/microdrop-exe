Set-PSDebug -Trace 1
Set-ExecutionPolicy RemoteSigned

# Configure Conda to operate without user input
conda config --set always_yes yes --set changeps1 no

# Update conda, and install conda-build (used for building in non-root env)
conda update -q conda

# Initialize Conda Powershell support.
conda init powershell
# Reload Powershell profile (simulates restart of shell after init).
foreach ($p in "~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1", "~\Documents\WindowsPowerShell\profile.ps1", "~\Documents\PowerShell\profile.ps1") {
    if (Test-Path $p) {
        echo "Reload ``$p``";
        & $(Resolve-Path $p)
    }
}

# Allow extra Conda channels to be added (e.g., for testing).
if ($env:CONDA_EXTRA_CHANNELS) {
    $env:CONDA_EXTRA_CHANNELS.Split(";") | ForEach {
        Write-Host "Adding Conda channel from %CONDA_EXTRA_CHANNELS%: $_"
        conda config --add channels $_
    }
}

conda activate

# Create new project environment
conda env create -n $env:APPVEYOR_PROJECT_NAME --file environment.yaml
if ($LASTEXITCODE) { throw "Failed to create build Conda environment." }

conda activate $env:APPVEYOR_PROJECT_NAME
conda info --envs

conda install 7za -y -c conda-forge

# Download 7zip installer and extract _self-extracting (SFX)_ plugins.
cmd /C curl -L --output 7zip-installer.exe https://www.7-zip.org/a/7z1805.exe
7za x "-ir!*.sfx" 7zip-installer.exe
if ($LASTEXITCODE) { throw "Failed to extract 7zip self-extracting executable module" }
