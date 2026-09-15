[CmdletBinding()]
param(
    [string]$MsysRoot = "C:\msys64",
    [switch]$Display,
    [string]$Memory = "2G"
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

$qemuFlags = "-m $Memory"
if (-not $Display) {
    $qemuFlags += " -display none -monitor none -serial stdio"
}

Write-Host "+ make -C $projectPath run QEMUFLAGS=$qemuFlags"
& $msysLauncher -lc "cd '$projectPath' && make run QEMUFLAGS='$qemuFlags'"
exit $LASTEXITCODE
