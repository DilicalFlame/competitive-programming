# Competitive Programming Test Runner (PowerShell)
# Compiles and tests C++ solutions against test cases

param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$Filename,
    
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CompileFlags
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

# Show help if no arguments
if (-not $Filename) {
    Write-ColorOutput "🏃 Competitive Programming Test Runner" "Cyan"
    Write-ColorOutput "======================================" "Blue"
    Write-Host
    Write-ColorOutput "Usage:" "Yellow"
    Write-ColorOutput "  .\run.ps1 <filename>                   # Run tests for filename.cpp" "Green"
    Write-ColorOutput "  .\run.ps1 <filename> -g -DDEBUG        # Run with additional compile flags" "Green"
    Write-Host
    Write-ColorOutput "Examples:" "Yellow"
    Write-ColorOutput "  .\run.ps1 4A_watermelon               # Test 4A.cpp" "Green"
    Write-ColorOutput "  .\run.ps1 two_sum -O0 -g              # Test two_sum.cpp with debug flags" "Green"
    Write-Host
    Write-ColorOutput "Note: The script automatically finds .cpp files in any subfolder" "Yellow"
    exit 1
}

$PythonScript = Join-Path $ScriptDir "scripts\test_runner.py"

# Create necessary directories
$IoDir = Join-Path $ScriptDir "io"
if (-not (Test-Path $IoDir)) {
    New-Item -ItemType Directory -Path $IoDir -Force | Out-Null
}

# Run the Python test runner
$allArgs = @($PythonScript, $Filename) + $CompileFlags
& uv run python @allArgs

$exitCode = $LASTEXITCODE
exit $exitCode
