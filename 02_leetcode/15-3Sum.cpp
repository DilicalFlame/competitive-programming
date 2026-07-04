// LeetCode:
// https://leetcode.com/problems/3sum/
//
// bug: can't run this code because my python logic doesn't know how to handle
// vector return types in c++

#include <algorithm>
#include <vector>

using namespace std;

class Solution {
public:
  vector<vector<int>> threeSum(vector<int> &nums) {
    vector<vector<int>> result;

    sort(nums.begin(), nums.end());

    for (auto i = 0; i < nums.size(); i++) {
      // skip duplicates: i
      if (i > 0 && nums[i] == nums[i - 1])
        continue;

      int left = i + 1;
      int right = nums.size() - 1;

      while (left < right) {
        int sum = nums[i] + nums[left] + nums[right];

        if (sum == 0) {
          result.push_back({nums[i], nums[left], nums[right]});
          // skip duplicates: left and right
          while (left < right && nums[left] == nums[left + 1])
            left++;
          while (left < right && nums[right] == nums[right - 1])
            right--;
          left++;
          right--;
        } else if (sum < 0) {
          // sum is small so increase the left
          left++;
        } else {
          // sum is big so decrease from right
          right--;
        }
      }
    }
    return result;
  }
};
