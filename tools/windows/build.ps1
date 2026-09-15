[CmdletBinding()]
param(
    [string]$MsysRoot = "C:\msys64",
    [ValidateSet("all", "all-hdd", "kernel")]
    [string]$Target = "all"
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

Write-Host "+ make -C $projectPath $Target"
& $bash -lc "export PATH='$msysPath'; cd '$projectPath' && make '$Target'"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
