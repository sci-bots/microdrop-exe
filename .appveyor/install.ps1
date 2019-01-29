Set-PSDebug -Trace 1
Set-ExecutionPolicy RemoteSigned

# Initialize Conda Powershell support.
~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1

# Allow extra Conda channels to be added (e.g., for testing).
if ($env:CONDA_EXTRA_CHANNELS) {
    $env:CONDA_EXTRA_CHANNELS.Split(";") | ForEach {
        Write-Host "Adding Conda channel from %CONDA_EXTRA_CHANNELS%: $_"
        conda config --add channels $_
    }
}

conda activate

# Create new project environment
conda env create -n microdrop-exe --file environment.yaml
if ($LASTEXITCODE) { throw "Failed to create build Conda environment." }

conda activate microdrop-exe
conda info --envs

conda install 7za -y -c conda-forge

# Download 7zip installer and extract _self-extracting (SFX)_ plugins.
cmd /C curl -L --output 7zip-installer.exe https://www.7-zip.org/a/7z1805.exe
7za x "-ir!*.sfx" 7zip-installer.exe
if ($LASTEXITCODE) { throw "Failed to extract 7zip self-extracting executable module" }
