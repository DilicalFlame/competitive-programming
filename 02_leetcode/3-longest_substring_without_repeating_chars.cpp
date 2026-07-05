// LeetCode:
// https://leetcode.com/problems/longest-substring-without-repeating-characters/

#include <algorithm>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    int answer = 0;

    if (s == "")
      return answer;

    unordered_map<char, int> hashIdx{};
    int left_idx = 0;

    for (int right_idx = 0; right_idx < s.length(); right_idx++) {
      char current_char = s[right_idx];
      if (hashIdx.count(current_char) > 0 &&
          hashIdx[current_char] >= left_idx) {
        left_idx = hashIdx[current_char] + 1;
      }
      hashIdx[current_char] = right_idx;
      answer = max(right_idx - left_idx + 1, answer);
    }
    return answer;
  }
};
