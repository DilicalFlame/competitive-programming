# Competitive Programming File Generator (PowerShell)
# Creates boilerplate files for different platforms

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Colors for output (PowerShell)
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

Write-ColorOutput "🚀 Competitive Programming File Generator" "Cyan"
Write-ColorOutput "==========================================" "Blue"

# Check if Python script exists
$PythonScript = Join-Path $ScriptDir "scripts\file_generator.py"

if (-not (Test-Path $PythonScript)) {
    Write-ColorOutput "❌ Error: Python script not found at $PythonScript" "Red"
    exit 1
}

# Check for required Python packages and install if missing
Write-ColorOutput "🔍 Checking dependencies..." "Yellow"

# Function to install packages if not available
function Install-IfMissing {
    param([string]$Package)
    
    $checkCmd = "uv run python -c `"import $Package`" 2>$null"
    $result = Invoke-Expression $checkCmd
    
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "📦 Installing $Package..." "Yellow"
        $installResult = & uv add $Package 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "⚠️  Could not install $Package automatically. Falling back to basic UI." "Yellow"
        }
    }
}

# Try to install optional packages for better UI
Install-IfMissing "rich"
Install-IfMissing "inquirer"

Write-ColorOutput "✅ Dependencies checked" "Green"
Write-Host

# Run the Python script
$allArgs = @($PythonScript) + $RemainingArgs
& uv run python @allArgs

# Check if the script ran successfully
if ($LASTEXITCODE -eq 0) {
    Write-Host
    Write-ColorOutput "🎉 Happy coding! Good luck with your competitive programming!" "Green"
} else {
    Write-Host
    Write-ColorOutput "❌ Something went wrong. Please check the error messages above." "Red"
    exit 1
}
