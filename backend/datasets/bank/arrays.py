"""
arrays.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists.\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Use a hash map to look up if (target - current_number) has already been seen.",
            "Map each number to its index as you iterate."
        ],
        "starter_code": {
            "python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function twoSum(nums, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 7, 11, 15]\n9",
                "expected_output": "[0, 1]",
                "is_sample": True,
                "explanation": "nums[0] + nums[1] == 9, so return [0, 1]."
            },
            {
                "input_data": "[3, 2, 4]\n6",
                "expected_output": "[1, 2]",
                "is_sample": True,
                "explanation": "nums[1] + nums[2] == 6, so return [1, 2]."
            },
            {
                "input_data": "[3, 3]\n6",
                "expected_output": "[0, 1]",
                "is_sample": False,
                "explanation": "Duplicates summing to target."
            },
            {
                "input_data": "[-1, -2, -3, -4, -5]\n-8",
                "expected_output": "[2, 4]",
                "is_sample": False,
                "explanation": "Negative integers."
            },
            {
                "input_data": "[0, 4, 3, 0]\n0",
                "expected_output": "[0, 3]",
                "is_sample": False,
                "explanation": "Zeroes."
            }
        ]
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.",
        "constraints": "1 <= prices.length <= 10^5\n0 <= prices[i] <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Track the lowest buying price seen so far.",
            "Compare selling on the current day against the recorded max profit."
        ],
        "starter_code": {
            "python": "def maxProfit(prices: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxProfit(prices) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[7, 1, 5, 3, 6, 4]",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "Buy at 1, sell at 6."
            },
            {
                "input_data": "[7, 6, 4, 3, 1]",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "Prices decrease, profit 0."
            },
            {
                "input_data": "[1, 2]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Two elements."
            },
            {
                "input_data": "[2, 4, 1]",
                "expected_output": "2",
                "is_sample": False,
                "explanation": "Minimum at end."
            },
            {
                "input_data": "[3, 2, 6, 5, 0, 3]",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "Multiple swings."
            }
        ]
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct.",
        "constraints": "1 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Use a set to store visited elements."
        ],
        "starter_code": {
            "python": "def containsDuplicate(nums: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function containsDuplicate(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean containsDuplicate(int[] nums) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool containsDuplicate(vector<int>& nums) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 1]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "1 appears twice."
            },
            {
                "input_data": "[1, 2, 3, 4]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "All distinct."
            },
            {
                "input_data": "[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Many duplicates."
            },
            {
                "input_data": "[42]",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Single item."
            },
            {
                "input_data": "[0, 0]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Two identical zeroes."
            }
        ]
    },
    {
        "title": "Remove Duplicates from Sorted Array",
        "slug": "remove-duplicates-from-sorted-array",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given an integer array `nums` sorted in non-decreasing order, remove duplicates in-place so that each unique element appears only once.\n\nReturn the number of unique elements `k`.",
        "constraints": "1 <= nums.length <= 3 * 10^4\n-100 <= nums[i] <= 100\nnums is sorted.\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Maintain a slow pointer for the position of the last unique element."
        ],
        "starter_code": {
            "python": "def removeDuplicates(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function removeDuplicates(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int removeDuplicates(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int removeDuplicates(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 1, 2]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "[1, 2] unique."
            },
            {
                "input_data": "[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "5 unique numbers."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "One element."
            },
            {
                "input_data": "[1, 2, 3, 4, 5]",
                "expected_output": "5",
                "is_sample": False,
                "explanation": "No duplicates."
            }
        ]
    },
    {
        "title": "Move Zeroes",
        "slug": "move-zeroes",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements in-place.",
        "constraints": "1 <= nums.length <= 10^4\n-2^31 <= nums[i] <= 2^31 - 1\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use a pointer to overwrite non-zero elements toward the front, then fill remaining slots with zeroes."
        ],
        "starter_code": {
            "python": "def moveZeroes(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function moveZeroes(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] moveZeroes(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> moveZeroes(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[0, 1, 0, 3, 12]",
                "expected_output": "[1, 3, 12, 0, 0]",
                "is_sample": True,
                "explanation": "Zeroes shifted to back."
            },
            {
                "input_data": "[0]",
                "expected_output": "[0]",
                "is_sample": True,
                "explanation": "Single zero."
            },
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "[1, 2, 3]",
                "is_sample": False,
                "explanation": "No zeroes."
            },
            {
                "input_data": "[0, 0, 1]",
                "expected_output": "[1, 0, 0]",
                "is_sample": False,
                "explanation": "Leading zeroes."
            }
        ]
    },
    {
        "title": "Majority Element",
        "slug": "majority-element",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an array `nums` of size `n`, return the majority element that appears more than `\u230an / 2\u230b` times.",
        "constraints": "1 <= nums.length <= 5 * 10^4\n-10^9 <= nums[i] <= 10^9\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use Boyer-Moore Voting algorithm with candidate and count."
        ],
        "starter_code": {
            "python": "def majorityElement(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function majorityElement(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int majorityElement(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int majorityElement(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 2, 3]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 is majority."
            },
            {
                "input_data": "[2, 2, 1, 1, 1, 2, 2]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 appears 4 times."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single item."
            },
            {
                "input_data": "[6, 5, 5]",
                "expected_output": "5",
                "is_sample": False,
                "explanation": "5 is majority."
            }
        ]
    },
    {
        "title": "Valid Palindrome",
        "slug": "valid-palindrome",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `True` if it is a palindrome, or `False` otherwise.",
        "constraints": "1 <= s.length <= 2 * 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Two pointers inward from both ends."
        ],
        "starter_code": {
            "python": "def isPalindrome(s: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isPalindrome(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isPalindrome(String s) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isPalindrome(string s) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"A man, a plan, a canal: Panama\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Is palindrome."
            },
            {
                "input_data": "\"race a car\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Not a palindrome."
            },
            {
                "input_data": "\" \"",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Empty alphanumeric."
            },
            {
                "input_data": "\"0P\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Not equal."
            }
        ]
    },
    {
        "title": "Squares of a Sorted Array",
        "slug": "squares-of-a-sorted-array",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given an integer array `nums` sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.",
        "constraints": "1 <= nums.length <= 10^4\n-10^4 <= nums[i] <= 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Use two pointers at the start and end of nums to place the largest square at the end of the output."
        ],
        "starter_code": {
            "python": "def sortedSquares(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function sortedSquares(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] sortedSquares(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> sortedSquares(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[-4, -1, 0, 3, 10]",
                "expected_output": "[0, 1, 9, 16, 100]",
                "is_sample": True,
                "explanation": "Squares in sorted order."
            },
            {
                "input_data": "[-7, -3, 2, 3, 11]",
                "expected_output": "[4, 9, 9, 49, 121]",
                "is_sample": True,
                "explanation": "Squares."
            },
            {
                "input_data": "[-1]",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "One element."
            },
            {
                "input_data": "[0, 2, 3]",
                "expected_output": "[0, 4, 9]",
                "is_sample": False,
                "explanation": "Non-negative."
            }
        ]
    },
    {
        "title": "Find All Numbers Disappeared in an Array",
        "slug": "find-all-numbers-disappeared-in-an-array",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an array `nums` of `n` integers where `nums[i]` is in the range `[1, n]`, return an array of all the integers in `[1, n]` that do not appear in `nums`.",
        "constraints": "1 <= n <= 10^5\nOptimal Time: O(n), Space: O(1) auxiliary",
        "hints": [
            "Use the sign of nums[abs(x) - 1] as a boolean flag for presence."
        ],
        "starter_code": {
            "python": "def findDisappearedNumbers(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findDisappearedNumbers(nums) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> findDisappearedNumbers(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findDisappearedNumbers(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[4, 3, 2, 7, 8, 2, 3, 1]",
                "expected_output": "[5, 6]",
                "is_sample": True,
                "explanation": "5 and 6 are missing."
            },
            {
                "input_data": "[1, 1]",
                "expected_output": "[2]",
                "is_sample": True,
                "explanation": "2 missing."
            },
            {
                "input_data": "[1]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "None missing."
            }
        ]
    },
    {
        "title": "Maximum Average Subarray I",
        "slug": "maximum-average-subarray-i",
        "topic": "Sliding Window",
        "difficulty": "Easy",
        "description": "You are given an integer array `nums` consisting of `n` elements, and an integer `k`.\n\nFind a contiguous subarray whose length is equal to `k` that has the maximum average value and return this value.",
        "constraints": "1 <= k <= n <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Maintain a running sum of length k."
        ],
        "starter_code": {
            "python": "def findMaxAverage(nums: list[int], k: int) -> float:\n    # Write your solution here\n    pass\n",
            "javascript": "function findMaxAverage(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public double findMaxAverage(int[] nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    double findMaxAverage(vector<int>& nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 12, -5, -6, 50, 3]\n4",
                "expected_output": "12.75",
                "is_sample": True,
                "explanation": "51 / 4 = 12.75."
            },
            {
                "input_data": "[5]\n1",
                "expected_output": "5.0",
                "is_sample": True,
                "explanation": "Single item 5.0."
            },
            {
                "input_data": "[0, 4, 0, 3, 2]\n1",
                "expected_output": "4.0",
                "is_sample": False,
                "explanation": "Max is 4."
            }
        ]
    },
    {
        "title": "3Sum",
        "slug": "3sum",
        "topic": "Two Pointers",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nNotice that the solution set must not contain duplicate triplets.",
        "constraints": "3 <= nums.length <= 3000\n-10^5 <= nums[i] <= 10^5\nOptimal Time: O(n^2), Space: O(1) beyond sorting",
        "hints": [
            "Sort the array first.",
            "Fix the first element, then use two pointers for the remaining two elements."
        ],
        "starter_code": {
            "python": "def threeSum(nums: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function threeSum(nums) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> threeSum(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> threeSum(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[-1, 0, 1, 2, -1, -4]",
                "expected_output": "[[-1, -1, 2], [-1, 0, 1]]",
                "is_sample": True,
                "explanation": "Two unique triplets sum to 0."
            },
            {
                "input_data": "[0, 1, 1]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "No triplet sums to 0."
            },
            {
                "input_data": "[0, 0, 0]",
                "expected_output": "[[0, 0, 0]]",
                "is_sample": False,
                "explanation": "All zeroes."
            },
            {
                "input_data": "[-2, 0, 1, 1, 2]",
                "expected_output": "[[-2, 0, 2], [-2, 1, 1]]",
                "is_sample": False,
                "explanation": "Triplets with duplicate values."
            }
        ]
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "topic": "Two Pointers",
        "difficulty": "Medium",
        "description": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.",
        "constraints": "n == height.length\n2 <= n <= 10^5\n0 <= height[i] <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Start with the widest container (left = 0, right = n - 1).",
            "Always move the pointer pointing to the shorter vertical line inward."
        ],
        "starter_code": {
            "python": "def maxArea(height: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxArea(height) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxArea(int[] height) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxArea(vector<int>& height) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 8, 6, 2, 5, 4, 8, 3, 7]",
                "expected_output": "49",
                "is_sample": True,
                "explanation": "Between indices 1 and 8: min(8, 7) * (8 - 1) = 7 * 7 = 49."
            },
            {
                "input_data": "[1, 1]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "min(1, 1) * 1 = 1."
            },
            {
                "input_data": "[4, 3, 2, 1, 4]",
                "expected_output": "16",
                "is_sample": False,
                "explanation": "Equal heights at ends: 4 * 4 = 16."
            }
        ]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "topic": "Sliding Window",
        "difficulty": "Medium",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "constraints": "0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.\nOptimal Time: O(n), Space: O(min(m, n))",
        "hints": [
            "Use a sliding window with a hash set or hash map storing last seen positions."
        ],
        "starter_code": {
            "python": "def lengthOfLongestSubstring(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function lengthOfLongestSubstring(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int lengthOfLongestSubstring(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"abcabcbb\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "\"abc\" length 3."
            },
            {
                "input_data": "\"bbbbb\"",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "\"b\" length 1."
            },
            {
                "input_data": "\"pwwkew\"",
                "expected_output": "3",
                "is_sample": False,
                "explanation": "\"wke\" length 3."
            },
            {
                "input_data": "\"\"",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Empty string has length 0."
            }
        ]
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "topic": "Array",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4\nOptimal Time: O(n), Space: O(1) (Kadane's Algorithm)",
        "hints": [
            "Kadane's algorithm: maintain the current max sum, resetting when it drops below zero."
        ],
        "starter_code": {
            "python": "def maxSubArray(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxSubArray(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxSubArray(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "[4, -1, 2, 1] sum is 6."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Single item 1."
            },
            {
                "input_data": "[5, 4, -1, 7, 8]",
                "expected_output": "23",
                "is_sample": False,
                "explanation": "Entire array sums to 23."
            },
            {
                "input_data": "[-5, -2, -3]",
                "expected_output": "-2",
                "is_sample": False,
                "explanation": "All negative: max is -2."
            }
        ]
    },
    {
        "title": "Minimum Size Subarray Sum",
        "slug": "minimum-size-subarray-sum",
        "topic": "Sliding Window",
        "difficulty": "Medium",
        "description": "Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a subarray whose sum is greater than or equal to `target`. If there is no such subarray, return `0` instead.",
        "constraints": "1 <= target <= 10^9\n1 <= nums.length <= 10^5\n1 <= nums[i] <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use two pointers for a variable-size sliding window."
        ],
        "starter_code": {
            "python": "def minSubArrayLen(target: int, nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function minSubArrayLen(target, nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int minSubArrayLen(int target, int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int minSubArrayLen(int target, vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "7\n[2, 3, 1, 2, 4, 3]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "[4, 3] has min length 2."
            },
            {
                "input_data": "4\n[1, 4, 4]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "[4] has length 1."
            },
            {
                "input_data": "11\n[1, 1, 1, 1, 1, 1, 1, 1]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "No subarray sums to >= 11."
            }
        ]
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "topic": "Array",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.\n\nYou must write an algorithm that runs in `O(n)` time and without using the division operation.",
        "constraints": "2 <= nums.length <= 10^5\n-30 <= nums[i] <= 30\nOptimal Time: O(n), Space: O(1) auxiliary",
        "hints": [
            "Prefix products from the left and suffix products from the right."
        ],
        "starter_code": {
            "python": "def productExceptSelf(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function productExceptSelf(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] productExceptSelf(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> productExceptSelf(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4]",
                "expected_output": "[24, 12, 8, 6]",
                "is_sample": True,
                "explanation": "Products excluding each position."
            },
            {
                "input_data": "[-1, 1, 0, -3, 3]",
                "expected_output": "[0, 0, 9, 0, 0]",
                "is_sample": True,
                "explanation": "Contains zero."
            },
            {
                "input_data": "[2, 3]",
                "expected_output": "[3, 2]",
                "is_sample": False,
                "explanation": "Two elements."
            }
        ]
    },
    {
        "title": "Subarray Sum Equals K",
        "slug": "subarray-sum-equals-k",
        "topic": "Prefix Sum",
        "difficulty": "Medium",
        "description": "Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.",
        "constraints": "1 <= nums.length <= 2 * 10^4\n-1000 <= nums[i] <= 1000\n-10^7 <= k <= 10^7\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Keep track of cumulative prefix sums in a hash map with their frequencies."
        ],
        "starter_code": {
            "python": "def subarraySum(nums: list[int], k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function subarraySum(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int subarraySum(int[] nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int subarraySum(vector<int>& nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 1, 1]\n2",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "[1, 1] at index 0-1 and 1-2."
            },
            {
                "input_data": "[1, 2, 3]\n3",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "[1, 2] and [3]."
            },
            {
                "input_data": "[1, -1, 0]\n0",
                "expected_output": "3",
                "is_sample": False,
                "explanation": "Zero-sum subarrays."
            }
        ]
    },
    {
        "title": "Longest Repeating Character Replacement",
        "slug": "longest-repeating-character-replacement",
        "topic": "Sliding Window",
        "difficulty": "Medium",
        "description": "You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character at most `k` times.\n\nReturn the length of the longest substring containing the same letter you can get after performing the above operations.",
        "constraints": "1 <= s.length <= 10^5\n0 <= k <= s.length\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Window length - count of most frequent character <= k."
        ],
        "starter_code": {
            "python": "def characterReplacement(s: str, k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function characterReplacement(s, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int characterReplacement(String s, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int characterReplacement(string s, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"ABAB\"\n2",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Replace two characters to get 'AAAA'."
            },
            {
                "input_data": "\"AABABBA\"\n1",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Replace one 'B' to get 'AAAA'."
            },
            {
                "input_data": "\"AAAA\"\n2",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "Already uniform."
            }
        ]
    },
    {
        "title": "Find Minimum in Rotated Sorted Array",
        "slug": "find-minimum-in-rotated-sorted-array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times.\n\nGiven the sorted rotated array `nums` of unique elements, return the minimum element of this array in `O(log n)` time.",
        "constraints": "1 <= nums.length <= 5000\n-5000 <= nums[i] <= 5000\nAll values are unique.\nOptimal Time: O(log n), Space: O(1)",
        "hints": [
            "Compare mid element with right element to decide which half is sorted."
        ],
        "starter_code": {
            "python": "def findMin(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findMin(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findMin(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findMin(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 4, 5, 1, 2]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 is the minimum."
            },
            {
                "input_data": "[4, 5, 6, 7, 0, 1, 2]",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "0 is minimum."
            },
            {
                "input_data": "[11, 13, 15, 17]",
                "expected_output": "11",
                "is_sample": False,
                "explanation": "Array not rotated (rotated 4 times)."
            }
        ]
    },
    {
        "title": "Next Permutation",
        "slug": "next-permutation",
        "topic": "Two Pointers",
        "difficulty": "Medium",
        "description": "A permutation of an array of integers is an arrangement of its members into a sequence or linear order.\n\nFind the next lexicographical permutation of numbers in-place.",
        "constraints": "1 <= nums.length <= 100\n0 <= nums[i] <= 100\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Find the first decreasing element from the right, swap it with the next larger element, and reverse the tail."
        ],
        "starter_code": {
            "python": "def nextPermutation(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function nextPermutation(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] nextPermutation(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> nextPermutation(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "[1, 3, 2]",
                "is_sample": True,
                "explanation": "Next permutation is [1, 3, 2]."
            },
            {
                "input_data": "[3, 2, 1]",
                "expected_output": "[1, 2, 3]",
                "is_sample": True,
                "explanation": "Wrap around to lowest order."
            },
            {
                "input_data": "[1, 1, 5]",
                "expected_output": "[1, 5, 1]",
                "is_sample": False,
                "explanation": "Duplicates handled properly."
            }
        ]
    },
    {
        "title": "Rotate Array",
        "slug": "rotate-array",
        "topic": "Array",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.",
        "constraints": "1 <= nums.length <= 10^5\n0 <= k <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Reverse entire array, then reverse first k elements, then reverse the rest."
        ],
        "starter_code": {
            "python": "def rotate(nums: list[int], k: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function rotate(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] rotate(int[] nums, int k) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> rotate(vector<int>& nums, int k) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5, 6, 7]\n3",
                "expected_output": "[5, 6, 7, 1, 2, 3, 4]",
                "is_sample": True,
                "explanation": "Rotated 3 steps."
            },
            {
                "input_data": "[-1, -100, 3, 99]\n2",
                "expected_output": "[3, 99, -1, -100]",
                "is_sample": True,
                "explanation": "Rotated 2 steps."
            },
            {
                "input_data": "[1, 2]\n5",
                "expected_output": "[2, 1]",
                "is_sample": False,
                "explanation": "k > n."
            }
        ]
    },
    {
        "title": "Sort Colors",
        "slug": "sort-colors",
        "topic": "Two Pointers",
        "difficulty": "Medium",
        "description": "Given an array `nums` with `n` objects colored red, white, or blue (represented as `0`, `1`, and `2`), sort them in-place so that objects of the same color are adjacent.",
        "constraints": "1 <= nums.length <= 300\nnums[i] is 0, 1, or 2.\nOptimal Time: O(n), Space: O(1) (Dutch National Flag)",
        "hints": [
            "Use three pointers: low, mid, high."
        ],
        "starter_code": {
            "python": "def sortColors(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function sortColors(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] sortColors(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> sortColors(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 0, 2, 1, 1, 0]",
                "expected_output": "[0, 0, 1, 1, 2, 2]",
                "is_sample": True,
                "explanation": "Sorted in place."
            },
            {
                "input_data": "[2, 0, 1]",
                "expected_output": "[0, 1, 2]",
                "is_sample": True,
                "explanation": "Sorted."
            },
            {
                "input_data": "[0]",
                "expected_output": "[0]",
                "is_sample": False,
                "explanation": "Single item."
            }
        ]
    },
    {
        "title": "Maximum Product Subarray",
        "slug": "maximum-product-subarray",
        "topic": "Array",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, find a subarray that has the largest product, and return the product.",
        "constraints": "1 <= nums.length <= 2 * 10^4\n-10 <= nums[i] <= 10\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Track both maximum product and minimum product at each step because negative numbers can flip signs."
        ],
        "starter_code": {
            "python": "def maxProduct(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxProduct(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxProduct(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxProduct(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 3, -2, 4]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "[2, 3] product 6."
            },
            {
                "input_data": "[-2, 0, -1]",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "0 is max."
            },
            {
                "input_data": "[-2, 3, -4]",
                "expected_output": "24",
                "is_sample": False,
                "explanation": "Negative times negative is positive."
            }
        ]
    },
    {
        "title": "4Sum",
        "slug": "4sum",
        "topic": "Two Pointers",
        "difficulty": "Medium",
        "description": "Given an array `nums` of `n` integers, return an array of all unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that `nums[a] + nums[b] + nums[c] + nums[d] == target`.",
        "constraints": "1 <= nums.length <= 200\n-10^9 <= nums[i] <= 10^9\nOptimal Time: O(n^3), Space: O(1) beyond sorting",
        "hints": [
            "Sort and use two nested loops with two pointers."
        ],
        "starter_code": {
            "python": "def fourSum(nums: list[int], target: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function fourSum(nums, target) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> fourSum(int[] nums, int target) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> fourSum(vector<int>& nums, int target) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 0, -1, 0, -2, 2]\n0",
                "expected_output": "[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]",
                "is_sample": True,
                "explanation": "Three quadruplets sum to 0."
            },
            {
                "input_data": "[2, 2, 2, 2, 2]\n8",
                "expected_output": "[[2, 2, 2, 2]]",
                "is_sample": True,
                "explanation": "Quadruplet with duplicates."
            },
            {
                "input_data": "[1, 2, 3, 4]\n100",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "No sum matches."
            }
        ]
    },
    {
        "title": "Permutation in String",
        "slug": "permutation-in-string",
        "topic": "Sliding Window",
        "difficulty": "Medium",
        "description": "Given two strings `s1` and `s2`, return `True` if `s2` contains a permutation of `s1`, or `False` otherwise.",
        "constraints": "1 <= s1.length, s2.length <= 10^4\ns1 and s2 consist of lowercase English letters.\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Slide a window of length len(s1) across s2 and compare character frequency counts."
        ],
        "starter_code": {
            "python": "def checkInclusion(s1: str, s2: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function checkInclusion(s1, s2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean checkInclusion(String s1, String s2) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool checkInclusion(string s1, string s2) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"ab\"\n\"eidbaooo\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "s2 contains \"ba\" which is a permutation of \"ab\"."
            },
            {
                "input_data": "\"ab\"\n\"eidboaoo\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "No permutation found."
            },
            {
                "input_data": "\"a\"\n\"a\"",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Equal single characters."
            }
        ]
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "topic": "Two Pointers",
        "difficulty": "Hard",
        "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.",
        "constraints": "n == height.length\n1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use two pointers moving inward, keeping track of left_max and right_max."
        ],
        "starter_code": {
            "python": "def trap(height: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function trap(height) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int trap(int[] height) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int trap(vector<int>& height) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "Trapped water is 6 units."
            },
            {
                "input_data": "[4, 2, 0, 3, 2, 5]",
                "expected_output": "9",
                "is_sample": True,
                "explanation": "Trapped water is 9 units."
            },
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Monotonic increasing cannot trap water."
            },
            {
                "input_data": "[5, 4, 1, 2]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Small valley traps 1 unit."
            }
        ]
    },
    {
        "title": "Sliding Window Maximum",
        "slug": "sliding-window-maximum",
        "topic": "Sliding Window",
        "difficulty": "Hard",
        "description": "You are given an array of integers `nums`, and a sliding window of size `k` moving from left to right. Return the max sliding window values.",
        "constraints": "1 <= nums.length <= 10^5\n1 <= k <= nums.length\nOptimal Time: O(n), Space: O(k) (Monotonic Deque)",
        "hints": [
            "Use a monotonic decreasing deque storing indices."
        ],
        "starter_code": {
            "python": "def maxSlidingWindow(nums: list[int], k: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxSlidingWindow(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] maxSlidingWindow(int[] nums, int k) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> maxSlidingWindow(vector<int>& nums, int k) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 3, -1, -3, 5, 3, 6, 7]\n3",
                "expected_output": "[3, 3, 5, 5, 6, 7]",
                "is_sample": True,
                "explanation": "Window maximums."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "[1]",
                "is_sample": True,
                "explanation": "Single item."
            },
            {
                "input_data": "[7, 2, 4]\n2",
                "expected_output": "[7, 4]",
                "is_sample": False,
                "explanation": "k = 2 window."
            }
        ]
    },
    {
        "title": "Minimum Window Substring",
        "slug": "minimum-window-substring",
        "topic": "Sliding Window",
        "difficulty": "Hard",
        "description": "Given two strings `s` and `t` of lengths `m` and `n`, return the minimum window substring of `s` such that every character in `t` is included in the window. If there is no such substring, return `\"\"`.",
        "constraints": "m == s.length, n == t.length\n1 <= m, n <= 10^5\nOptimal Time: O(m + n), Space: O(1)",
        "hints": [
            "Use two pointers and character count hash maps."
        ],
        "starter_code": {
            "python": "def minWindow(s: str, t: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function minWindow(s, t) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String minWindow(String s, String t) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string minWindow(string s, string t) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"ADOBECODEBANC\"\n\"ABC\"",
                "expected_output": "\"BANC\"",
                "is_sample": True,
                "explanation": "\"BANC\" includes A, B, and C."
            },
            {
                "input_data": "\"a\"\n\"a\"",
                "expected_output": "\"a\"",
                "is_sample": True,
                "explanation": "Single char matches."
            },
            {
                "input_data": "\"a\"\n\"aa\"",
                "expected_output": "\"\"",
                "is_sample": False,
                "explanation": "Cannot satisfy count."
            }
        ]
    },
    {
        "title": "First Missing Positive",
        "slug": "first-missing-positive",
        "topic": "Array",
        "difficulty": "Hard",
        "description": "Given an unsorted integer array `nums`, return the smallest positive integer that is not present in `nums`.\n\nYou must implement an algorithm that runs in `O(n)` time and uses `O(1)` auxiliary space.",
        "constraints": "1 <= nums.length <= 10^5\n-2^31 <= nums[i] <= 2^31 - 1\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Place each number x in its bucket index x - 1 using cyclic sort."
        ],
        "starter_code": {
            "python": "def firstMissingPositive(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function firstMissingPositive(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int firstMissingPositive(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int firstMissingPositive(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 0]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 is smallest missing positive."
            },
            {
                "input_data": "[3, 4, -1, 1]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 is missing."
            },
            {
                "input_data": "[7, 8, 9, 11, 12]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "1 is missing."
            }
        ]
    },
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "topic": "Binary Search",
        "difficulty": "Hard",
        "description": "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.\n\nThe overall run time complexity should be `O(log (m+n))`.",
        "constraints": "0 <= m, n <= 1000\n1 <= m + n <= 2000\nOptimal Time: O(log(min(m, n))), Space: O(1)",
        "hints": [
            "Binary search on partition cut in the smaller array."
        ],
        "starter_code": {
            "python": "def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:\n    # Write your solution here\n    pass\n",
            "javascript": "function findMedianSortedArrays(nums1, nums2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public double findMedianSortedArrays(int[] nums1, int[] nums2) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 3]\n[2]",
                "expected_output": "2.0",
                "is_sample": True,
                "explanation": "Merged array [1, 2, 3], median 2.0."
            },
            {
                "input_data": "[1, 2]\n[3, 4]",
                "expected_output": "2.5",
                "is_sample": True,
                "explanation": "Merged array [1, 2, 3, 4], median (2 + 3) / 2 = 2.5."
            },
            {
                "input_data": "[0, 0]\n[0, 0]",
                "expected_output": "0.0",
                "is_sample": False,
                "explanation": "All zeroes."
            }
        ]
    }
]
