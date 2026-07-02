// LeetCode:
// https://leetcode.com/problems/median-of-two-sorted-arrays/?envType=problem-list-v2&envId=array

#include <algorithm>
#include <cmath>
#include <vector>

using namespace std;

class Solution {
public:
  double findMedianSortedArrays(vector<int> &nums1, vector<int> &nums2) {
    double result;
    int nums1_len = nums1.size();
    int nums2_len = nums2.size();

    nums1.insert(nums1.end(), nums2.begin(), nums2.end());
    sort(nums1.begin(), nums1.end());
    if ((nums1_len + nums2_len) % 2 == 0) {
      result = (nums1[floor(nums1.size() / 2.0) - 1] +
                nums1[floor(nums1.size() / 2.0)]) /
               2.0;
    } else {
      result = nums1[floor(nums1.size() / 2.0)];
    }

    return result;
  }
};
