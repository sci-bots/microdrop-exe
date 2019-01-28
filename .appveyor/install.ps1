Set-PSDebug -Trace 1
Set-ExecutionPolicy RemoteSigned

# Configure Conda to operate without user input
conda config --set always_yes yes --set changeps1 no

# Allow extra Conda channels to be added (e.g., for testing).
if ($env:CONDA_EXTRA_CHANNELS) {
    $env:CONDA_EXTRA_CHANNELS.Split(";") | ForEach {
        Write-Host "Adding Conda channel from %CONDA_EXTRA_CHANNELS%: $_"
        conda config --add channels $_
    }
}


# Use PSCondaEnvs to allow activation using powershell:
conda install -n root -c pscondaenvs pscondaenvs

# Update conda, and install conda-build (used for building in non-root env)
conda update -q conda

# Create new project environment
conda env create -n microdrop-exe --file environment.yaml
if ($LASTEXITCODE) { throw "Failed to create build Conda environment." }

conda info --envs

activate
activate microdrop-exe

conda info --envs

conda install 7za -y -c conda-forge

# Download 7zip installer and extract _self-extracting (SFX)_ plugins.
cmd /C curl -L --output 7zip-installer.exe https://www.7-zip.org/a/7z1805.exe
7za x "-ir!*.sfx" 7zip-installer.exe
if ($LASTEXITCODE) { throw "Failed to extract 7zip self-extracting executable module" }
