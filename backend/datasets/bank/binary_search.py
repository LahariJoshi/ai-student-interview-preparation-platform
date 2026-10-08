"""
binary_search.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.",
        "constraints": "1 <= nums.length <= 10^4\n-10^4 < nums[i], target < 10^4\nAll integers in nums are unique.\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Compare target with middle element and halve search space."
        ],
        "starter_code": {
            "python": "def search(nums: list[int], target: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function search(nums, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int search(int[] nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[-1, 0, 3, 5, 9, 12]\n9",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "9 exists in nums and its index is 4."
            },
            {
                "input_data": "[-1, 0, 3, 5, 9, 12]\n2",
                "expected_output": "-1",
                "is_sample": True,
                "explanation": "2 does not exist in nums so return -1."
            },
            {
                "input_data": "[5]\n5",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Single item found at index 0."
            }
        ]
    },
    {
        "title": "Search Insert Position",
        "slug": "search-insert-position",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.",
        "constraints": "1 <= nums.length <= 10^4\n-10^4 <= nums[i], target <= 10^4\nnums is sorted in ascending order.\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Standard binary search: return `low` when search terminates."
        ],
        "starter_code": {
            "python": "def searchInsert(nums: list[int], target: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function searchInsert(nums, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int searchInsert(int[] nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int searchInsert(vector<int>& nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 3, 5, 6]\n5",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "5 found at index 2."
            },
            {
                "input_data": "[1, 3, 5, 6]\n2",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "2 inserted at index 1."
            },
            {
                "input_data": "[1, 3, 5, 6]\n7",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "Inserted at end index 4."
            }
        ]
    },
    {
        "title": "Sqrt(x)",
        "slug": "sqrtx",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest integer. The returned integer should be non-negative as well.",
        "constraints": "0 <= x <= 2^31 - 1\nOptimal Time: O(log x), Space: O(1)",
        "hints": [
            "Binary search between 0 and x."
        ],
        "starter_code": {
            "python": "def mySqrt(x: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function mySqrt(x) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int mySqrt(int x) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int mySqrt(int x) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "4",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Square root of 4 is 2."
            },
            {
                "input_data": "8",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Square root of 8 is 2.82842..., rounded down to 2."
            },
            {
                "input_data": "0",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Sqrt of 0 is 0."
            }
        ]
    },
    {
        "title": "Peak Index in a Mountain Array",
        "slug": "peak-index-in-a-mountain-array",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "An array `arr` is a mountain if it increases then decreases. Return the index of the peak element in `O(log n)` time.",
        "constraints": "3 <= arr.length <= 10^5\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Compare arr[mid] with arr[mid + 1]."
        ],
        "starter_code": {
            "python": "def peakIndexInMountainArray(arr: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function peakIndexInMountainArray(arr) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int peakIndexInMountainArray(int[] arr) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int peakIndexInMountainArray(vector<int>& arr) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[0, 1, 0]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Peak index is 1."
            },
            {
                "input_data": "[0, 2, 1, 0]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Peak index is 1."
            },
            {
                "input_data": "[0, 10, 5, 2]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Peak is 10 at index 1."
            }
        ]
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "Given a rotated sorted array `nums` with unique elements, find the index of `target`, or return `-1` if it is not in `nums`.",
        "constraints": "1 <= nums.length <= 5000\n-10^4 <= nums[i] <= 10^4\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Determine which half is sorted, then check if target lies within that range."
        ],
        "starter_code": {
            "python": "def searchRotated(nums: list[int], target: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function searchRotated(nums, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int searchRotated(int[] nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int searchRotated(vector<int>& nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[4, 5, 6, 7, 0, 1, 2]\n0",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "0 is at index 4."
            },
            {
                "input_data": "[4, 5, 6, 7, 0, 1, 2]\n3",
                "expected_output": "-1",
                "is_sample": True,
                "explanation": "3 is not found."
            },
            {
                "input_data": "[1]\n0",
                "expected_output": "-1",
                "is_sample": False,
                "explanation": "Single item not matching."
            }
        ]
    },
    {
        "title": "Find Peak Element",
        "slug": "find-peak-element",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "A peak element is an element that is strictly greater than its neighbors. Find a peak element and return its index.",
        "constraints": "1 <= nums.length <= 1000\n-2^31 <= nums[i] <= 2^31 - 1\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "If nums[mid] > nums[mid + 1], peak is in left half (including mid)."
        ],
        "starter_code": {
            "python": "def findPeakElement(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findPeakElement(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findPeakElement(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findPeakElement(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 1]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "3 is peak at index 2."
            },
            {
                "input_data": "[1, 2, 1, 3, 5, 6, 4]",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "Index 5 (value 6) is a peak."
            },
            {
                "input_data": "[1]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Single element is peak."
            }
        ]
    },
    {
        "title": "Search a 2D Matrix",
        "slug": "search-a-2d-matrix",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "You are given an `m x n` integer matrix with properties: each row is sorted, and the first integer of each row is greater than the last integer of the previous row. Return `True` if `target` is in `matrix`.",
        "constraints": "1 <= m, n <= 100\n-10^4 <= matrix[i][j], target <= 10^4\nOptimal Time: O(log(m * n)), Space: O(1)",
        "hints": [
            "Treat matrix as a flattened array of size m * n."
        ],
        "starter_code": {
            "python": "def searchMatrix(matrix: list[list[int]], target: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function searchMatrix(matrix, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean searchMatrix(int[][] matrix, int target) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool searchMatrix(vector<vector<int>>& matrix, int target) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]\n3",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "3 is found."
            },
            {
                "input_data": "[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]\n13",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "13 not in matrix."
            },
            {
                "input_data": "[[1]]\n1",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Single item 1 found."
            }
        ]
    },
    {
        "title": "Koko Eating Bananas",
        "slug": "koko-eating-bananas",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "Koko loves to eat bananas. There are `n` piles of bananas. She can eat at speed `k` bananas per hour. Return the minimum integer `k` such that she can eat all the bananas within `h` hours.",
        "constraints": "1 <= piles.length <= 10^4\npiles.length <= h <= 10^9\n1 <= piles[i] <= 10^9\nOptimal Time: O(n log(max(piles))), Space: O(1)",
        "hints": [
            "Binary search on eating speed k between 1 and max(piles)."
        ],
        "starter_code": {
            "python": "def minEatingSpeed(piles: list[int], h: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function minEatingSpeed(piles, h) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int minEatingSpeed(int[] piles, int h) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int minEatingSpeed(vector<int>& piles, int h) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 6, 7, 11]\n8",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Speed 4 eats in 8 hours."
            },
            {
                "input_data": "[30, 11, 23, 4, 20]\n5",
                "expected_output": "30",
                "is_sample": True,
                "explanation": "Speed 30."
            },
            {
                "input_data": "[30, 11, 23, 4, 20]\n6",
                "expected_output": "23",
                "is_sample": False,
                "explanation": "Speed 23."
            }
        ]
    },
    {
        "title": "Capacity To Ship Packages Within D Days",
        "slug": "capacity-to-ship-packages-within-d-days",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "A conveyor belt has packages that must be shipped within `days` days. Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days.",
        "constraints": "1 <= days <= weights.length <= 5 * 10^4\n1 <= weights[i] <= 500\nOptimal Time: O(n log(sum(weights))), Space: O(1)",
        "hints": [
            "Binary search on capacity between max(weights) and sum(weights)."
        ],
        "starter_code": {
            "python": "def shipWithinDays(weights: list[int], days: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function shipWithinDays(weights, days) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int shipWithinDays(int[] weights, int days) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int shipWithinDays(vector<int>& weights, int days) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n5",
                "expected_output": "15",
                "is_sample": True,
                "explanation": "Capacity 15 ships in 5 days."
            },
            {
                "input_data": "[3, 2, 2, 4, 1, 4]\n3",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "Capacity 6 ships in 3 days."
            },
            {
                "input_data": "[1, 2, 3, 1, 1]\n4",
                "expected_output": "3",
                "is_sample": False,
                "explanation": "Capacity 3."
            }
        ]
    },
    {
        "title": "Single Element in a Sorted Array",
        "slug": "single-element-in-a-sorted-array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once. Return the single element in `O(log n)` time and `O(1)` space.",
        "constraints": "1 <= nums.length <= 10^5\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Before the single element, pairs start at even indices."
        ],
        "starter_code": {
            "python": "def singleNonDuplicate(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function singleNonDuplicate(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int singleNonDuplicate(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int singleNonDuplicate(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 1, 2, 3, 3, 4, 4, 8, 8]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 is the single element."
            },
            {
                "input_data": "[3, 3, 7, 7, 10, 11, 11]",
                "expected_output": "10",
                "is_sample": True,
                "explanation": "10 appears once."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single item."
            }
        ]
    },
    {
        "title": "Split Array Largest Sum",
        "slug": "split-array-largest-sum",
        "topic": "Binary Search",
        "difficulty": "Hard",
        "description": "Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty subarrays such that the largest sum of any subarray is minimized. Return the minimized largest sum.",
        "constraints": "1 <= nums.length <= 1000\n0 <= nums[i] <= 10^6\n1 <= k <= min(50, nums.length)\nOptimal Time: O(n log(sum)), Space: O(1)",
        "hints": [
            "Binary search on the answer between max(nums) and sum(nums)."
        ],
        "starter_code": {
            "python": "def splitArray(nums: list[int], k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function splitArray(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int splitArray(int[] nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int splitArray(vector<int>& nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[7, 2, 5, 10, 8]\n2",
                "expected_output": "18",
                "is_sample": True,
                "explanation": "Best split: [7, 2, 5] (14) and [10, 8] (18)."
            },
            {
                "input_data": "[1, 2, 3, 4, 5]\n2",
                "expected_output": "9",
                "is_sample": True,
                "explanation": "[1, 2, 3] (6) and [4, 5] (9)."
            },
            {
                "input_data": "[1, 4, 4]\n3",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "Split each into its own subarray."
            }
        ]
    },
    {
        "title": "Find in Mountain Array",
        "slug": "find-in-mountain-array",
        "topic": "Binary Search",
        "difficulty": "Hard",
        "description": "Given a mountain array `arr` and a `target`, return the minimum index such that `arr[index] == target`. If such an index does not exist, return `-1`.",
        "constraints": "3 <= arr.length <= 10^4\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Find peak index first, then binary search on ascending slope, then descending slope."
        ],
        "starter_code": {
            "python": "def findInMountainArray(target: int, arr: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findInMountainArray(target, arr) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findInMountainArray(int target, int[] arr) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findInMountainArray(int target, vector<int>& arr) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "3\n[1, 2, 3, 4, 5, 3, 1]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "3 appears at index 2 and index 5; min index is 2."
            },
            {
                "input_data": "3\n[0, 1, 2, 4, 2, 1]",
                "expected_output": "-1",
                "is_sample": True,
                "explanation": "3 is not in array."
            },
            {
                "input_data": "0\n[0, 5, 3, 1]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "0 at start."
            }
        ]
    }
]
