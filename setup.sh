#!/bin/bash

# Setup script for Competitive Programming Workspace
# Installs required dependencies and sets up the environment using uv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔧 Setting up Competitive Programming Workspace${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv not found. Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env 2>/dev/null || true
    
    # Check again after installation
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}❌ Failed to install uv. Please install it manually: https://docs.astral.sh/uv/getting-started/installation/${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ uv found${NC}"

# Check if g++ is installed
if ! command -v g++ &> /dev/null; then
    echo -e "${YELLOW}⚠️  g++ not found. Attempting to install build-essential...${NC}"
    sudo apt-get update && sudo apt-get install -y build-essential
fi

echo -e "${GREEN}✅ g++ found${NC}"

# Initialize uv project if not already initialized
if [ ! -f "$SCRIPT_DIR/pyproject.toml" ]; then
    echo -e "${YELLOW}🚀 Initializing uv project...${NC}"
    cd "$SCRIPT_DIR"
    uv init --no-readme --no-workspace
    echo -e "${GREEN}✅ uv project initialized${NC}"
else
    echo -e "${GREEN}✅ uv project already exists${NC}"
fi

# Install optional Python packages for better UI using uv
echo -e "${YELLOW}📦 Installing Python packages with uv...${NC}"

packages=("rich" "inquirer")

cd "$SCRIPT_DIR"
for package in "${packages[@]}"; do
    echo -e "  Installing ${BLUE}$package${NC}..."
    uv add "$package" 2>/dev/null && echo -e "    ${GREEN}✅ $package installed${NC}" || echo -e "    ${YELLOW}⚠️  $package installation failed (optional)${NC}"
done

# Update scripts to use uv python
echo -e "${YELLOW}🔧 Updating scripts to use uv environment...${NC}"

# Update create script
if [ -f "$SCRIPT_DIR/create" ]; then
    # Replace python3 with uv run python in create script
    sed -i 's/python3 "$PYTHON_SCRIPT"/uv run python "$PYTHON_SCRIPT"/g' "$SCRIPT_DIR/create"
fi

# Update run script  
if [ -f "$SCRIPT_DIR/run" ]; then
    # Replace python3 with uv run python in run script
    sed -i 's/python3 "$PYTHON_SCRIPT"/uv run python "$PYTHON_SCRIPT"/g' "$SCRIPT_DIR/run"
fi

echo -e "${GREEN}✅ Scripts updated to use uv${NC}"

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p "$SCRIPT_DIR/io"
touch "$SCRIPT_DIR/io/input.txt"
touch "$SCRIPT_DIR/io/output.txt"
mkdir -p "$SCRIPT_DIR/01_codeforces/tests"
mkdir -p "$SCRIPT_DIR/01_codeforces/out"
mkdir -p "$SCRIPT_DIR/02_leetcode/tests"
mkdir -p "$SCRIPT_DIR/02_leetcode/out"
mkdir -p "$SCRIPT_DIR/03_atcoder/tests"
mkdir -p "$SCRIPT_DIR/03_atcoder/out"
mkdir -p "$SCRIPT_DIR/04_hackerrank/tests"
mkdir -p "$SCRIPT_DIR/04_hackerrank/out"

echo -e "${GREEN}✅ Directories created${NC}"

# Make scripts executable
echo -e "${YELLOW}🔧 Making scripts executable...${NC}"
chmod +x "$SCRIPT_DIR/create"
chmod +x "$SCRIPT_DIR/run"
chmod +x "$SCRIPT_DIR/scripts/file_generator.py"
chmod +x "$SCRIPT_DIR/scripts/test_runner.py"

echo -e "${GREEN}✅ Scripts made executable${NC}"

echo
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo
echo -e "${YELLOW}Usage:${NC}"
echo -e "  ${GREEN}./create${NC}           # Create new competitive programming files"
echo -e "  ${GREEN}./run <filename>${NC}   # Run tests for a file"
echo
echo -e "${YELLOW}Examples:${NC}"
echo -e "  ${GREEN}./create${NC}           # Interactive file creation"
echo -e "  ${GREEN}./run 4A${NC}          # Test 4A.cpp with its test cases"
echo
echo -e "${CYAN}Happy competitive programming! 🚀${NC}"
