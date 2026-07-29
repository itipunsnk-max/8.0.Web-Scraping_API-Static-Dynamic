[CmdletBinding()]
param(
    [switch]$InstallBrowser
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$pythonCommand = $null
$pythonArguments = @()
$pythonLauncher = Get-Command py.exe -ErrorAction SilentlyContinue

if ($null -ne $pythonLauncher) {
    $pythonCommand = $pythonLauncher.Source
    $pythonArguments = @("-3")
} else {
    $pythonExecutable = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($null -eq $pythonExecutable) {
        throw "Python was not found. Install Python 3.11 or newer, then reopen PowerShell."
    }
    $pythonCommand = $pythonExecutable.Source
}

& $pythonCommand @pythonArguments -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "Python 3.11 or newer is required."
}

$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Creating virtual environment at $venvPath"
    & $pythonCommand @pythonArguments -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "Virtual environment creation failed."
    }
} else {
    Write-Host "Existing virtual environment found; it will be reused."
}

& $venvPython --version
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "pip upgrade failed."
}

$extras = "dev"
if ($InstallBrowser) {
    $extras = "dev,browser"
}

Write-Host "Installing dependencies: [$extras]"
& $venvPython -m pip install -e ".[${extras}]"
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

if ($InstallBrowser) {
    Write-Host "Installing Chromium for Playwright"
    & $venvPython -m playwright install chromium
    if ($LASTEXITCODE -ne 0) {
        throw "Chromium installation for Playwright failed."
    }
}

Write-Host "Phase 1 setup completed."
Write-Host "Activate the environment with: .\.venv\Scripts\Activate.ps1"
