[CmdletBinding()]
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$Previous = "use_cases\price_monitor\previous.json",
    [string]$Current = "use_cases\price_monitor\current.json",
    [string]$Output = "output\scheduled\price_changes.json",
    [string]$Lock = "output\scheduled\price-monitor.lock",
    [string]$Log = "output\scheduled\price-monitor.log"
)

$ErrorActionPreference = "Stop"
$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$python = Join-Path $resolvedRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Virtual environment not found: $python"
}

Set-Location -LiteralPath $resolvedRoot
& $python (Join-Path $resolvedRoot "scripts\run_scheduled_job.py") `
    --previous (Join-Path $resolvedRoot $Previous) `
    --current (Join-Path $resolvedRoot $Current) `
    --output (Join-Path $resolvedRoot $Output) `
    --lock (Join-Path $resolvedRoot $Lock) `
    --log (Join-Path $resolvedRoot $Log)
exit $LASTEXITCODE
