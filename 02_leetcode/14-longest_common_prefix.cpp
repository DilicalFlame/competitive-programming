// LeetCode:
// https://leetcode.com/problems/longest-common-prefix/description/?envType=problem-list-v2&envId=array

#include <string>
#include <vector>

using namespace std;

struct TrieNode {
  TrieNode *children[26]{};
  bool isEnd = false;
};

void insert_word(TrieNode *root, const string &word) {
  TrieNode *current = root;
  for (char c : word) {
    int idx = c - 'a';
    if (current->children[idx] == nullptr)
      current->children[idx] = new TrieNode();
    current = current->children[idx];
  }
  current->isEnd = true;
}

int count_children(TrieNode *node) {
  int count = 0;
  for (int i = 0; i < 26; i++) {
    if (node->children[i] != nullptr)
      count++;
  }
  return count;
}

class Solution {
public:
  string longestCommonPrefix(vector<string> &strs) {
    TrieNode *root = new TrieNode();
    string common;
    for (const string &w : strs)
      insert_word(root, w);
    TrieNode *current = root;
    while (count_children(current) == 1 && !current->isEnd) {
      for (int i = 0; i < 26; i++) {
        if (current->children[i] != nullptr) {
          common += char(i + 'a');
          current = current->children[i];
          break;
        }
      }
    }
    return common;
  }
};
