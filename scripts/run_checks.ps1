[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "The .venv folder was not found. Run .\scripts\setup_windows.ps1 first."
}

Write-Host "== Python =="
& $venvPython --version
& $venvPython -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "Python in .venv must be 3.11 or newer."
}

Write-Host "== pip check =="
& $venvPython -m pip check
if ($LASTEXITCODE -ne 0) {
    throw "Dependency problems were found."
}

Write-Host "== Runtime package imports =="
$runtimeModules = @("requests", "bs4", "lxml", "pandas", "openpyxl", "dotenv", "tenacity")
foreach ($moduleName in $runtimeModules) {
    & $venvPython -c "import importlib; importlib.import_module('$moduleName')"
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to import package: $moduleName"
    }
}
Write-Host "Runtime package imports: OK"

$pythonFiles = @(Get-ChildItem -Path $projectRoot -Recurse -File -Filter "*.py" | Where-Object {
    $_.FullName -notmatch "\\.venv\\|\\__pycache__\\|\\build\\|\\dist\\"
})
$testFiles = @($pythonFiles | Where-Object { $_.Name -like "test_*.py" -or $_.FullName -match "\\tests\\" })

if ($testFiles.Count -gt 0) {
    Write-Host "== Pytest =="
    & $venvPython -m pytest
    if ($LASTEXITCODE -ne 0) {
        throw "Pytest failed."
    }
} else {
    Write-Host "No test files found; skipping Pytest for Phase 1."
}

$ruffAvailable = $true
& $venvPython -m ruff --version 2>$null
if ($LASTEXITCODE -ne 0) {
    $ruffAvailable = $false
}

if ($ruffAvailable -and $pythonFiles.Count -gt 0) {
    Write-Host "== Ruff =="
    & $venvPython -m ruff check .
    if ($LASTEXITCODE -ne 0) {
        throw "Ruff failed."
    }
} else {
    Write-Host "Ruff or Python files are not available; skipping Ruff for Phase 1."
}

Write-Host "Phase 1 checks completed successfully."
