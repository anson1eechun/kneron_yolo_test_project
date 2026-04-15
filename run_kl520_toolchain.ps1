# Run from repo root: build KL520 NEF via kneron/toolchain Docker.
# Requires Docker Desktop and: docker pull kneron/toolchain
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Checking Docker..."
docker ps | Out-Null

New-Item -ItemType Directory -Force -Path (Join-Path $root "kneron_workspace\output\kl520_flow") | Out-Null

Write-Host "Starting kneron/toolchain (output -> kneron_workspace\output\kl520_flow)..."
docker run --rm `
  -e "KNERON_PROJECT=/project" `
  -v "${root}:/project" `
  -v "${root}/kneron_workspace/output/kl520_flow:/data1/kneron_flow" `
  kneron/toolchain `
  bash /project/kneron_workspace/build_kl520_nef.sh

if ($LASTEXITCODE -ne 0) { throw "Docker/toolchain failed with exit code $LASTEXITCODE" }
Write-Host "Done. See kneron_workspace\output\kl520_flow for NEF and reports."
