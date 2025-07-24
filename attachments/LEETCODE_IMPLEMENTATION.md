# LeetCode Test Execution Implementation

## Overview

The LeetCode test execution feature has been fully implemented to support automated testing of LeetCode problems with the following capabilities:

## Features Implemented

### 1. Template Generation Without Main Function

- LeetCode C++ files are generated with only the `Solution` class
- No `main()` function is included in the source code
- Clean template focused on the solution implementation

### 2. Intelligent Method Signature Detection

- Automatically parses the `Solution` class method signature
- Extracts return type, method name, and parameters
- Supports various data types: `int`, `double`, `string`, `bool`, `vector<int>`, `vector<string>`, etc.

### 3. Dynamic Test Runner Generation

- Creates temporary C++ files in the `io/` folder
- Generates appropriate input parsing code based on parameter types
- Handles multiple vectors and different data types
- Automatically formats output based on return type

### 4. Smart Input Format Conversion

- Converts LeetCode test format to stdin-compatible format
- Example: `[2,7,11,15] 9` → separate lines for vector and integer
- Supports multiple vectors: `[1,3] [2]` → two separate vector inputs

### 5. Comprehensive Test Case Support

- Parses LeetCode-specific test case format from markdown files
- Supports multiple test cases separated by `---`
- Validates output format and provides detailed feedback

## Usage Examples

### Creating a New LeetCode Problem

```bash
./create
# Select LeetCode platform
# Enter filename: two-sum
# Enter method name: twoSum
# Enter return type: vector<int>
# Enter parameters: vector<int>& nums, int target
```

### Generated Template

```cpp
// LeetCode: paste link to problem here

#include <iostream>
#include <vector>
// ... other includes

using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Your code here

    }
};
```

### Test Case Format

````markdown
# LeetCode - two-sum

## Test Cases

```tests
Function: twoSum
Sample Input: [2,7,11,15] 9
Sample Output: [0,1]
---
Function: twoSum
Sample Input: [3,2,4] 6
Sample Output: [1,2]
```
````

````

### Running Tests

```bash
./run two-sum
````

## Supported Data Types

### Input Parameters

- `vector<int>`: Parsed from `[1,2,3]` format
- `vector<string>`: Parsed from `["hello","world"]` format
- `int`: Direct integer input
- `string`: Direct string input
- `bool`: Boolean values
- `char`: Single character input

### Return Types

- `vector<int>`: Output as `[1,2,3]`
- `vector<string>`: Output as `["hello","world"]`
- `int`: Direct integer output
- `double`: Formatted with 5 decimal places
- `string`: Direct string output
- `bool`: Output as `true`/`false`
- `char`: Single character output

## Technical Implementation

### 1. Method Signature Parsing

```python
def parse_leetcode_method_signature(cpp_filepath: str) -> tuple:
    # Regex pattern to extract method from Solution class
    method_pattern = r'class\s+Solution\s*\{[^}]*public:\s*([^{}]*?)\s*\{'
    # Parse return type, method name, and parameters
```

### 2. Dynamic Input Parser Generation

```python
def generate_leetcode_input_parser(return_type: str, method_name: str, params: str, test_cases: List[TestCase]) -> str:
    # Generates appropriate parsing code based on parameter types
    # Creates method call with correct arguments
    # Formats output based on return type
```

### 3. Temporary Test Runner Creation

```python
def create_leetcode_test_runner(cpp_filepath: str, test_cases: List[TestCase]) -> str:
    # Removes existing main function from original code
    # Adds necessary includes (sstream, iomanip)
    # Generates complete test runner with input parsing and output formatting
```

## Advanced Features

### Multiple Vector Support

Handles problems with multiple vector parameters:

```cpp
double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2)
```

Test case format:

```
Sample Input: [1,3] [2]
Sample Output: 2.00000
```

### Precision Handling

For `double` return types, output is formatted with 5 decimal places using `setprecision(5)`.

### Error Handling

- Compilation errors are reported with detailed messages
- Runtime errors and timeouts are handled gracefully
- Memory usage tracking for performance analysis

## File Structure

```
02_leetcode/
├── problem-name.cpp          # Solution file (no main function)
├── tests/
│   └── problem-name.md       # Test cases in LeetCode format
└── out/
    └── problem-name          # Compiled executable (temporary)

io/
├── temp_leetcode_runner.cpp  # Generated test runner (temporary)
├── input.txt                 # Formatted input for current test
└── output.txt               # Program output for comparison
```

## Benefits

1. **Clean Code**: Source files contain only the solution logic
2. **Automated Testing**: No need to manually write test harnesses
3. **Multiple Test Cases**: Run all test cases with a single command
4. **Performance Metrics**: Execution time and memory usage tracking
5. **Type Safety**: Intelligent parsing based on actual method signatures
6. **Format Conversion**: Seamless conversion between LeetCode and stdin formats

## Integration with VS Code

The implementation integrates seamlessly with VS Code tasks:

- **Build Task**: Compiles the solution
- **Test Task**: Runs all test cases
- **Debug Task**: Runs with debug flags

This implementation provides a complete, production-ready solution for competitive programming on LeetCode with automated test execution and comprehensive error handling.
