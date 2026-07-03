# LeetCode - 11-container_with_most_water

## Problem Description
You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `ith` line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return _the maximum amount of water a container can store_.

**Notice** that you may not slant the container.

**Example 1:**

![](https://s3-lc-upload.s3.amazonaws.com/uploads/2018/07/17/question_11.jpg)

**Input:** height = \[1,8,6,2,5,4,8,3,7\]
**Output:** 49
**Explanation:** The above vertical lines are represented by array \[1,8,6,2,5,4,8,3,7\]. In this case, the max area of water (blue section) the container can contain is 49.

**Example 2:**

**Input:** height = \[1,1\]
**Output:** 1

**Constraints:**

-   `n == height.length`
-   `2 <= n <= 105`
-   `0 <= height[i] <= 104`

## Test Cases

```tests
Function: maxArea
Sample Input: [1,8,6,2,5,4,8,3,7]
Sample Output: 49
---
Function: maxArea
Sample Input: [1,1]
Sample Output: 1
```

## Notes
- Input format: vector<int>& height
- Return type: int

> Following code is not wrong but it will exceed the time limit!

```cpp
#include <algorithm>
#include <vector>

using namespace std;

class Solution {
public:
  int maxArea(vector<int> &height) {
    long long int area = 0;
    for (int i = 0; i < size(height); i++) {
      for (int j = i + 1; j < size(height); j++) {
        int distance = j - i;
        long long int prod = min(height[i], height[j]) * distance;
        area = max(area, prod);
      }
    }
    return area;
  }
};
```
