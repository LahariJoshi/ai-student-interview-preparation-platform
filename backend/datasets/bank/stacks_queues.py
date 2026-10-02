"""
stacks_queues.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Min Stack",
        "slug": "min-stack",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.",
        "constraints": "-2^31 <= val <= 2^31 - 1\nAt most 3 * 10^4 calls\nOptimal Time: O(1) for all ops, Space: O(n)",
        "hints": [
            "Store pairs of (val, current_min) in the stack."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"MinStack\", \"push\", \"push\", \"push\", \"getMin\", \"pop\", \"top\", \"getMin\"]\n[[], [-2], [0], [-3], [], [], [], []]",
                "expected_output": "[None, None, None, None, -3, None, 0, -2]",
                "is_sample": True,
                "explanation": "MinStack operations."
            },
            {
                "input_data": "[\"MinStack\", \"push\", \"getMin\"]\n[[], [1], []]",
                "expected_output": "[None, None, 1]",
                "is_sample": True,
                "explanation": "Single item."
            },
            {
                "input_data": "[\"MinStack\", \"push\", \"push\", \"getMin\"]\n[[], [2], [2], []]",
                "expected_output": "[None, None, None, 2]",
                "is_sample": False,
                "explanation": "Duplicate mins."
            }
        ]
    },
    {
        "title": "Implement Queue using Stacks",
        "slug": "implement-queue-using-stacks",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Implement a first in first out (FIFO) queue using only two stacks.",
        "constraints": "1 <= x <= 9\nAt most 100 calls\nOptimal Time: O(1) amortized, Space: O(n)",
        "hints": [
            "Use in_stack for push and out_stack for pop/peek."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"MyQueue\", \"push\", \"push\", \"peek\", \"pop\", \"empty\"]\n[[], [1], [2], [], [], []]",
                "expected_output": "[None, None, None, 1, 1, False]",
                "is_sample": True,
                "explanation": "FIFO behavior."
            },
            {
                "input_data": "[\"MyQueue\", \"push\", \"pop\", \"empty\"]\n[[], [5], [], []]",
                "expected_output": "[None, None, 5, True]",
                "is_sample": True,
                "explanation": "Pushed then popped."
            },
            {
                "input_data": "[\"MyQueue\", \"empty\"]\n[[]]",
                "expected_output": "[None, True]",
                "is_sample": False,
                "explanation": "Empty queue."
            }
        ]
    },
    {
        "title": "Implement Stack using Queues",
        "slug": "implement-stack-using-queues",
        "topic": "Queue",
        "difficulty": "Easy",
        "description": "Implement a last-in-first-out (LIFO) stack using only standard queue operations.",
        "constraints": "1 <= x <= 9\nAt most 100 calls\nOptimal Time: O(n) push, O(1) pop",
        "hints": [
            "Rotate the queue by n-1 elements after every push."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"MyStack\", \"push\", \"push\", \"top\", \"pop\", \"empty\"]\n[[], [1], [2], [], [], []]",
                "expected_output": "[None, None, None, 2, 2, False]",
                "is_sample": True,
                "explanation": "LIFO behavior."
            },
            {
                "input_data": "[\"MyStack\", \"push\", \"pop\", \"empty\"]\n[[], [10], [], []]",
                "expected_output": "[None, None, 10, True]",
                "is_sample": True,
                "explanation": "Empty stack."
            },
            {
                "input_data": "[\"MyStack\", \"empty\"]\n[[]]",
                "expected_output": "[None, True]",
                "is_sample": False,
                "explanation": "Initially empty."
            }
        ]
    },
    {
        "title": "Backspace String Compare",
        "slug": "backspace-string-compare",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Given two strings `s` and `t`, return `True` if they are equal when both are typed into empty text editors. `'#'` means a backspace character.",
        "constraints": "1 <= s.length, t.length <= 200\nOptimal Time: O(n), Space: O(1) or O(n)",
        "hints": [
            "Simulate with a stack or iterate backwards with skip count."
        ],
        "starter_code": {
            "python": "def backspaceCompare(s: str, t: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function backspaceCompare(s, t) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean backspaceCompare(String s, String t) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool backspaceCompare(string s, string t) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"ab#c\"\n\"ad#c\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Both become \"ac\"."
            },
            {
                "input_data": "\"ab##\"\n\"c#d#\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Both become \"\"."
            },
            {
                "input_data": "\"a#c\"\n\"b\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "\"c\" != \"b\"."
            }
        ]
    },
    {
        "title": "Baseball Game",
        "slug": "baseball-game",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "You are keeping the scores for a baseball game with strange rules. Return the sum of all the scores on the record after applying operations: integer (add score), '+' (sum previous two), 'D' (double previous), 'C' (invalidate previous).",
        "constraints": "1 <= operations.length <= 1000\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Use a stack to maintain valid scores."
        ],
        "starter_code": {
            "python": "def calPoints(operations: list[str]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function calPoints(operations) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int calPoints(String[] operations) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int calPoints(vector<string>& operations) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"5\", \"2\", \"C\", \"D\", \"+\"]",
                "expected_output": "30",
                "is_sample": True,
                "explanation": "Score record: [5], [5, 2], [5], [5, 10], [5, 10, 15] -> sum 30."
            },
            {
                "input_data": "[\"5\", \"-2\", \"4\", \"C\", \"D\", \"9\", \"+\", \"+\"]",
                "expected_output": "27",
                "is_sample": True,
                "explanation": "Sum 27."
            },
            {
                "input_data": "[\"1\"]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single score 1."
            }
        ]
    },
    {
        "title": "Daily Temperatures",
        "slug": "daily-temperatures",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature.",
        "constraints": "1 <= temperatures.length <= 10^5\n30 <= temperatures[i] <= 100\nOptimal Time: O(n), Space: O(n) (Monotonic Stack)",
        "hints": [
            "Use a monotonic decreasing stack storing indices."
        ],
        "starter_code": {
            "python": "def dailyTemperatures(temperatures: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function dailyTemperatures(temperatures) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] dailyTemperatures(int[] temperatures) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> dailyTemperatures(vector<int>& temperatures) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[73, 74, 75, 71, 69, 72, 76, 73]",
                "expected_output": "[1, 1, 4, 2, 1, 1, 0, 0]",
                "is_sample": True,
                "explanation": "Days to wait for warmer temp."
            },
            {
                "input_data": "[30, 40, 50, 60]",
                "expected_output": "[1, 1, 1, 0]",
                "is_sample": True,
                "explanation": "Always warmer next day."
            },
            {
                "input_data": "[30, 60, 90]",
                "expected_output": "[1, 1, 0]",
                "is_sample": False,
                "explanation": "Warmest day has 0."
            }
        ]
    },
    {
        "title": "Evaluate Reverse Polish Notation",
        "slug": "evaluate-reverse-polish-notation",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are `+`, `-`, `*`, and `/` (truncate toward zero).",
        "constraints": "1 <= tokens.length <= 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Operands push to stack; operator pops top two, calculates, and pushes result back."
        ],
        "starter_code": {
            "python": "def evalRPN(tokens: list[str]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function evalRPN(tokens) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int evalRPN(String[] tokens) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int evalRPN(vector<string>& tokens) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"2\", \"1\", \"+\", \"3\", \"*\"]",
                "expected_output": "9",
                "is_sample": True,
                "explanation": "((2 + 1) * 3) = 9."
            },
            {
                "input_data": "[\"4\", \"13\", \"5\", \"/\", \"+\"]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "(4 + (13 / 5)) = 6."
            },
            {
                "input_data": "[\"10\", \"6\", \"9\", \"3\", \"+\", \"-11\", \"*\", \"/\", \"*\", \"17\", \"+\", \"5\", \"+\"]",
                "expected_output": "22",
                "is_sample": False,
                "explanation": "Evaluation result 22."
            }
        ]
    },
    {
        "title": "Decode String",
        "slug": "decode-string",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Given an encoded string, return its decoded string. The encoding rule is: `k[encoded_string]`.",
        "constraints": "1 <= s.length <= 30\nOptimal Time: O(output length), Space: O(n)",
        "hints": [
            "Use a stack of (string_so_far, count) when encountering '['."
        ],
        "starter_code": {
            "python": "def decodeString(s: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function decodeString(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String decodeString(String s) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string decodeString(string s) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"3[a]2[bc]\"",
                "expected_output": "\"aaabcbc\"",
                "is_sample": True,
                "explanation": "Decoded string."
            },
            {
                "input_data": "\"3[a2[c]]\"",
                "expected_output": "\"accaccacc\"",
                "is_sample": True,
                "explanation": "Nested decoding."
            },
            {
                "input_data": "\"2[abc]3[cd]ef\"",
                "expected_output": "\"abcabccdcdcdef\"",
                "is_sample": False,
                "explanation": "Multiple chunks."
            }
        ]
    },
    {
        "title": "Next Greater Element II",
        "slug": "next-greater-element-ii",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Given a circular integer array `nums`, return the next greater number for every element in `nums`.",
        "constraints": "1 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Simulate array of double length (2 * n) with modulo arithmetic."
        ],
        "starter_code": {
            "python": "def nextGreaterElements(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function nextGreaterElements(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] nextGreaterElements(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> nextGreaterElements(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 1]",
                "expected_output": "[2, -1, 2]",
                "is_sample": True,
                "explanation": "Next greater in circular array."
            },
            {
                "input_data": "[1, 2, 3, 4, 3]",
                "expected_output": "[2, 3, 4, -1, 4]",
                "is_sample": True,
                "explanation": "Circular lookup."
            },
            {
                "input_data": "[5, 4, 3, 2, 1]",
                "expected_output": "[-1, 5, 5, 5, 5]",
                "is_sample": False,
                "explanation": "All circular to 5."
            }
        ]
    },
    {
        "title": "Asteroid Collision",
        "slug": "asteroid-collision",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "We are given an array `asteroids` of integers representing asteroids in a row. Find out the state of the asteroids after all collisions.",
        "constraints": "2 <= asteroids.length <= 10^4\n-1000 <= asteroids[i] <= 1000\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Collision only occurs when top of stack is moving right (>0) and current is moving left (<0)."
        ],
        "starter_code": {
            "python": "def asteroidCollision(asteroids: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function asteroidCollision(asteroids) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] asteroidCollision(int[] asteroids) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> asteroidCollision(vector<int>& asteroids) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[5, 10, -5]",
                "expected_output": "[5, 10]",
                "is_sample": True,
                "explanation": "10 destroys -5."
            },
            {
                "input_data": "[8, -8]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Both explode."
            },
            {
                "input_data": "[10, 2, -5]",
                "expected_output": "[10]",
                "is_sample": False,
                "explanation": "-5 destroys 2, then 10 destroys -5."
            }
        ]
    },
    {
        "title": "132 Pattern",
        "slug": "132-pattern",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Given an array of `n` integers `nums`, a 132 pattern is a subsequence of three integers `nums[i], nums[j] and nums[k]` such that `i < j < k` and `nums[i] < nums[k] < nums[j]`. Return `True` if there is a 132 pattern.",
        "constraints": "1 <= nums.length <= 2 * 10^5\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Scan backwards from the right, maintaining candidate for '2' in monotonic stack."
        ],
        "starter_code": {
            "python": "def find132pattern(nums: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function find132pattern(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean find132pattern(int[] nums) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool find132pattern(vector<int>& nums) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "No 132 pattern."
            },
            {
                "input_data": "[3, 1, 4, 2]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "[1, 4, 2] is 132 pattern."
            },
            {
                "input_data": "[-1, 3, 2, 0]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "[-1, 3, 2] is 132."
            }
        ]
    },
    {
        "title": "Online Stock Span",
        "slug": "online-stock-span",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day (consecutive days <= price).",
        "constraints": "1 <= price <= 10^5\nOptimal Time: O(1) amortized, Space: O(n)",
        "hints": [
            "Monotonic decreasing stack of (price, span)."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"StockSpanner\", \"next\", \"next\", \"next\", \"next\", \"next\", \"next\", \"next\"]\n[[], [100], [80], [60], [70], [60], [75], [85]]",
                "expected_output": "[None, 1, 1, 1, 2, 1, 4, 6]",
                "is_sample": True,
                "explanation": "Stock spans."
            },
            {
                "input_data": "[\"StockSpanner\", \"next\", \"next\"]\n[[], [10], [20]]",
                "expected_output": "[None, 1, 2]",
                "is_sample": True,
                "explanation": "Increasing prices."
            },
            {
                "input_data": "[\"StockSpanner\", \"next\"]\n[[], [5]]",
                "expected_output": "[None, 1]",
                "is_sample": False,
                "explanation": "Single quote."
            }
        ]
    },
    {
        "title": "Largest Rectangle in Histogram",
        "slug": "largest-rectangle-in-histogram",
        "topic": "Stack",
        "difficulty": "Hard",
        "description": "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        "constraints": "1 <= heights.length <= 10^5\n0 <= heights[i] <= 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Monotonic increasing stack of bar indices."
        ],
        "starter_code": {
            "python": "def largestRectangleArea(heights: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function largestRectangleArea(heights) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int largestRectangleArea(int[] heights) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int largestRectangleArea(vector<int>& heights) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 1, 5, 6, 2, 3]",
                "expected_output": "10",
                "is_sample": True,
                "explanation": "Rectangle formed by 5 and 6 has area 10."
            },
            {
                "input_data": "[2, 4]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Area 4."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single bar area 1."
            }
        ]
    },
    {
        "title": "Maximal Rectangle",
        "slug": "maximal-rectangle",
        "topic": "Stack",
        "difficulty": "Hard",
        "description": "Given a `rows x cols` binary `matrix` filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.",
        "constraints": "1 <= rows, cols <= 200\nmatrix[i][j] is '0' or '1'\nOptimal Time: O(rows * cols), Space: O(cols)",
        "hints": [
            "Convert each row into a histogram and call Largest Rectangle in Histogram."
        ],
        "starter_code": {
            "python": "def maximalRectangle(matrix: list[list[str]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maximalRectangle(matrix) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maximalRectangle(char[][] matrix) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maximalRectangle(vector<vector<char>>& matrix) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[\"1\", \"0\", \"1\", \"0\", \"0\"], [\"1\", \"0\", \"1\", \"1\", \"1\"], [\"1\", \"1\", \"1\", \"1\", \"1\"], [\"1\", \"0\", \"0\", \"1\", \"0\"]]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "Maximal rectangle area is 6."
            },
            {
                "input_data": "[[\"0\"]]",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "Zero area."
            },
            {
                "input_data": "[[\"1\"]]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Area 1."
            }
        ]
    },
    {
        "title": "Basic Calculator",
        "slug": "basic-calculator",
        "topic": "Stack",
        "difficulty": "Hard",
        "description": "Given a string `s` representing a valid expression with `+`, `-`, parentheses `(`, `)` and spaces, evaluate this expression and return its value.",
        "constraints": "1 <= s.length <= 3 * 10^5\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Keep running sum and sign. Push (res, sign) to stack on '('."
        ],
        "starter_code": {
            "python": "def calculate(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function calculate(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int calculate(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int calculate(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"1 + 1\"",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "1 + 1 = 2."
            },
            {
                "input_data": "\" 2-1 + 2 \"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "2 - 1 + 2 = 3."
            },
            {
                "input_data": "\"(1+(4+5+2)-3)+(6+8)\"",
                "expected_output": "23",
                "is_sample": False,
                "explanation": "Parentheses evaluated correctly."
            }
        ]
    }
]
