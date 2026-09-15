[CmdletBinding()]
param(
    [string]$MsysRoot = "C:\msys64",
    [ValidateSet("all", "all-hdd", "kernel")]
    [string]$Target = "all"
)

$ErrorActionPreference = "Stop"

$msysLauncher = Join-Path $MsysRoot "ucrt64.exe"
if (-not (Test-Path $msysLauncher)) {
    throw "MSYS2 UCRT64 was not found at '$msysLauncher'. Install MSYS2 or pass -MsysRoot."
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\")).Path
$projectPath = & $msysLauncher -lc "cygpath -u '$projectRoot'"
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($projectPath)) {
    throw "Could not convert the project path for MSYS2: $projectRoot"
}

Write-Host "+ make -C $projectPath $Target"
& $msysLauncher -lc "cd '$projectPath' && make '$Target'"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
