# Refresh PATH in current PowerShell session
# This combines both Machine and User PATH variables

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "PATH refreshed successfully!" -ForegroundColor Green
Write-Host "Python version:" -ForegroundColor Cyan
python --version


