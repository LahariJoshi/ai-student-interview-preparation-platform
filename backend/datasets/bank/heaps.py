"""
heaps.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Last Stone Weight",
        "slug": "last-stone-weight",
        "topic": "Heap",
        "difficulty": "Easy",
        "description": "You are given an array of integers `stones` where `stones[i]` is the weight of the `i-th` stone. We smash the two heaviest stones `x` and `y` (x <= y). If x != y, stone of weight `y - x` remains. Return the weight of the last remaining stone, or 0 if none remain.",
        "constraints": "1 <= stones.length <= 30\n1 <= stones[i] <= 1000\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Use a max-heap (invert numbers in Python's min-heap)."
        ],
        "starter_code": {
            "python": "def lastStoneWeight(stones: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function lastStoneWeight(stones) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int lastStoneWeight(int[] stones) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int lastStoneWeight(vector<int>& stones) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 7, 4, 1, 8, 1]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Last stone remaining weight is 1."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Single stone weight 1."
            },
            {
                "input_data": "[2, 2]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Both smash completely, returning 0."
            }
        ]
    },
    {
        "title": "Kth Largest Element in a Stream",
        "slug": "kth-largest-element-in-a-stream",
        "topic": "Heap",
        "difficulty": "Easy",
        "description": "Design a class to find the `k-th` largest element in a stream.",
        "constraints": "1 <= k <= 10^4\n0 <= nums.length <= 10^4\nAt most 10^4 calls\nOptimal Time: O(log k) per add, Space: O(k)",
        "hints": [
            "Maintain a min-heap of size k."
        ],
        "starter_code": {
            "python": "    def __init__(self, k: int, nums: list[int]):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"KthLargest\", \"add\", \"add\", \"add\", \"add\", \"add\"]\n[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]",
                "expected_output": "[None, 4, 5, 5, 8, 8]",
                "is_sample": True,
                "explanation": "Stream maintains 3rd largest."
            },
            {
                "input_data": "[\"KthLargest\", \"add\"]\n[[1, []], [-3]]",
                "expected_output": "[None, -3]",
                "is_sample": True,
                "explanation": "Empty initial stream."
            },
            {
                "input_data": "[\"KthLargest\", \"add\", \"add\"]\n[[2, [0]], [-1], [1]]",
                "expected_output": "[None, -1, 0]",
                "is_sample": False,
                "explanation": "Size 2."
            }
        ]
    },
    {
        "title": "Relative Ranks",
        "slug": "relative-ranks",
        "topic": "Heap",
        "difficulty": "Easy",
        "description": "You are given an integer array `score` of size `n`, where `score[i]` is the score of the `i-th` athlete in a competition. Return the rank of each athlete with top 3 awarded 'Gold Medal', 'Silver Medal', 'Bronze Medal'.",
        "constraints": "1 <= n <= 10^4\n0 <= score[i] <= 10^6\nAll scores are unique.\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Sort scores descending while keeping track of original indices."
        ],
        "starter_code": {
            "python": "def findRelativeRanks(score: list[int]) -> list[str]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findRelativeRanks(score) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String[] findRelativeRanks(int[] score) {\n        // Write your solution here\n        return new String[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<string> findRelativeRanks(vector<int>& score) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[5, 4, 3, 2, 1]",
                "expected_output": "[\"Gold Medal\", \"Silver Medal\", \"Bronze Medal\", \"4\", \"5\"]",
                "is_sample": True,
                "explanation": "Direct ranks."
            },
            {
                "input_data": "[10, 3, 8, 9, 4]",
                "expected_output": "[\"Gold Medal\", \"5\", \"Bronze Medal\", \"Silver Medal\", \"4\"]",
                "is_sample": True,
                "explanation": "Sorted order."
            },
            {
                "input_data": "[1]",
                "expected_output": "[\"Gold Medal\"]",
                "is_sample": False,
                "explanation": "Single athlete."
            }
        ]
    },
    {
        "title": "Kth Largest Element in an Array",
        "slug": "kth-largest-element-in-an-array",
        "topic": "Heap",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` and an integer `k`, return the `k-th` largest element in the array. Can you solve it in `O(n)` average time?",
        "constraints": "1 <= k <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4\nOptimal Time: O(n) average Quickselect, O(n log k) with Min-Heap",
        "hints": [
            "Maintain a min-heap of size k, or use QuickSelect."
        ],
        "starter_code": {
            "python": "def findKthLargest(nums: list[int], k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findKthLargest(nums, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findKthLargest(int[] nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findKthLargest(vector<int>& nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 2, 1, 5, 6, 4]\n2",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "2nd largest element is 5."
            },
            {
                "input_data": "[3, 2, 3, 1, 2, 4, 5, 5, 6]\n4",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "4th largest element is 4."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single element."
            }
        ]
    },
    {
        "title": "Find K Closest Elements",
        "slug": "find-k-closest-elements",
        "topic": "Heap",
        "difficulty": "Medium",
        "description": "Given a sorted integer array `arr`, two integers `k` and `x`, return the `k` closest integers to `x` in the array. The result should also be sorted in ascending order.",
        "constraints": "1 <= k <= arr.length <= 10^4\n-10^4 <= arr[i], x <= 10^4\narr is sorted in ascending order.\nOptimal Time: O(log(n - k) + k), Space: O(1)",
        "hints": [
            "Binary search for the left boundary of the window of size k."
        ],
        "starter_code": {
            "python": "def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findClosestElements(arr, k, x) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> findClosestElements(int[] arr, int k, int x) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findClosestElements(vector<int>& arr, int k, int x) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]\n4\n3",
                "expected_output": "[1, 2, 3, 4]",
                "is_sample": True,
                "explanation": "4 closest integers to 3 are [1, 2, 3, 4]."
            },
            {
                "input_data": "[1, 1, 2, 3, 4, 5]\n4\n-1",
                "expected_output": "[1, 1, 2, 3]",
                "is_sample": True,
                "explanation": "Closest to negative number."
            },
            {
                "input_data": "[1, 2]\n1\n1",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Closest is 1."
            }
        ]
    },
    {
        "title": "Sort Characters By Frequency",
        "slug": "sort-characters-by-frequency",
        "topic": "Heap",
        "difficulty": "Medium",
        "description": "Given a string `s`, sort it in decreasing order based on the frequency of the characters.",
        "constraints": "1 <= s.length <= 5 * 10^5\nOptimal Time: O(n log k), Space: O(n)",
        "hints": [
            "Count frequencies and sort characters by count descending."
        ],
        "starter_code": {
            "python": "def frequencySort(s: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function frequencySort(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String frequencySort(String s) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string frequencySort(string s) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"tree\"",
                "expected_output": "\"eert\"",
                "is_sample": True,
                "explanation": "'e' appears twice, 'r' and 't' once."
            },
            {
                "input_data": "\"cccaaa\"",
                "expected_output": "\"cccaaa\"",
                "is_sample": True,
                "explanation": "'c' and 'a' both appear three times."
            },
            {
                "input_data": "\"Aabb\"",
                "expected_output": "\"bbAa\"",
                "is_sample": False,
                "explanation": "'b' is most frequent."
            }
        ]
    },
    {
        "title": "Task Scheduler",
        "slug": "task-scheduler",
        "topic": "Heap",
        "difficulty": "Medium",
        "description": "Given a characters array `tasks`, representing the tasks a CPU needs to do, and a non-negative integer `n` representing the cooldown period, return the least number of intervals the CPU will take to finish all tasks.",
        "constraints": "1 <= tasks.length <= 10^4\n0 <= n <= 100\nOptimal Time: O(tasks), Space: O(1)",
        "hints": [
            "Formula based on the maximum frequency count: (max_freq - 1) * (n + 1) + num_max_freq."
        ],
        "starter_code": {
            "python": "def leastInterval(tasks: list[str], n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function leastInterval(tasks, n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int leastInterval(char[] tasks, int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int leastInterval(vector<char>& tasks, int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"A\", \"A\", \"A\", \"B\", \"B\", \"B\"]\n2",
                "expected_output": "8",
                "is_sample": True,
                "explanation": "A -> B -> idle -> A -> B -> idle -> A -> B (8 units)."
            },
            {
                "input_data": "[\"A\", \"C\", \"A\", \"B\", \"D\", \"B\"]\n1",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "No idle needed."
            },
            {
                "input_data": "[\"A\", \"A\", \"A\", \"B\", \"B\", \"B\"]\n0",
                "expected_output": "6",
                "is_sample": False,
                "explanation": "Zero cooldown."
            }
        ]
    },
    {
        "title": "Reorganize String",
        "slug": "reorganize-string",
        "topic": "Heap",
        "difficulty": "Medium",
        "description": "Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same. Return `\"\"` if not possible.",
        "constraints": "1 <= s.length <= 500\nOptimal Time: O(n log A), Space: O(A)",
        "hints": [
            "Max-heap of characters by count; greedily pick top two distinct characters."
        ],
        "starter_code": {
            "python": "def reorganizeString(s: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function reorganizeString(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String reorganizeString(String s) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string reorganizeString(string s) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"aab\"",
                "expected_output": "\"aba\"",
                "is_sample": True,
                "explanation": "\"aba\" has no adjacent duplicates."
            },
            {
                "input_data": "\"aaab\"",
                "expected_output": "\"\"",
                "is_sample": True,
                "explanation": "Impossible, return empty string."
            },
            {
                "input_data": "\"vvvlo\"",
                "expected_output": "\"vlvov\"",
                "is_sample": False,
                "explanation": "Valid rearrangement."
            }
        ]
    },
    {
        "title": "Kth Smallest Element in a Sorted Matrix",
        "slug": "kth-smallest-element-in-a-sorted-matrix",
        "topic": "Heap",
        "difficulty": "Medium",
        "description": "Given an `n x n` matrix where each of the rows and columns is sorted in ascending order, return the `k-th` smallest element in the matrix.",
        "constraints": "n == matrix.length == matrix[i].length\n1 <= n <= 300\n-10^9 <= matrix[i][j] <= 10^9\nOptimal Time: O(n log(max - min)), Space: O(1)",
        "hints": [
            "Binary search on range [matrix[0][0], matrix[n-1][n-1]] counting elements <= mid."
        ],
        "starter_code": {
            "python": "def kthSmallestMatrix(matrix: list[list[int]], k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function kthSmallestMatrix(matrix, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int kthSmallestMatrix(int[][] matrix, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int kthSmallestMatrix(vector<vector<int>>& matrix, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 5, 9], [10, 11, 13], [12, 13, 15]]\n8",
                "expected_output": "13",
                "is_sample": True,
                "explanation": "8th smallest element is 13."
            },
            {
                "input_data": "[[-5]]\n1",
                "expected_output": "-5",
                "is_sample": True,
                "explanation": "Single item."
            },
            {
                "input_data": "[[1, 2], [1, 3]]\n2",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "2nd element is 1."
            }
        ]
    },
    {
        "title": "Find Median from Data Stream",
        "slug": "find-median-from-data-stream",
        "topic": "Heap",
        "difficulty": "Hard",
        "description": "Design a data structure that supports adding integer numbers from the data stream and finding the median of the current numbers in `O(log n)` and `O(1)` respectively.",
        "constraints": "-10^5 <= num <= 10^5\nAt most 5 * 10^4 calls\nOptimal Time: O(log n) addNum, O(1) findMedian",
        "hints": [
            "Two heaps: a max-heap for lower half and a min-heap for upper half."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"MedianFinder\", \"addNum\", \"addNum\", \"findMedian\", \"addNum\", \"findMedian\"]\n[[], [1], [2], [], [3], []]",
                "expected_output": "[None, None, None, 1.5, None, 2.0]",
                "is_sample": True,
                "explanation": "Median updates dynamically."
            },
            {
                "input_data": "[\"MedianFinder\", \"addNum\", \"findMedian\"]\n[[], [5], []]",
                "expected_output": "[None, None, 5.0]",
                "is_sample": True,
                "explanation": "Single item."
            },
            {
                "input_data": "[\"MedianFinder\", \"addNum\", \"addNum\", \"findMedian\"]\n[[], [-1], [-2], []]",
                "expected_output": "[None, None, None, -1.5]",
                "is_sample": False,
                "explanation": "Negative numbers."
            }
        ]
    },
    {
        "title": "IPO",
        "slug": "ipo",
        "topic": "Heap",
        "difficulty": "Hard",
        "description": "Suppose LeetCode will start its IPO soon. To maximize capital, select at most `k` distinct projects from available projects with profits and capital requirements. Return the final maximized capital.",
        "constraints": "1 <= k <= 10^5\n0 <= w <= 10^9\n1 <= profits.length <= 10^5\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Sort projects by capital requirement; push available projects to max-heap of profits."
        ],
        "starter_code": {
            "python": "def findMaximizedCapital(k: int, w: int, profits: list[int], capital: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findMaximizedCapital(k, w, profits, capital) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findMaximizedCapital(int k, int w, vector<int>& profits, vector<int>& capital) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2\n0\n[1, 2, 3]\n[0, 1, 1]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Start with capital 0 -> project 0 (capital 0, profit 1) -> w=1 -> project 2 (capital 1, profit 3) -> w=4."
            },
            {
                "input_data": "3\n0\n[1, 2, 3]\n[0, 1, 2]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "Final capital 6."
            },
            {
                "input_data": "1\n2\n[1, 2, 3]\n[1, 1, 2]",
                "expected_output": "5",
                "is_sample": False,
                "explanation": "Pick project with profit 3."
            }
        ]
    }
]
