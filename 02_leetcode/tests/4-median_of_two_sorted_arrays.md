# LeetCode - 4-median_of_two_sorted_arrays

## Problem Description
Given an array of integers `nums` and an integer `target`, return _indices of the two numbers such that they add up to `target`_.

You may assume that each input would have **_exactly_ one solution**, and you may not use the _same_ element twice.

You can return the answer in any order.

**Example 1:**

**Input:** nums = \[2,7,11,15\], target = 9
**Output:** \[0,1\]
**Explanation:** Because nums\[0\] + nums\[1\] == 9, we return \[0, 1\].

**Example 2:**

**Input:** nums = \[3,2,4\], target = 6
**Output:** \[1,2\]

**Example 3:**

**Input:** nums = \[3,3\], target = 6
**Output:** \[0,1\]

**Constraints:**

-   `2 <= nums.length <= 104`
-   `-109 <= nums[i] <= 109`
-   `-109 <= target <= 109`
-   **Only one valid answer exists.**

## Test Cases

```tests
Function: findMedianSortedArrays
Sample Input: [1,3] [2]
Sample Output: 2.00000
---
Function: findMedianSortedArrays
Sample Input: [1,2] [3,4]
Sample Output: 2.50000
```

## Notes
- Input format: vector<int>& nums1, vector<int>& nums2
- Return type: double

if you divide two integers, you get an integer.
To bypass this, suffix any integer with .0 to make it a floating point division.
