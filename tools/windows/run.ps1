[CmdletBinding()]
param(
    [string]$MsysRoot = "C:\msys64",
    [switch]$Display,
    [string]$Memory = "2G"
)

$ErrorActionPreference = "Stop"

$bash = Join-Path $MsysRoot "usr\bin\bash.exe"
if (-not (Test-Path $bash)) {
    throw "MSYS2 Bash was not found at '$bash'. Install MSYS2 or pass -MsysRoot."
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\")).Path
$msysPath = "/ucrt64/bin:/usr/bin"
$projectPath = (& $bash -lc "export PATH='$msysPath'; cygpath -u -- '$projectRoot'").Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($projectPath)) {
    throw "Could not convert the project path for MSYS2: $projectRoot"
}

$qemuFlags = "-m $Memory"
if (-not $Display) {
    $qemuFlags += " -display none -monitor none -serial stdio"
}

Write-Host "+ make -C $projectPath run QEMUFLAGS=$qemuFlags"
& $bash -lc "export PATH='$msysPath'; cd '$projectPath' && make run QEMUFLAGS='$qemuFlags'"
exit $LASTEXITCODE
