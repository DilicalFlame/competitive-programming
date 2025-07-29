# Setup script for Competitive Programming Workspace (PowerShell)
# Installs required dependencies and sets up the environment using uv

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

Write-ColorOutput "🔧 Setting up Competitive Programming Workspace" "Cyan"
Write-ColorOutput "=============================================" "Blue"

# Check if uv is installed
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvInstalled) {
    Write-ColorOutput "⚠️  uv not found. Please install uv manually:" "Yellow"
    Write-ColorOutput "Visit: https://docs.astral.sh/uv/getting-started/installation/" "Yellow"
    Write-ColorOutput "For Windows, run: powershell -c ""irm https://astral.sh/uv/install.ps1 | iex""" "Yellow"
    exit 1
}

Write-ColorOutput "✅ uv found" "Green"

# Check if g++ is installed (for MinGW or similar)
$gppInstalled = Get-Command g++ -ErrorAction SilentlyContinue
if (-not $gppInstalled) {
    Write-ColorOutput "⚠️  g++ not found. Please install a C++ compiler:" "Yellow"
    Write-ColorOutput "Options:" "Yellow"
    Write-ColorOutput "  - Install MinGW-w64: https://www.mingw-w64.org/" "Yellow"
    Write-ColorOutput "  - Install Visual Studio with C++ support" "Yellow"
    Write-ColorOutput "  - Install clang" "Yellow"
} else {
    Write-ColorOutput "✅ g++ found" "Green"
}

# Initialize uv project if not already initialized
$pyprojectPath = Join-Path $ScriptDir "pyproject.toml"
if (-not (Test-Path $pyprojectPath)) {
    Write-ColorOutput "🚀 Initializing uv project..." "Yellow"
    Set-Location $ScriptDir
    & uv init --no-readme --no-workspace
    Write-ColorOutput "✅ uv project initialized" "Green"
} else {
    Write-ColorOutput "✅ uv project already exists" "Green"
}

# Install optional Python packages for better UI using uv
Write-ColorOutput "📦 Installing Python packages with uv..." "Yellow"

$packages = @("rich", "inquirer")

Set-Location $ScriptDir
foreach ($package in $packages) {
    Write-ColorOutput "  Installing $package..." "Blue"
    $result = & uv add $package 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "    ✅ $package installed" "Green"
    } else {
        Write-ColorOutput "    ⚠️  $package installation failed (optional)" "Yellow"
    }
}

Write-ColorOutput "✅ Scripts are ready to use with uv" "Green"

# Create necessary directories
Write-ColorOutput "📁 Creating directories..." "Yellow"

$directories = @(
    "io",
    "01_codeforces\tests",
    "01_codeforces\out",
    "02_leetcode\tests", 
    "02_leetcode\out",
    "03_atcoder\tests",
    "03_atcoder\out",
    "04_hackerrank\tests",
    "04_hackerrank\out"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $ScriptDir $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    }
}

# Create empty files
$inputFile = Join-Path $ScriptDir "io\input.txt"
$outputFile = Join-Path $ScriptDir "io\output.txt"

if (-not (Test-Path $inputFile)) {
    New-Item -ItemType File -Path $inputFile -Force | Out-Null
}
if (-not (Test-Path $outputFile)) {
    New-Item -ItemType File -Path $outputFile -Force | Out-Null
}

Write-ColorOutput "✅ Directories created" "Green"

Write-Host
Write-ColorOutput "🎉 Setup complete!" "Green"
Write-Host
Write-ColorOutput "Usage:" "Yellow"
Write-ColorOutput "  .\create.ps1           # Create new competitive programming files" "Green"
Write-ColorOutput "  .\run.ps1 <filename>   # Run tests for a file" "Green"
Write-ColorOutput "  .\create.cmd           # CMD version of create" "Green"
Write-ColorOutput "  .\run.cmd <filename>   # CMD version of run" "Green"
Write-Host
Write-ColorOutput "Examples:" "Yellow"
Write-ColorOutput "  .\create.ps1           # Interactive file creation" "Green"
Write-ColorOutput "  .\run.ps1 4A          # Test 4A.cpp with its test cases" "Green"
Write-Host
Write-ColorOutput "Happy competitive programming! 🚀" "Cyan"
