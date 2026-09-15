[CmdletBinding()]
param(
    [switch]$Hard
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\")).Path
$cleanup = Join-Path $projectRoot "tools\cleanup.py"
$arguments = @($cleanup)
if ($Hard) {
    $arguments += "--hard"
}

Write-Host "+ python $($arguments -join ' ')"
& python @arguments
exit $LASTEXITCODE
