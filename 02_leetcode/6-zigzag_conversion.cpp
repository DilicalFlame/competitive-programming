// LeetCode: https://leetcode.com/problems/zigzag-conversion/

#include <algorithm>
#include <string>
#include <vector>

using namespace std;

class Solution {
public:
  string convert(string s, int numRows) {
    if (numRows == 1)
      return s;

    int cycle = 2 * numRows - 2;
    vector<string> ss(numRows);
    int diff;

    for (int idx = 0; idx < s.length(); idx++) {
      char c = s[idx];
      int cycnum = idx % cycle;
      int ssidx = min(cycnum, cycle - cycnum);
      ss[ssidx] += c;
    }

    string ans = "";
    for (string l : ss)
      ans += l;

    return ans;
  }
};
