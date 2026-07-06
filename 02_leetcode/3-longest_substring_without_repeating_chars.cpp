// LeetCode:
// https://leetcode.com/problems/longest-substring-without-repeating-characters/

#include <algorithm>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    int ans = 0;

    if (s == "")
      return ans;

    // character to index mapping
    unordered_map<char, int> cidx{};
    int lidx = 0;

    for (int ridx = 0; ridx < s.length(); ridx++) {
      char c = s[ridx];
      if (cidx.count(c) > 0 && cidx[c] >= lidx) {
        lidx = cidx[c] + 1;
      }
      cidx[c] = ridx;
      ans = max(ridx - lidx + 1, ans);
    }
    return ans;
  }
};
