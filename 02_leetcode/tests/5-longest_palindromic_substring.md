# LeetCode - 5-longest_palindromic_substring

## Problem Description
Given a string `s`, return _the longest_ _palindromic_ _substring_ in `s`.

**Example 1:**

**Input:** s = "babad"
**Output:** "bab"
**Explanation:** "aba" is also a valid answer.

**Example 2:**

**Input:** s = "cbbd"
**Output:** "bb"

**Constraints:**

-   `1 <= s.length <= 1000`
-   `s` consist of only digits and English letters.

## Test Cases

```tests
Function: longestPalindrome
Sample Input: babad
Sample Output: aba
---
Function: longestPalindrome
Sample Input: cbbd
Sample Output: bb
```

## Notes
- Input format: string s
- Return type: string

study following solution later:

```cpp
class Solution {
public:
    string longestPalindrome(string s) {

        if (s.empty())
            return "";

        // Step 1 : Preprocess
        string t = "#";
        for(char c : s){
            t += c;
            t += '#';
        }

        int n = t.size();

        vector<int> p(n,0);

        int center = 0;
        int right = 0;

        int bestCenter = 0;
        int bestRadius = 0;
        cout<<t<<endl;

        for(int i=0;i<n;i++){

            int mirror = 2*center - i;

            // Step 2 : Copy radius if inside current palindrome
            if(i < right)
            {
                // we have to check for the current palindrome, we only have information till right after that we dont know so we assign p[i]=min(right-i,p[mirror]) later we can expand right. and we dont write right-i because in palindrome if we have found p[mirror] and i is in current palindrome then that means i will have same radius as of mirror but we have information till right so we assign min
                 p[i] = min(right-i,p[mirror]);
            }
               


            // Step 3 : Expand
            while(i-p[i]-1>=0 &&
                  i+p[i]+1<n &&
                  t[i-p[i]-1]==t[i+p[i]+1])
            {

                p[i]++;
            }

            // Step 4 : Update current palindrome
            if(i+p[i] > right){
                center = i;
                right = i+p[i];
            }

            // Step 5 : Store answer
            if(p[i] > bestRadius){
                bestRadius = p[i];
                bestCenter = i;
            }
        }

        int start = (bestCenter-bestRadius)/2;

        return s.substr(start,bestRadius);
    }
};
```
