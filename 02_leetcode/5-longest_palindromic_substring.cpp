// LeetCode: https://leetcode.com/problems/longest-palindromic-substring/
// bug: I don't know why, do you need operator overloading to print string ?! my
// python runner doesn't know how to run this code.

#include <string>
#include <vector>

using namespace std;

class Solution {
public:
  vector<int> panlindromeCheck(const string &s, int lidx, int ridx) {
    while (lidx >= 0 && ridx < s.length() && s[lidx] == s[ridx]) {
      lidx--;
      ridx++;
    }
    return {lidx + 1, ridx - 1};
  }

  string longestPalindrome(const string s) {
    string palindrome = "";

    if (s == "")
      return palindrome;

    for (int i = 0; i < s.length(); i++) {
      vector<int> v1 = panlindromeCheck(s, i, i);
      vector<int> v2 = panlindromeCheck(s, i, i + 1);
      string substr1 = s.substr(v1[0], v1[1] - v1[0] + 1);
      string substr2 = s.substr(v2[0], v2[1] - v2[0] + 1);
      if (palindrome.length() < substr1.length()) {
        palindrome = substr1;
      }
      if (palindrome.length() < substr2.length()) {
        palindrome = substr2;
      }
    }
    // palindrome.length() == 1 ? palindrome = "" : palindrome;
    return palindrome;
  }
};
