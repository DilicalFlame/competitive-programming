# LeetCode - 6-zigzag_conversion

## Problem Description
The string `"PAYPALISHIRING"` is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R

And then read line by line: `"PAHNAPLSIIGYIR"`

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);

**Example 1:**

**Input:** s = "PAYPALISHIRING", numRows = 3
**Output:** "PAHNAPLSIIGYIR"

**Example 2:**

**Input:** s = "PAYPALISHIRING", numRows = 4
**Output:** "PINALSIGYAHRPI"
**Explanation:**
P     I    N
A   L S  I G
Y A   H R
P     I

**Example 3:**

**Input:** s = "A", numRows = 1
**Output:** "A"

**Constraints:**

-   `1 <= s.length <= 1000`
-   `s` consists of English letters (lower-case and upper-case), `','` and `'.'`.
-   `1 <= numRows <= 1000`

## Test Cases

```tests
Function: convert
Sample Input: PAYPALISHIRING 3
Sample Output: PAHNAPLSIIGYIR
---
Function: convert
Sample Input: PAYPALISHIRING 4
Sample Output: PINALSIGYAHRPI
```

## Notes
- Input format: string s, int numRows
- Return type: string

study following solution later:

```cpp
class Solution {
public:
    string convert(string s, int numRows) {
        // handle single row
        if (numRows == 1) return s;

        string ret_s = "";
        for (int i = 0; i < numRows; i++) {
            int index = i;
            bool top_row = (i == 0);
            bool last_row = (i == numRows - 1);
            bool dir = !last_row; // true: down, false: up

            while (index < s.length()) {
                ret_s += s[index];

                if (dir) {
                    index += 2*(numRows - i - 1);
                } else {
                    index += 2*i;
                }
                
                if (!(last_row || top_row)) dir = !dir;
            }
        }
        return ret_s;
    }
};
```
