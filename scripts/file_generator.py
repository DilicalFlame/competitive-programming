#!/usr/bin/env python3
"""
Competitive Programming File Generator
Creates boilerplate files for different platforms with interactive UI
"""

import os
import sys
from enum import Enum
from dataclasses import dataclass
from typing import Optional

# Try to import rich for beautiful UI, fallback to simple implementation
try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Color utility class for beautiful terminal output (fallback when Rich is not available)
class Colors:
    """ANSI color codes for terminal output"""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def colored_print(text: str, color: str = Colors.WHITE, style: str = "", end: str = "\n"):
    """Print colored text to terminal"""
    print(f"{style}{color}{text}{Colors.RESET}", end=end)

def success(text: str, end: str = "\n"):
    """Print success message in green"""
    colored_print(text, Colors.BRIGHT_GREEN, Colors.BOLD, end)

def error(text: str, end: str = "\n"):
    """Print error message in red"""
    colored_print(text, Colors.BRIGHT_RED, Colors.BOLD, end)

def warning(text: str, end: str = "\n"):
    """Print warning message in yellow"""
    colored_print(text, Colors.BRIGHT_YELLOW, Colors.BOLD, end)

def info(text: str, end: str = "\n"):
    """Print info message in cyan"""
    colored_print(text, Colors.BRIGHT_CYAN, end=end)

# Try to import inquirer for interactive selection
try:
    import inquirer
    INQUIRER_AVAILABLE = True
except ImportError:
    INQUIRER_AVAILABLE = False

if RICH_AVAILABLE:
    console = Console()

class Platform(Enum):
    CODEFORCES = ("01_codeforces", "Codeforces", "https://codeforces.com/")
    LEETCODE = ("02_leetcode", "LeetCode", "https://leetcode.com/")
    ATCODER = ("03_atcoder", "AtCoder", "https://atcoder.jp/")
    HACKERRANK = ("04_hackerrank", "HackerRank", "https://www.hackerrank.com/")
    
    def __init__(self, folder, display_name, base_url):
        self.folder = folder
        self.display_name = display_name
        self.base_url = base_url

@dataclass
class FileConfig:
    platform: Platform
    filename: str
    method_name: Optional[str] = None
    return_type: Optional[str] = None
    parameters: Optional[str] = None

def print_header():
    if RICH_AVAILABLE:
        header = Text("🚀 Competitive Programming File Generator", style="bold blue")
        console.print(Panel(Align.center(header), border_style="bright_blue"))
    else:
        colored_print("🚀 Competitive Programming File Generator", Colors.BRIGHT_CYAN, Colors.BOLD)
        colored_print("=" * 50, Colors.BRIGHT_BLUE)

def select_platform() -> Platform:
    """Interactive platform selection"""
    if INQUIRER_AVAILABLE:
        questions = [
            inquirer.List('platform',
                message="Select the platform",
                choices=[(p.display_name, p) for p in Platform],
                carousel=True
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers['platform']
    else:
        # Fallback to simple input
        if RICH_AVAILABLE:
            table = Table(title="Available Platforms")
            table.add_column("Number", style="cyan")
            table.add_column("Platform", style="magenta")
            
            for i, platform in enumerate(Platform, 1):
                table.add_row(str(i), platform.display_name)
            
            console.print(table)
            
            while True:
                choice = Prompt.ask("Select platform (1-4)", default="1")
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(Platform):
                        return list(Platform)[idx]
                except ValueError:
                    pass
                console.print("[red]Invalid choice! Please enter 1-4[/red]")
        else:
            colored_print("\nAvailable Platforms:", Colors.BRIGHT_CYAN, Colors.BOLD)
            for i, platform in enumerate(Platform, 1):
                colored_print(f"{i}. ", Colors.BRIGHT_WHITE, end="")
                
                # Color-code platforms
                if platform == Platform.CODEFORCES:
                    colored_print(platform.display_name, Colors.BRIGHT_BLUE, Colors.BOLD)
                elif platform == Platform.LEETCODE:
                    colored_print(platform.display_name, Colors.BRIGHT_YELLOW, Colors.BOLD)
                elif platform == Platform.ATCODER:
                    colored_print(platform.display_name, Colors.BRIGHT_GREEN, Colors.BOLD)
                elif platform == Platform.HACKERRANK:
                    colored_print(platform.display_name, Colors.BRIGHT_MAGENTA, Colors.BOLD)
            
            while True:
                try:
                    colored_print("Select platform (1-4): ", Colors.WHITE, end="")
                    choice = int(input())
                    if 1 <= choice <= len(Platform):
                        return list(Platform)[choice - 1]
                    error("Invalid choice! Please enter 1-4")
                except ValueError:
                    error("Invalid input! Please enter a number")

def get_filename(platform: Platform) -> str:
    """Get filename from user"""
    if RICH_AVAILABLE:
        filename = Prompt.ask(f"Enter filename (without .cpp extension)")
    else:
        colored_print(f"Enter filename (without .cpp extension): ", Colors.BRIGHT_CYAN, end="")
        filename = input()
    
    return filename.strip()

def get_leetcode_details() -> tuple[str, str, str]:
    """Get LeetCode specific details"""
    if RICH_AVAILABLE:
        method_name = Prompt.ask("Enter method name", default="solution")
        return_type = Prompt.ask("Enter return type", default="int")
        parameters = Prompt.ask("Enter parameters (e.g., 'vector<int>& nums, int target')", default="")
    else:
        colored_print("Enter method name (default: solution): ", Colors.BRIGHT_CYAN, end="")
        method_name = input().strip() or "solution"
        colored_print("Enter return type (default: int): ", Colors.BRIGHT_CYAN, end="")
        return_type = input().strip() or "int"
        colored_print("Enter parameters (e.g., 'vector<int>& nums, int target'): ", Colors.BRIGHT_CYAN, end="")
        parameters = input().strip()
    
    return method_name, return_type, parameters

def create_standard_cpp_file(config: FileConfig, filepath: str) -> None:
    """Create standard C++ file for Codeforces, AtCoder, HackerRank"""
    content = f"""// {config.platform.display_name}: paste link to problem here

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <deque>
#include <cmath>
#include <climits>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    // Your code here
    
    return 0;
}}
"""
    
    with open(filepath, 'w') as f:
        f.write(content)

def create_leetcode_cpp_file(config: FileConfig, filepath: str) -> None:
    """Create LeetCode C++ file with Solution class"""
    # Format parameters if provided
    params = config.parameters if config.parameters else ""
    
    content = f"""// {config.platform.display_name}: paste link to problem here

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <deque>
#include <cmath>
#include <climits>

using namespace std;

class Solution {{
public:
    {config.return_type} {config.method_name}({params}) {{
        // Your code here
        
    }}
}};
"""
    
    with open(filepath, 'w') as f:
        f.write(content)

def create_standard_test_file(config: FileConfig, filepath: str) -> None:
    """Create standard test file for Codeforces, AtCoder, HackerRank"""
    content = f"""# {config.platform.display_name} - {config.filename}

## Problem Description
Add problem description here

## Test Cases

```tests
sample input

sample output
---
sample input

sample output
```

## Notes
Add any additional notes here
"""
    
    with open(filepath, 'w') as f:
        f.write(content)

def create_leetcode_test_file(config: FileConfig, filepath: str) -> None:
    """Create LeetCode test file"""
    # Create sample input format based on parameters
    sample_format = ""
    if config.parameters:
        # Count vector parameters
        vector_count = config.parameters.count("vector<int>")
        if vector_count >= 2:
            sample_format = "[1,3] [2]"
        elif "vector<int>" in config.parameters and "int" in config.parameters:
            sample_format = "[2,7,11,15] 9"
        elif "vector<int>" in config.parameters:
            sample_format = "[2,7,11,15]"
        elif "string" in config.parameters:
            sample_format = "\"hello\" \"world\""
        elif "int" in config.parameters:
            sample_format = "5 3"
        else:
            sample_format = "input1 input2"
    else:
        sample_format = "input_value"
    
    # Create sample output format based on return type
    sample_output = ""
    if config.return_type == "vector<int>":
        sample_output = "[0,1]"
    elif config.return_type == "int":
        sample_output = "42"
    elif config.return_type == "double":
        sample_output = "2.00000"
    elif config.return_type == "string":
        sample_output = "result"
    elif config.return_type == "bool":
        sample_output = "true"
    else:
        sample_output = "expected_output"
    
    content = f"""# {config.platform.display_name} - {config.filename}

## Problem Description
Add problem description here

## Test Cases

```tests
Function: {config.method_name}
Sample Input: {sample_format}
Sample Output: {sample_output}
---
Function: {config.method_name}
Sample Input: {sample_format}
Sample Output: {sample_output}
```

## Notes
- Input format: {config.parameters if config.parameters else 'Add parameter description'}
- Return type: {config.return_type}
- Add any additional notes here
"""
    
    with open(filepath, 'w') as f:
        f.write(content)

def create_files(config: FileConfig) -> None:
    """Create the C++ and test files"""
    # Get workspace root
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create paths
    cpp_dir = os.path.join(workspace_root, config.platform.folder)
    cpp_filepath = os.path.join(cpp_dir, f"{config.filename}.cpp")
    
    test_dir = os.path.join(cpp_dir, "tests")
    test_filepath = os.path.join(test_dir, f"{config.filename}.md")
    
    # Create directories if they don't exist
    os.makedirs(cpp_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # Check if files already exist
    if os.path.exists(cpp_filepath) or os.path.exists(test_filepath):
        if RICH_AVAILABLE:
            overwrite = Confirm.ask(f"Files already exist for {config.filename}. Overwrite?", default=False)
        else:
            warning(f"Files already exist for {config.filename}.")
            colored_print("Overwrite? (y/N): ", Colors.BRIGHT_YELLOW, end="")
            overwrite = input().lower().startswith('y')
        
        if not overwrite:
            if RICH_AVAILABLE:
                console.print("[yellow]Operation cancelled.[/yellow]")
            else:
                warning("Operation cancelled.")
            return
    
    # Create C++ file
    if config.platform == Platform.LEETCODE:
        create_leetcode_cpp_file(config, cpp_filepath)
        create_leetcode_test_file(config, test_filepath)
    else:
        create_standard_cpp_file(config, cpp_filepath)
        create_standard_test_file(config, test_filepath)
    
    # Success message
    if RICH_AVAILABLE:
        success_panel = Panel(
            f"✅ Files created successfully!\n\n"
            f"📁 C++ File: {cpp_filepath}\n"
            f"📝 Test File: {test_filepath}",
            title="Success",
            border_style="green"
        )
        console.print(success_panel)
    else:
        print()
        success(f"✅ Files created successfully!")
        info(f"📁 C++ File: {cpp_filepath}")
        info(f"📝 Test File: {test_filepath}")

def main():
    """Main function"""
    print_header()
    
    try:
        # Select platform
        platform = select_platform()
        
        # Get filename
        filename = get_filename(platform)
        if not filename:
            if RICH_AVAILABLE:
                console.print("[red]Filename cannot be empty![/red]")
            else:
                error("Filename cannot be empty!")
            return
        
        # Create config
        config = FileConfig(platform=platform, filename=filename)
        
        # Get LeetCode specific details if needed
        if platform == Platform.LEETCODE:
            method_name, return_type, parameters = get_leetcode_details()
            config.method_name = method_name
            config.return_type = return_type
            config.parameters = parameters
        
        # Create files
        create_files(config)
        
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        else:
            print()
            warning("Operation cancelled by user.")
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error: {str(e)}[/red]")
        else:
            error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
