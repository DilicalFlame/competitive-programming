# LeetCode - 3-longest_substring_without_repeating_chars

## Problem Description
Given a string `s`, find the length of the **longest** **substring** without duplicate characters.

**Example 1:**

**Input:** s = "abcabcbb"
**Output:** 3
**Explanation:** The answer is "abc", with the length of 3. Note that `"bca"` and `"cab"` are also correct answers.

**Example 2:**

**Input:** s = "bbbbb"
**Output:** 1
**Explanation:** The answer is "b", with the length of 1.

**Example 3:**

**Input:** s = "pwwkew"
**Output:** 3
**Explanation:** The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

**Constraints:**

-   `0 <= s.length <= 5 * 104`
-   `s` consists of English letters, digits, symbols and spaces.

## Test Cases

```tests
Function: lengthOfLongestSubstring
Sample Input: abcabcbb
Sample Output: 3
---
Function: lengthOfLongestSubstring
Sample Input: bbbbb
Sample Output: 1
---
Function: lengthOfLongestSubstring
Sample Input: pwwkew
Sample Output: 3
```

## Notes
- Input format: string s
- Return type: int

I wrote following solution at first which is wrong because the else block never executes!
Whenever something is searched in hash then, it just initialises it to zero and its always true here.

Also, I don't check if left_idx while updating it and it sometimes goes backward increasing the window size.
Finally! I don't update the character's index in the else block (which never executes anyway).

```cpp
#include <algorithm>
#include <map>
#include <string>

using namespace std;

class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    int answer = 0;

    if (s == "")
      return answer;

    map<char, int> hash{};
    int left_idx = 0;
    int right_idx = 0;

    for (right_idx = 0; s[right_idx] != '\0'; right_idx++) {
      if (!hash[s[right_idx]]) {
        hash[s[right_idx]]++;
      } else {
        left_idx = right_idx;
      }
      answer = max(right_idx - left_idx + 1, answer);
    }
    return answer;
  }
};
```
