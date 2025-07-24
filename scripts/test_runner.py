#!/usr/bin/env python3
"""
Competitive Programming Test Runner
Runs and tests C++ solutions against test cases
"""

import os
import sys
import subprocess
import time
import re
import tempfile
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class TestCase:
    input_data: str
    expected_output: str
    test_number: int

@dataclass
class TestResult:
    test_case: TestCase
    actual_output: str
    passed: bool
    execution_time: float
    memory_used: str

@dataclass
class CompilationResult:
    success: bool
    error_message: str = ""
    executable_path: str = ""

class Platform:
    CODEFORCES = "Codeforces"
    LEETCODE = "LeetCode"
    ATCODER = "AtCoder"
    HACKERRANK = "HackerRank"

def print_header():
    print("🏃 Competitive Programming Test Runner")
    print("=" * 50)

def find_cpp_file(filename: str, workspace_root: str) -> Optional[str]:
    """Find C++ file in any subfolder"""
    for root, dirs, files in os.walk(workspace_root):
        # Skip certain directories
        if any(skip in root for skip in ['out', 'build', '.git', '__pycache__']):
            continue
            
        cpp_file = f"{filename}.cpp"
        if cpp_file in files:
            return os.path.join(root, cpp_file)
    
    return None

def detect_platform(cpp_filepath: str) -> str:
    """Detect platform from the first line comment"""
    try:
        with open(cpp_filepath, 'r') as f:
            first_line = f.readline().strip()
            
        if 'Codeforces' in first_line or 'codeforces' in first_line:
            return Platform.CODEFORCES
        elif 'LeetCode' in first_line or 'leetcode' in first_line:
            return Platform.LEETCODE
        elif 'AtCoder' in first_line or 'atcoder' in first_line:
            return Platform.ATCODER
        elif 'HackerRank' in first_line or 'hackerrank' in first_line:
            return Platform.HACKERRANK
        else:
            return Platform.CODEFORCES  # Default fallback
    except:
        return Platform.CODEFORCES

def find_test_file(cpp_filepath: str) -> Optional[str]:
    """Find corresponding test file"""
    cpp_dir = os.path.dirname(cpp_filepath)
    filename = os.path.splitext(os.path.basename(cpp_filepath))[0]
    
    test_file = os.path.join(cpp_dir, "tests", f"{filename}.md")
    if os.path.exists(test_file):
        return test_file
    
    return None

def parse_test_cases(test_filepath: str, platform: str) -> List[TestCase]:
    """Parse test cases from markdown file"""
    test_cases = []
    
    try:
        with open(test_filepath, 'r') as f:
            content = f.read()
        
        # Find the ```tests``` block
        tests_match = re.search(r'```tests\n(.*?)\n```', content, re.DOTALL)
        if not tests_match:
            return test_cases
        
        tests_content = tests_match.group(1)
        
        if platform == Platform.LEETCODE:
            # Parse LeetCode format
            test_blocks = tests_content.split('---')
            for i, block in enumerate(test_blocks):
                lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
                if len(lines) >= 3:
                    # Extract function name, input, and output
                    function_line = lines[0]
                    input_line = lines[1] if len(lines) > 1 else ""
                    output_line = lines[2] if len(lines) > 2 else ""
                    
                    if input_line.startswith("Sample Input:"):
                        input_data = input_line.replace("Sample Input:", "").strip()
                    else:
                        input_data = ""
                    
                    if output_line.startswith("Sample Output:"):
                        expected_output = output_line.replace("Sample Output:", "").strip()
                    else:
                        expected_output = ""
                    
                    if input_data and expected_output:
                        test_cases.append(TestCase(input_data, expected_output, i + 1))
        else:
            # Parse standard format for other platforms
            test_blocks = tests_content.split('---')
            for i, block in enumerate(test_blocks):
                lines = block.strip().split('\n')
                if len(lines) >= 2:
                    # Find empty line that separates input and output
                    empty_line_idx = -1
                    for j, line in enumerate(lines):
                        if line.strip() == '':
                            empty_line_idx = j
                            break
                    
                    if empty_line_idx > 0:
                        input_lines = lines[:empty_line_idx]
                        output_lines = lines[empty_line_idx + 1:]
                        
                        input_data = '\n'.join(input_lines)
                        expected_output = '\n'.join(output_lines).strip()
                        
                        if input_data.strip() and expected_output:
                            test_cases.append(TestCase(input_data, expected_output, i + 1))
    
    except Exception as e:
        print(f"Error parsing test cases: {str(e)}")
    
    return test_cases

def compile_cpp(cpp_filepath: str, extra_flags: Optional[List[str]] = None) -> CompilationResult:
    """Compile C++ file"""
    # Get the platform directory (e.g., 01_codeforces)
    platform_dir = os.path.dirname(cpp_filepath)
    out_dir = os.path.join(platform_dir, "out")
    os.makedirs(out_dir, exist_ok=True)
    
    filename = os.path.splitext(os.path.basename(cpp_filepath))[0]
    executable_path = os.path.join(out_dir, filename)
    
    # Base compilation flags
    flags = ["-std=c++17", "-O2", "-Wall", "-Wextra"]
    if extra_flags:
        flags.extend(extra_flags)
    
    compile_cmd = ["g++"] + flags + [cpp_filepath, "-o", executable_path]
    
    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return CompilationResult(True, "", executable_path)
        else:
            return CompilationResult(False, result.stderr)
    except subprocess.TimeoutExpired:
        return CompilationResult(False, "Compilation timeout")
    except Exception as e:
        return CompilationResult(False, str(e))

def run_test_case(executable_path: str, test_case: TestCase, workspace_root: str, platform: str = None) -> TestResult:
    """Run a single test case"""
    io_dir = os.path.join(workspace_root, "io")
    os.makedirs(io_dir, exist_ok=True)
    
    input_file = os.path.join(io_dir, "input.txt")
    output_file = os.path.join(io_dir, "output.txt")
    
    # For LeetCode, format input differently
    if platform == Platform.LEETCODE:
        # Parse LeetCode test case format: "[2,7,11,15] 9"
        input_data = test_case.input_data.strip()
        
        # Convert LeetCode format to stdin format
        parts = input_data.split()
        formatted_input = ""
        
        for part in parts:
            if part.startswith('[') and part.endswith(']'):
                # Handle vector input - remove brackets and add as comma-separated line
                formatted_input += part + "\n"
            else:
                # Handle regular input
                formatted_input += part + "\n"
        
        # Write formatted input to file
        with open(input_file, 'w') as f:
            f.write(formatted_input.strip())
    else:
        # Write input to file for other platforms
        with open(input_file, 'w') as f:
            f.write(test_case.input_data)
    
    try:
        # Run the executable with time measurement
        start_time = time.time()
        
        # Use /usr/bin/time for detailed metrics
        time_cmd = ["/usr/bin/time", "-f", "%e %M", executable_path]
        
        with open(input_file, 'r') as stdin_file, open(output_file, 'w') as stdout_file:
            result = subprocess.run(
                time_cmd,
                stdin=stdin_file,
                stdout=stdout_file,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5  # 5 second timeout
            )
        
        execution_time = time.time() - start_time
        
        # Parse time and memory from stderr
        time_output = result.stderr.strip()
        try:
            parts = time_output.split()
            if len(parts) >= 2:
                exec_time_str = parts[0]
                memory_kb = parts[1]
                execution_time = float(exec_time_str)
                memory_used = f"{memory_kb} KB"
            else:
                memory_used = "N/A"
        except:
            memory_used = "N/A"
        
        # Read output
        with open(output_file, 'r') as f:
            actual_output = f.read().strip()
        
        # Compare outputs
        passed = actual_output == test_case.expected_output.strip()
        
        return TestResult(test_case, actual_output, passed, execution_time, memory_used)
        
    except subprocess.TimeoutExpired:
        return TestResult(test_case, "TIMEOUT", False, 5.0, "N/A")
    except Exception as e:
        return TestResult(test_case, f"ERROR: {str(e)}", False, 0.0, "N/A")

def parse_leetcode_method_signature(cpp_filepath: str) -> tuple:
    """Parse method signature from LeetCode C++ file"""
    with open(cpp_filepath, 'r') as f:
        content = f.read()
    
    # Find the method signature in the Solution class
    # Look for pattern: returnType methodName(parameters)
    method_pattern = r'class\s+Solution\s*\{[^}]*public:\s*([^{}]*?)\s*\{'
    match = re.search(method_pattern, content, re.DOTALL)
    
    if match:
        method_signature = match.group(1).strip()
        # Extract return type and method name
        parts = method_signature.split()
        if len(parts) >= 2:
            return_type = parts[0]
            method_part = parts[1]
            method_name = method_part.split('(')[0]
            
            # Extract full parameter list
            param_start = method_signature.find('(')
            param_end = method_signature.find(')')
            if param_start != -1 and param_end != -1:
                params = method_signature[param_start+1:param_end].strip()
                return return_type, method_name, params
    
    return "int", "solution", ""

def generate_leetcode_input_parser(return_type: str, method_name: str, params: str, test_cases: List[TestCase]) -> str:
    """Generate input parsing and method calling code for LeetCode"""
    # Analyze the first test case to understand input format
    if not test_cases:
        return ""
    
    sample_input = test_cases[0].input_data.strip()
    
    # Parse parameters to understand what inputs to expect
    param_types = []
    param_names = []
    
    if params:
        # Split parameters by comma
        param_list = [p.strip() for p in params.split(',')]
        for param in param_list:
            if param:
                parts = param.split()
                if len(parts) >= 2:
                    param_type = ' '.join(parts[:-1])  # Everything except last word
                    param_name = parts[-1].strip('&*')  # Remove reference/pointer symbols
                    param_types.append(param_type)
                    param_names.append(param_name)
    
    parsing_code = ""
    call_args = []
    
    # Simple parsing logic for common LeetCode patterns
    input_parts = sample_input.split()
    
    for i, (param_type, param_name) in enumerate(zip(param_types, param_names)):
        if "vector<int>" in param_type:
            parsing_code += f"""
    // Parse vector<int> {param_name}
    string line{i + 1};
    getline(cin, line{i + 1});
    
    // Remove brackets and parse numbers
    line{i + 1} = line{i + 1}.substr(1, line{i + 1}.length() - 2); // Remove [ and ]
    vector<int> {param_name};
    if (!line{i + 1}.empty()) {{
        stringstream ss{i + 1}(line{i + 1});
        string num{i + 1};
        while (getline(ss{i + 1}, num{i + 1}, ',')) {{
            {param_name}.push_back(stoi(num{i + 1}));
        }}
    }}
"""
            call_args.append(param_name)
        elif "vector<string>" in param_type:
            parsing_code += f"""
    // Parse vector<string> {param_name}
    string line{i + 1};
    getline(cin, line{i + 1});
    
    // Remove brackets and parse strings
    line{i + 1} = line{i + 1}.substr(1, line{i + 1}.length() - 2); // Remove [ and ]
    vector<string> {param_name};
    stringstream ss{i + 1}(line{i + 1});
    string str{i + 1};
    while (getline(ss{i + 1}, str{i + 1}, ',')) {{
        // Remove quotes if present
        if (str{i + 1}.front() == '"') str{i + 1} = str{i + 1}.substr(1, str{i + 1}.length() - 2);
        {param_name}.push_back(str{i + 1});
    }}
"""
            call_args.append(param_name)
        elif param_type == "int":
            parsing_code += f"""
    int {param_name};
    cin >> {param_name};
"""
            call_args.append(param_name)
        elif param_type == "string":
            parsing_code += f"""
    string {param_name};
    cin >> {param_name};
"""
            call_args.append(param_name)
        elif param_type == "bool":
            parsing_code += f"""
    bool {param_name};
    cin >> {param_name};
"""
            call_args.append(param_name)
        elif param_type == "char":
            parsing_code += f"""
    char {param_name};
    cin >> {param_name};
"""
            call_args.append(param_name)
        else:
            # Default handling for unknown types
            parsing_code += f"""
    // Parse {param_type} {param_name} (default handling)
    {param_type} {param_name};
    cin >> {param_name};
"""
            call_args.append(param_name)
    
    # Generate method call based on return type
    method_call = f"sol.{method_name}({', '.join(call_args)})"
    
    if return_type == "vector<int>":
        result_code = f"""
    vector<int> result = {method_call};
    cout << "[";
    for (int i = 0; i < result.size(); i++) {{
        if (i > 0) cout << ",";
        cout << result[i];
    }}
    cout << "]" << endl;
"""
    elif return_type == "vector<string>":
        result_code = f"""
    vector<string> result = {method_call};
    cout << "[";
    for (int i = 0; i < result.size(); i++) {{
        if (i > 0) cout << ",";
        cout << "\\"" << result[i] << "\\"";
    }}
    cout << "]" << endl;
"""
    elif return_type == "int":
        result_code = f"""
    int result = {method_call};
    cout << result << endl;
"""
    elif return_type == "double":
        result_code = f"""
    double result = {method_call};
    cout << fixed << setprecision(5) << result << endl;
"""
    elif return_type == "string":
        result_code = f"""
    string result = {method_call};
    cout << result << endl;
"""
    elif return_type == "bool":
        result_code = f"""
    bool result = {method_call};
    cout << (result ? "true" : "false") << endl;
"""
    elif return_type == "char":
        result_code = f"""
    char result = {method_call};
    cout << result << endl;
"""
    else:
        result_code = f"""
    auto result = {method_call};
    cout << result << endl;
"""
    
    return parsing_code + result_code

def create_leetcode_test_runner(cpp_filepath: str, test_cases: List[TestCase]) -> str:
    """Create temporary test runner for LeetCode problems"""
    workspace_root = str(Path(cpp_filepath).parent.parent)
    io_dir = os.path.join(workspace_root, "io")
    os.makedirs(io_dir, exist_ok=True)
    
    temp_file = os.path.join(io_dir, "temp_leetcode_runner.cpp")
    
    # Read original file to extract Solution class (without main function)
    with open(cpp_filepath, 'r') as f:
        original_content = f.read()
    
    # Remove any existing main function from original content
    main_pattern = r'int\s+main\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    original_content = re.sub(main_pattern, '', original_content, flags=re.DOTALL)
    
    # Parse method signature
    return_type, method_name, params = parse_leetcode_method_signature(cpp_filepath)
    
    # Generate input parsing and method calling code
    input_parser = generate_leetcode_input_parser(return_type, method_name, params, test_cases)
    
    # Create complete test runner
    test_runner_content = f"""// Temporary test runner for LeetCode
{original_content}

#include <sstream>
#include <iomanip>

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    Solution sol;
{input_parser}
    
    return 0;
}}
"""
    
    with open(temp_file, 'w') as f:
        f.write(test_runner_content)
    
    return temp_file

def display_results(results: List[TestResult], compilation_time: float = 0.0):
    """Display test results"""
    if not results:
        print("⚠️  No test cases found!")
        return
    
    passed_tests = sum(1 for r in results if r.passed)
    total_tests = len(results)
    
    print(f"\n📊 Test Results: {passed_tests}/{total_tests} passed")
    print("=" * 70)
    
    # Show each test result
    for result in results:
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"Test #{result.test_case.test_number}: {status} ({result.execution_time:.3f}s, {result.memory_used})")
        
        if not result.passed:
            print(f"  Input: {repr(result.test_case.input_data)}")
            print(f"  Expected: {repr(result.test_case.expected_output)}")
            print(f"  Actual: {repr(result.actual_output)}")
            print()
    
    # Performance summary
    if results:
        avg_time = sum(r.execution_time for r in results) / len(results)
        max_time = max(r.execution_time for r in results)
        
        print(f"⏱️  Performance: Avg {avg_time:.3f}s | Max {max_time:.3f}s", end="")
        if compilation_time > 0:
            print(f" | Compilation {compilation_time:.3f}s")
        else:
            print()

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 test_runner.py <filename> [compile_flags...]")
        sys.exit(1)
    
    filename = sys.argv[1]
    extra_flags = sys.argv[2:] if len(sys.argv) > 2 else []
    
    print_header()
    
    # Find workspace root
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Find C++ file
    cpp_filepath = find_cpp_file(filename, workspace_root)
    if not cpp_filepath:
        print(f"❌ C++ file '{filename}.cpp' not found in workspace!")
        sys.exit(1)
    
    # Detect platform
    platform = detect_platform(cpp_filepath)
    
    print(f"📂 Found: {cpp_filepath}")
    print(f"🏷️  Platform: {platform}")
    
    # Find test file
    test_filepath = find_test_file(cpp_filepath)
    if not test_filepath:
        print(f"⚠️  No test file found for {filename}")
        sys.exit(1)
    
    # Parse test cases
    test_cases = parse_test_cases(test_filepath, platform)
    if not test_cases:
        print(f"⚠️  No test cases found in {test_filepath}")
        sys.exit(1)
    
    print(f"📝 Found {len(test_cases)} test cases")
    
    # Handle LeetCode differently
    temp_cpp = None
    if platform == Platform.LEETCODE:
        # For LeetCode, create a temporary test runner
        temp_cpp = create_leetcode_test_runner(cpp_filepath, test_cases)
        compile_filepath = temp_cpp
    else:
        compile_filepath = cpp_filepath
    
    # Compile
    print("🔨 Compiling...")
    start_compile = time.time()
    compilation_result = compile_cpp(compile_filepath, extra_flags)
    compile_time = time.time() - start_compile
    
    if not compilation_result.success:
        print("❌ Compilation failed!")
        print("Compilation Error:")
        print(compilation_result.error_message)
        sys.exit(1)
    
    print(f"✅ Compilation successful! ({compile_time:.3f}s)")
    
    # Run tests
    print("🧪 Running tests...")
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  Running test {i}/{len(test_cases)}...", end=" ")
        result = run_test_case(compilation_result.executable_path, test_case, workspace_root, platform)
        results.append(result)
        status = "✅" if result.passed else "❌"
        print(f"{status} ({result.execution_time:.3f}s)")
    
    # Display results
    display_results(results, compile_time)
    
    # Clean up temporary files for LeetCode
    if platform == Platform.LEETCODE and temp_cpp is not None:
        try:
            os.remove(temp_cpp)
        except:
            pass

if __name__ == "__main__":
    main()
