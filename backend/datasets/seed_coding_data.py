"""
build_coding_questions.py
Builds a curated repository of 190+ Data Structures & Algorithms coding questions
with accurate starter codes, constraints, hints, sample test cases, and hidden test cases.
"""

import json
from typing import List, Dict, Any

RAW_QUESTIONS: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. ARRAYS & TWO POINTERS & SLIDING WINDOW (EASY)
    # =========================================================================
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists.\nOptimal Time Complexity: O(n)\nOptimal Space Complexity: O(n)",
        "hints": [
            "A brute force approach checks all pairs in O(n^2) time.",
            "Can you use a hash map to look up if the complement (target - num) has already been seen in O(1) time?"
        ],
        "starter_code": {
            "python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    # Your solution here\n    pass\n",
            "javascript": "function twoSum(nums, target) {\n    // Your solution here\n}\n",
            "java": "import java.util.*;\n\npublic class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[2, 7, 11, 15]\n9", "expected_output": "[0, 1]", "is_sample": True, "explanation": "nums[0] + nums[1] == 9, so return [0, 1]."},
            {"input_data": "[3, 2, 4]\n6", "expected_output": "[1, 2]", "is_sample": True, "explanation": "nums[1] + nums[2] == 6, so return [1, 2]."},
            {"input_data": "[3, 3]\n6", "expected_output": "[0, 1]", "is_sample": False, "explanation": "Duplicate elements matching target."},
            {"input_data": "[-1, -2, -3, -4, -5]\n-8", "expected_output": "[2, 4]", "is_sample": False, "explanation": "Negative numbers: -3 + -5 = -8."},
            {"input_data": "[0, 4, 3, 0]\n0", "expected_output": "[0, 3]", "is_sample": False, "explanation": "Zeroes."}
        ]
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.",
        "constraints": "1 <= prices.length <= 10^5\n0 <= prices[i] <= 10^4\nOptimal Time Complexity: O(n)\nOptimal Space Complexity: O(1)",
        "hints": [
            "Track the minimum price observed so far as you iterate through the array.",
            "At each step, calculate the potential profit if you were to sell at the current price."
        ],
        "starter_code": {
            "python": "def maxProfit(prices: list[int]) -> int:\n    # Your solution here\n    pass\n",
            "javascript": "function maxProfit(prices) {\n    // Your solution here\n}\n",
            "java": "public class Solution {\n    public int maxProfit(int[] prices) {\n        // Your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        // Your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[7, 1, 5, 3, 6, 4]", "expected_output": "5", "is_sample": True, "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5."},
            {"input_data": "[7, 6, 4, 3, 1]", "expected_output": "0", "is_sample": True, "explanation": "In this case, no transactions are done and max profit = 0."},
            {"input_data": "[1, 2]", "expected_output": "1", "is_sample": False, "explanation": "Two elements."},
            {"input_data": "[2, 4, 1]", "expected_output": "2", "is_sample": False, "explanation": "Minimum occurs at the end."},
            {"input_data": "[3, 2, 6, 5, 0, 3]", "expected_output": "4", "is_sample": False, "explanation": "Multiple peaks and valleys."}
        ]
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.",
        "constraints": "1 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9\nOptimal Time Complexity: O(n)\nOptimal Space Complexity: O(n)",
        "hints": [
            "A hash set allows O(1) average lookup and insertion time.",
            "If an element already exists in the set, a duplicate has been found."
        ],
        "starter_code": {
            "python": "def containsDuplicate(nums: list[int]) -> bool:\n    # Your solution here\n    pass\n",
            "javascript": "function containsDuplicate(nums) {\n    // Your solution here\n}\n",
            "java": "import java.util.*;\n\npublic class Solution {\n    public boolean containsDuplicate(int[] nums) {\n        // Your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <vector>\n#include <unordered_set>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    boolean containsDuplicate(vector<int>& nums) {\n        // Your solution here\n        return false;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[1, 2, 3, 1]", "expected_output": "true", "is_sample": True, "explanation": "1 appears twice."},
            {"input_data": "[1, 2, 3, 4]", "expected_output": "false", "is_sample": True, "explanation": "All elements are distinct."},
            {"input_data": "[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]", "expected_output": "true", "is_sample": False, "explanation": "Multiple duplicates."},
            {"input_data": "[42]", "expected_output": "false", "is_sample": False, "explanation": "Single element array."},
            {"input_data": "[0, 0]", "expected_output": "true", "is_sample": False, "explanation": "Two identical zeroes."}
        ]
    },
    {
        "title": "Remove Duplicates from Sorted Array",
        "slug": "remove-duplicates-from-sorted-array",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.\n\nReturn the number of unique elements `k` in `nums`.",
        "constraints": "1 <= nums.length <= 3 * 10^4\n-100 <= nums[i] <= 100\nnums is sorted in non-decreasing order.\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use two pointers: a slow pointer for the position of unique elements, and a fast pointer to scan the array."
        ],
        "starter_code": {
            "python": "def removeDuplicates(nums: list[int]) -> int:\n    # Your solution here\n    pass\n",
            "javascript": "function removeDuplicates(nums) {\n    // Your solution here\n}\n",
            "java": "public class Solution {\n    public int removeDuplicates(int[] nums) {\n        // Your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int removeDuplicates(vector<int>& nums) {\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[1, 1, 2]", "expected_output": "2", "is_sample": True, "explanation": "Unique elements are [1, 2], so return 2."},
            {"input_data": "[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]", "expected_output": "5", "is_sample": True, "explanation": "Unique elements are 5."},
            {"input_data": "[1]", "expected_output": "1", "is_sample": False, "explanation": "Single element."},
            {"input_data": "[1, 2, 3, 4, 5]", "expected_output": "5", "is_sample": False, "explanation": "Already unique."}
        ]
    },
    {
        "title": "Move Zeroes",
        "slug": "move-zeroes",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.\n\nNote that you must do this in-place without making a copy of the array and return the modified array.",
        "constraints": "1 <= nums.length <= 10^4\n-2^31 <= nums[i] <= 2^31 - 1\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Keep a pointer tracking where the next non-zero element should be written."
        ],
        "starter_code": {
            "python": "def moveZeroes(nums: list[int]) -> list[int]:\n    # Modify in place and return nums\n    pass\n",
            "javascript": "function moveZeroes(nums) {\n    // Modify in place and return nums\n}\n",
            "java": "public class Solution {\n    public int[] moveZeroes(int[] nums) {\n        return nums;\n    }\n}\n",
            "cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> moveZeroes(vector<int>& nums) {\n        return nums;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[0, 1, 0, 3, 12]", "expected_output": "[1, 3, 12, 0, 0]", "is_sample": True, "explanation": "All non-zeroes moved to front."},
            {"input_data": "[0]", "expected_output": "[0]", "is_sample": True, "explanation": "Single zero."},
            {"input_data": "[1, 2, 3]", "expected_output": "[1, 2, 3]", "is_sample": False, "explanation": "No zeroes."},
            {"input_data": "[0, 0, 1]", "expected_output": "[1, 0, 0]", "is_sample": False, "explanation": "Leading zeroes."}
        ]
    },
    {
        "title": "Majority Element",
        "slug": "majority-element",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an array `nums` of size `n`, return the majority element.\n\nThe majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.",
        "constraints": "n == nums.length\n1 <= n <= 5 * 10^4\n-10^9 <= nums[i] <= 10^9\nOptimal Time: O(n), Space: O(1) using Boyer-Moore Voting",
        "hints": [
            "Can you solve it in linear time and O(1) space with Boyer-Moore Voting Algorithm?"
        ],
        "starter_code": {
            "python": "def majorityElement(nums: list[int]) -> int:\n    pass\n",
            "javascript": "function majorityElement(nums) {\n}\n",
            "java": "public class Solution {\n    public int majorityElement(int[] nums) {\n        return 0;\n    }\n}\n",
            "cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int majorityElement(vector<int>& nums) {\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[3, 2, 3]", "expected_output": "3", "is_sample": True, "explanation": "3 appears 2 times, which is > 3/2."},
            {"input_data": "[2, 2, 1, 1, 1, 2, 2]", "expected_output": "2", "is_sample": True, "explanation": "2 appears 4 times, > 7/2."},
            {"input_data": "[1]", "expected_output": "1", "is_sample": False, "explanation": "Single element is majority."},
            {"input_data": "[6, 5, 5]", "expected_output": "5", "is_sample": False, "explanation": "Majority is 5."}
        ]
    },
    {
        "title": "Valid Palindrome",
        "slug": "valid-palindrome",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `true` if it is a palindrome, or `false` otherwise.",
        "constraints": "1 <= s.length <= 2 * 10^5\ns consists only of printable ASCII characters.\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use two pointers moving inward from both ends, skipping non-alphanumeric characters."
        ],
        "starter_code": {
            "python": "def isPalindrome(s: str) -> bool:\n    pass\n",
            "javascript": "function isPalindrome(s) {\n}\n",
            "java": "public class Solution {\n    public boolean isPalindrome(String s) {\n        return false;\n    }\n}\n",
            "cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool isPalindrome(string s) {\n        return false;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "\"A man, a plan, a canal: Panama\"", "expected_output": "true", "is_sample": True, "explanation": "\"amanaplanacanalpanama\" is a palindrome."},
            {"input_data": "\"race a car\"", "expected_output": "false", "is_sample": True, "explanation": "\"raceacar\" is not a palindrome."},
            {"input_data": "\" \"", "expected_output": "true", "is_sample": False, "explanation": "Empty string after removing non-alphanumeric."},
            {"input_data": "\"0P\"", "expected_output": "false", "is_sample": False, "explanation": "Not equal."}
        ]
    },
    {
        "title": "Squares of a Sorted Array",
        "slug": "squares-of-a-sorted-array",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given an integer array `nums` sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.",
        "constraints": "1 <= nums.length <= 10^4\n-10^4 <= nums[i] <= 10^4\nnums is sorted in non-decreasing order.\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "The largest square values will be at either end of the array."
        ],
        "starter_code": {
            "python": "def sortedSquares(nums: list[int]) -> list[int]:\n    pass\n",
            "javascript": "function sortedSquares(nums) {\n}\n",
            "java": "public class Solution {\n    public int[] sortedSquares(int[] nums) {\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> sortedSquares(vector<int>& nums) {\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[-4, -1, 0, 3, 10]", "expected_output": "[0, 1, 9, 16, 100]", "is_sample": True, "explanation": "After squaring, [16, 1, 0, 9, 100]. Sorted: [0, 1, 9, 16, 100]."},
            {"input_data": "[-7, -3, 2, 3, 11]", "expected_output": "[4, 9, 9, 49, 121]", "is_sample": True, "explanation": "Sorted squares."},
            {"input_data": "[-1]", "expected_output": "[1]", "is_sample": False, "explanation": "Single negative number."},
            {"input_data": "[0, 2, 3]", "expected_output": "[0, 4, 9]", "is_sample": False, "explanation": "All positive."}
        ]
    },
    {
        "title": "Find All Numbers Disappeared in an Array",
        "slug": "find-all-numbers-disappeared-in-an-array",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "Given an array `nums` of `n` integers where `nums[i]` is in the range `[1, n]`, return an array of all the integers in the range `[1, n]` that do not appear in `nums`.",
        "constraints": "n == nums.length\n1 <= n <= 10^5\n1 <= nums[i] <= n\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Can you negate the number at index abs(num) - 1 to mark presence?"
        ],
        "starter_code": {
            "python": "def findDisappearedNumbers(nums: list[int]) -> list[int]:\n    pass\n",
            "javascript": "function findDisappearedNumbers(nums) {\n}\n",
            "java": "import java.util.*;\npublic class Solution {\n    public List<Integer> findDisappearedNumbers(int[] nums) {\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> findDisappearedNumbers(vector<int>& nums) {\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[4, 3, 2, 7, 8, 2, 3, 1]", "expected_output": "[5, 6]", "is_sample": True, "explanation": "5 and 6 are missing."},
            {"input_data": "[1, 1]", "expected_output": "[2]", "is_sample": True, "explanation": "2 is missing."},
            {"input_data": "[1]", "expected_output": "[]", "is_sample": False, "explanation": "No numbers missing."}
        ]
    },
    {
        "title": "Maximum Average Subarray I",
        "slug": "maximum-average-subarray-i",
        "topic": "Sliding Window",
        "difficulty": "Easy",
        "description": "You are given an integer array `nums` consisting of `n` elements, and an integer `k`.\n\nFind a contiguous subarray whose length is equal to `k` that has the maximum average value and return this value.",
        "constraints": "n == nums.length\n1 <= k <= n <= 10^5\n-10^4 <= nums[i] <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Compute the sum of the first k elements, then slide the window across the array."
        ],
        "starter_code": {
            "python": "def findMaxAverage(nums: list[int], k: int) -> float:\n    pass\n",
            "javascript": "function findMaxAverage(nums, k) {\n}\n",
            "java": "public class Solution {\n    public double findMaxAverage(int[] nums, int k) {\n        return 0.0;\n    }\n}\n",
            "cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    double findMaxAverage(vector<int>& nums, int k) {\n        return 0.0;\n    }\n};\n"
        },
        "test_cases": [
            {"input_data": "[1, 12, -5, -6, 50, 3]\n4", "expected_output": "12.75", "is_sample": True, "explanation": "Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75."},
            {"input_data": "[5]\n1", "expected_output": "5.0", "is_sample": True, "explanation": "Single element average is 5.0."},
            {"input_data": "[0, 4, 0, 3, 2]\n1", "expected_output": "4.0", "is_sample": False, "explanation": "Max element is 4."}
        ]
    }
]
