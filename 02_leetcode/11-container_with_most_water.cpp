// LeetCode:
// https://leetcode.com/problems/container-with-most-water/?envType=problem-list-v2&envId=array

#include <algorithm>
#include <iterator>
#include <vector>

using namespace std;

class Solution {
public:
  int maxArea(vector<int> &height) {
    long long int area = 0;
    int distance;
    long long int prod;

    int left = 0;
    int right = size(height) - 1;

    while (left < right) {
      distance = right - left;
      prod = min(height[left], height[right]) * distance;
      area = max(area, prod);
      height[left] < height[right] ? left++ : right--;
    }
    return area;
  }
};
