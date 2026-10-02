"""
hash_tables.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Intersection of Two Arrays II",
        "slug": "intersection-of-two-arrays-ii",
        "topic": "Hash Table",
        "difficulty": "Easy",
        "description": "Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must appear as many times as it shows in both arrays and you may return the result in any order.",
        "constraints": "1 <= nums1.length, nums2.length <= 1000\n0 <= nums1[i], nums2[i] <= 1000\nOptimal Time: O(n + m), Space: O(min(n, m))",
        "hints": [
            "Count elements in nums1 using a hash map, then decrement when present in nums2."
        ],
        "starter_code": {
            "python": "def intersect(nums1: list[int], nums2: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function intersect(nums1, nums2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] intersect(int[] nums1, int[] nums2) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> intersect(vector<int>& nums1, vector<int>& nums2) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 2, 1]\n[2, 2]",
                "expected_output": "[2, 2]",
                "is_sample": True,
                "explanation": "2 appears twice in both."
            },
            {
                "input_data": "[4, 9, 5]\n[9, 4, 9, 8, 4]",
                "expected_output": "[4, 9]",
                "is_sample": True,
                "explanation": "Intersection is [4, 9]."
            },
            {
                "input_data": "[1, 2]\n[3, 4]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "No common elements."
            }
        ]
    },
    {
        "title": "Single Number",
        "slug": "single-number",
        "topic": "Bit Manipulation",
        "difficulty": "Easy",
        "description": "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.",
        "constraints": "1 <= nums.length <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "XOR of two identical numbers is 0; x ^ 0 = x."
        ],
        "starter_code": {
            "python": "def singleNumber(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function singleNumber(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int singleNumber(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int singleNumber(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 2, 1]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 is unique."
            },
            {
                "input_data": "[4, 1, 2, 1, 2]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "4 is unique."
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
        "title": "Happy Number",
        "slug": "happy-number",
        "topic": "Hash Table",
        "difficulty": "Easy",
        "description": "Write an algorithm to determine if a number `n` is happy (eventually reaches 1 when repeatedly replaced by the sum of squares of its digits).",
        "constraints": "1 <= n <= 2^31 - 1\nOptimal Time: O(log n), Space: O(log n)",
        "hints": [
            "Use a hash set to detect cycles."
        ],
        "starter_code": {
            "python": "def isHappy(n: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isHappy(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isHappy(int n) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isHappy(int n) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "19",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "19 -> 82 -> 68 -> 100 -> 1."
            },
            {
                "input_data": "2",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Enters endless cycle."
            },
            {
                "input_data": "1",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "1 is already happy."
            }
        ]
    },
    {
        "title": "Word Pattern",
        "slug": "word-pattern",
        "topic": "Hash Table",
        "difficulty": "Easy",
        "description": "Given a `pattern` and a string `s`, find if `s` follows the same pattern (bijection between letter and word).",
        "constraints": "1 <= pattern.length <= 300\n1 <= s.length <= 3000\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Use two maps to ensure one-to-one mapping between pattern chars and words."
        ],
        "starter_code": {
            "python": "def wordPattern(pattern: str, s: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function wordPattern(pattern, s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean wordPattern(String pattern, String s) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool wordPattern(string pattern, string s) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"abba\"\n\"dog cat cat dog\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Valid bijection."
            },
            {
                "input_data": "\"abba\"\n\"dog cat cat fish\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Pattern mismatch."
            },
            {
                "input_data": "\"aaaa\"\n\"dog cat cat dog\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Mismatch."
            }
        ]
    },
    {
        "title": "Isomorphic Strings",
        "slug": "isomorphic-strings",
        "topic": "Hash Table",
        "difficulty": "Easy",
        "description": "Given two strings `s` and `t`, determine if they are isomorphic.",
        "constraints": "1 <= s.length <= 5 * 10^4\nt.length == s.length\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Track character mappings in both directions."
        ],
        "starter_code": {
            "python": "def isIsomorphic(s: str, t: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isIsomorphic(s, t) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isIsomorphic(String s, String t) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isIsomorphic(string s, string t) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"egg\"\n\"add\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "'e' -> 'a', 'g' -> 'd'."
            },
            {
                "input_data": "\"foo\"\n\"bar\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "'o' cannot map to both 'a' and 'r'."
            },
            {
                "input_data": "\"paper\"\n\"title\"",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Isomorphic."
            }
        ]
    },
    {
        "title": "Insert Delete GetRandom O(1)",
        "slug": "insert-delete-getrandom-o1",
        "topic": "Hash Table",
        "difficulty": "Medium",
        "description": "Implement the `RandomizedSet` class which supports `insert(val)`, `remove(val)`, and `getRandom()` in average `O(1)` time.",
        "constraints": "-2^31 <= val <= 2^31 - 1\nAt most 2 * 10^5 calls\nOptimal Time: O(1) average, Space: O(n)",
        "hints": [
            "Combine an array (for random index access) and a hash map (value -> index). Swap with last element to delete in O(1)."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"RandomizedSet\", \"insert\", \"remove\", \"insert\"]\n[[], [1], [2], [2]]",
                "expected_output": "[None, True, False, True]",
                "is_sample": True,
                "explanation": "Basic operations."
            },
            {
                "input_data": "[\"RandomizedSet\", \"insert\", \"insert\", \"remove\"]\n[[], [1], [1], [1]]",
                "expected_output": "[None, True, False, True]",
                "is_sample": True,
                "explanation": "Duplicates."
            },
            {
                "input_data": "[\"RandomizedSet\", \"remove\"]\n[[], [0]]",
                "expected_output": "[None, False]",
                "is_sample": False,
                "explanation": "Remove non-existent."
            }
        ]
    },
    {
        "title": "Subarray Sums Divisible by K",
        "slug": "subarray-sums-divisible-by-k",
        "topic": "Hash Table",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.",
        "constraints": "1 <= nums.length <= 3 * 10^4\n-10^4 <= nums[i] <= 10^4\n2 <= k <= 10^4\nOptimal Time: O(n), Space: O(k)",
        "hints": [
            "Use prefix sums modulo k: two prefix sums with identical remainder produce a subarray divisible by k."
        ],
        "starter_code": {
            "python": "def subarraysDivByK(nums: list[int], k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function subarraysDivByK(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int subarraysDivByK(int[] nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int subarraysDivByK(vector<int>& nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[4, 5, 0, -2, -3, 1]\n5",
                "expected_output": "7",
                "is_sample": True,
                "explanation": "7 subarrays divisible by 5."
            },
            {
                "input_data": "[5]\n9",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "No subarray."
            },
            {
                "input_data": "[-1, 2, 9]\n2",
                "expected_output": "2",
                "is_sample": False,
                "explanation": "Divisible by 2."
            }
        ]
    },
    {
        "title": "Longest Consecutive Sequence",
        "slug": "longest-consecutive-sequence",
        "topic": "Hash Table",
        "difficulty": "Medium",
        "description": "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence in `O(n)` time.",
        "constraints": "0 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Store in a hash set. Only start counting sequence if (num - 1) is not in the set."
        ],
        "starter_code": {
            "python": "def longestConsecutive(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function longestConsecutive(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int longestConsecutive(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int longestConsecutive(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[100, 4, 200, 1, 3, 2]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "[1, 2, 3, 4] has length 4."
            },
            {
                "input_data": "[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]",
                "expected_output": "9",
                "is_sample": True,
                "explanation": "[0, 1, 2, 3, 4, 5, 6, 7, 8] has length 9."
            },
            {
                "input_data": "[]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Empty array length 0."
            }
        ]
    },
    {
        "title": "Top K Frequent Elements",
        "slug": "top-k-frequent-elements",
        "topic": "Hash Table",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.",
        "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4\nk is in range [1, unique elements].\nOptimal Time: O(n), Space: O(n) using Bucket Sort",
        "hints": [
            "Use frequency map then bucket sort where index = frequency."
        ],
        "starter_code": {
            "python": "def topKFrequent(nums: list[int], k: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function topKFrequent(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] topKFrequent(int[] nums, int k) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> topKFrequent(vector<int>& nums, int k) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 1, 1, 2, 2, 3]\n2",
                "expected_output": "[1, 2]",
                "is_sample": True,
                "explanation": "1 (freq 3) and 2 (freq 2)."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "[1]",
                "is_sample": True,
                "explanation": "Single item."
            },
            {
                "input_data": "[4, 1, -1, 2, -1, 2, 3]\n2",
                "expected_output": "[-1, 2]",
                "is_sample": False,
                "explanation": "-1 and 2 each appear twice."
            }
        ]
    },
    {
        "title": "Continuous Subarray Sum",
        "slug": "continuous-subarray-sum",
        "topic": "Hash Table",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` and an integer `k`, return `True` if `nums` has a good subarray of length at least 2 whose sum is a multiple of `k`.",
        "constraints": "1 <= nums.length <= 10^5\n0 <= nums[i] <= 10^9\n1 <= k <= 2^31 - 1\nOptimal Time: O(n), Space: O(min(n, k))",
        "hints": [
            "Store remainder -> earliest index seen in a hash map."
        ],
        "starter_code": {
            "python": "def checkSubarraySum(nums: list[int], k: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function checkSubarraySum(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean checkSubarraySum(int[] nums, int k) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool checkSubarraySum(vector<int>& nums, int k) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[23, 2, 4, 6, 7]\n6",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "[2, 4] sum is 6, multiple of 6."
            },
            {
                "input_data": "[23, 2, 6, 4, 7]\n6",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "[23, 2, 6, 4, 7] sum is 42."
            },
            {
                "input_data": "[23, 2, 6, 4, 7]\n13",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "No continuous subarray."
            }
        ]
    },
    {
        "title": "Substring with Concatenation of All Words",
        "slug": "substring-with-concatenation-of-all-words",
        "topic": "Hash Table",
        "difficulty": "Hard",
        "description": "You are given a string `s` and an array of strings `words` of the same length. Return all starting indices of substring(s) in `s` that is a concatenation of each word in `words` exactly once.",
        "constraints": "1 <= s.length <= 10^4\n1 <= words.length <= 5000\n1 <= words[i].length <= 30\nOptimal Time: O(s.length * word_length), Space: O(words.length)",
        "hints": [
            "Sliding window with step equal to word length."
        ],
        "starter_code": {
            "python": "def findSubstring(s: str, words: list[str]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findSubstring(s, words) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> findSubstring(String s, String[] words) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findSubstring(string s, vector<string>& words) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"barfoothefoobarman\"\n[\"foo\", \"bar\"]",
                "expected_output": "[0, 9]",
                "is_sample": True,
                "explanation": "Indices 0 and 9."
            },
            {
                "input_data": "\"wordgoodgoodgoodbestword\"\n[\"word\", \"good\", \"best\", \"word\"]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "No concatenation matches."
            },
            {
                "input_data": "\"barfoofoobarthefoobarman\"\n[\"bar\", \"foo\", \"the\"]",
                "expected_output": "[6, 9, 12]",
                "is_sample": False,
                "explanation": "Overlapping matches."
            }
        ]
    },
    {
        "title": "Max Points on a Line",
        "slug": "max-points-on-a-line",
        "topic": "Hash Table",
        "difficulty": "Hard",
        "description": "Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.",
        "constraints": "1 <= points.length <= 300\npoints[i].length == 2\n-10^4 <= xi, yi <= 10^4\nOptimal Time: O(n^2), Space: O(n)",
        "hints": [
            "For each point, calculate the slopes to all other points using reduced fractions (dy/gcd, dx/gcd)."
        ],
        "starter_code": {
            "python": "def maxPoints(points: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxPoints(points) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxPoints(int[][] points) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxPoints(vector<vector<int>>& points) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 1], [2, 2], [3, 3]]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "All 3 points lie on y = x."
            },
            {
                "input_data": "[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "4 points on one line."
            },
            {
                "input_data": "[[0, 0]]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single point max is 1."
            }
        ]
    }
]
