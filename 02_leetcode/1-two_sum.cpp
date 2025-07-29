// LeetCode: paste link to problem here

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <deque>
#include <cmath>
#include <climits>

using namespace std;

class Solution
{
public:
    vector<int> twoSum(vector<int> &nums, int target)
    {
        map<int, int> numToIndex;

        for (int i = 0; i < nums.size(); i++)
        {
            int complement = target - nums[i];

            // Check if complement exists in the map
            if (numToIndex.find(complement) != numToIndex.end())
            {
                return {numToIndex[complement], i};
            }

            // Store current number and its index
            numToIndex[nums[i]] = i;
        }

        // Should never reach here based on problem constraints
        return {};
    }
};
