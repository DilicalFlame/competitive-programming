// LeetCode: https://leetcode.com/problems/two-sum/

#include <map>
#include <vector>

using namespace std;

class Solution {
public:
  vector<int> twoSum(vector<int> &nums, int target) {
    map<int, int> numToIndex;

    for (int i = 0; i < nums.size(); i++) {
      int complement = target - nums[i];

      if (numToIndex.find(complement) != numToIndex.end()) {
        return {numToIndex[complement], i};
      }

      numToIndex[nums[i]] = i;
    }

    return {};
  }
};
