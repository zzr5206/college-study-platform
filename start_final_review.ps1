$ErrorActionPreference = "Stop"

$appDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonCandidates = @(
    "C:\Anaconda3\python.exe",
    (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
)

$appFile = Join-Path $appDir "desktop_app.py"
if (-not (Test-Path -LiteralPath $appFile)) {
    Write-Host ""
    Write-Host "Cannot find the app file:"
    Write-Host $appFile
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

$python = $pythonCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $python) {
    Write-Host ""
    Write-Host "Python was not found. Tried:"
    $pythonCandidates | ForEach-Object { Write-Host $_ }
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

Set-Location -LiteralPath $appDir
& $python "desktop_app.py"
