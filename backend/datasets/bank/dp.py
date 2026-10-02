"""
dp.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "description": "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "constraints": "1 <= n <= 45\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Base cases: ways(1) = 1, ways(2) = 2. For n > 2: ways(n) = ways(n-1) + ways(n-2)."
        ],
        "starter_code": {
            "python": "def climbStairs(n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function climbStairs(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int climbStairs(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int climbStairs(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "1 step + 1 step, or 2 steps."
            },
            {
                "input_data": "3",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "1+1+1, 1+2, 2+1."
            },
            {
                "input_data": "5",
                "expected_output": "8",
                "is_sample": False,
                "explanation": "Fibonacci(5) = 8."
            }
        ]
    },
    {
        "title": "Min Cost Climbing Stairs",
        "slug": "min-cost-climbing-stairs",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "description": "You are given an integer array `cost` where `cost[i]` is the cost of `i-th` step on a staircase. Once you pay the cost, you can climb either 1 or 2 steps. Return the minimum cost to reach the top of the floor.",
        "constraints": "2 <= cost.length <= 1000\n0 <= cost[i] <= 999\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "dp[i] = cost[i] + min(dp[i-1], dp[i-2])."
        ],
        "starter_code": {
            "python": "def minCostClimbingStairs(cost: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function minCostClimbingStairs(cost) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int minCostClimbingStairs(int[] cost) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int minCostClimbingStairs(vector<int>& cost) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[10, 15, 20]",
                "expected_output": "15",
                "is_sample": True,
                "explanation": "Start at index 1 (cost 15), climb 2 steps."
            },
            {
                "input_data": "[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "Min cost is 6."
            },
            {
                "input_data": "[0, 0]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Zero cost."
            }
        ]
    },
    {
        "title": "N-th Tribonacci Number",
        "slug": "n-th-tribonacci-number",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "description": "The Tribonacci sequence Tn is defined as: T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0. Given `n`, return the value of Tn.",
        "constraints": "0 <= n <= 37\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Three variables a, b, c updating iteratively."
        ],
        "starter_code": {
            "python": "def tribonacci(n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function tribonacci(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int tribonacci(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int tribonacci(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "4",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "T4 = 1 + 1 + 2 = 4."
            },
            {
                "input_data": "25",
                "expected_output": "1389537",
                "is_sample": True,
                "explanation": "T25 = 1389537."
            },
            {
                "input_data": "0",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "T0 = 0."
            }
        ]
    },
    {
        "title": "Divisor Game",
        "slug": "divisor-game",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "description": "Alice and Bob take turns playing a game, with Alice starting first. If Alice wins assuming both players play optimally, return `True`. Otherwise, return `False`.",
        "constraints": "1 <= n <= 1000\nOptimal Time: O(1), Space: O(1)",
        "hints": [
            "If n is even, Alice can always choose x = 1 to hand Bob an odd number."
        ],
        "starter_code": {
            "python": "def divisorGame(n: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function divisorGame(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean divisorGame(int n) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool divisorGame(int n) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Alice chooses 1, and Bob has no moves."
            },
            {
                "input_data": "3",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Alice chooses 1, Bob chooses 1 and wins."
            },
            {
                "input_data": "4",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Even n wins."
            }
        ]
    },
    {
        "title": "Counting Bits",
        "slug": "counting-bits",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "description": "Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`'s in the binary representation of `i`.",
        "constraints": "0 <= n <= 10^5\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "dp[i] = dp[i >> 1] + (i & 1)."
        ],
        "starter_code": {
            "python": "def countBits(n: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function countBits(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] countBits(int n) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> countBits(int n) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2",
                "expected_output": "[0, 1, 1]",
                "is_sample": True,
                "explanation": "0: 0, 1: 1, 2: 10."
            },
            {
                "input_data": "5",
                "expected_output": "[0, 1, 1, 2, 1, 2]",
                "is_sample": True,
                "explanation": "Popcounts up to 5."
            },
            {
                "input_data": "0",
                "expected_output": "[0]",
                "is_sample": False,
                "explanation": "n = 0."
            }
        ]
    },
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "You are given an integer array `coins` representing coins of different denominations and an integer `amount`. Return the fewest number of coins that you need to make up that amount, or `-1` if not possible.",
        "constraints": "1 <= coins.length <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4\nOptimal Time: O(amount * len(coins)), Space: O(amount)",
        "hints": [
            "dp[i] = min(dp[i - coin] + 1 for coin in coins)."
        ],
        "starter_code": {
            "python": "def coinChange(coins: list[int], amount: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function coinChange(coins, amount) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int coinChange(int[] coins, int amount) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int coinChange(vector<int>& coins, int amount) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 5]\n11",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "11 = 5 + 5 + 1 (3 coins)."
            },
            {
                "input_data": "[2]\n3",
                "expected_output": "-1",
                "is_sample": True,
                "explanation": "Cannot form 3 using only 2s."
            },
            {
                "input_data": "[1]\n0",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "0 amount needs 0 coins."
            }
        ]
    },
    {
        "title": "Longest Increasing Subsequence",
        "slug": "longest-increasing-subsequence",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, return the length of the longest strictly increasing subsequence in `O(n log n)` time.",
        "constraints": "1 <= nums.length <= 2500\n-10^4 <= nums[i] <= 10^4\nOptimal Time: O(n log n), Space: O(n) (Patience Sorting / Bisect)",
        "hints": [
            "Maintain an array `tails` of smallest tail of all increasing subsequences of length i."
        ],
        "starter_code": {
            "python": "def lengthOfLIS(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function lengthOfLIS(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int lengthOfLIS(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int lengthOfLIS(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[10, 9, 2, 5, 3, 7, 101, 18]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "[2, 3, 7, 101] has length 4."
            },
            {
                "input_data": "[0, 1, 0, 3, 2, 3]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "[0, 1, 2, 3] length 4."
            },
            {
                "input_data": "[7, 7, 7, 7, 7, 7, 7]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Strictly increasing length is 1."
            }
        ]
    },
    {
        "title": "Word Break",
        "slug": "word-break",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of one or more dictionary words.",
        "constraints": "1 <= s.length <= 300\n1 <= wordDict.length <= 1000\nOptimal Time: O(n^2), Space: O(n)",
        "hints": [
            "dp[i] = any(dp[j] and s[j:i] in wordDict for j in range(i))."
        ],
        "starter_code": {
            "python": "def wordBreak(s: str, wordDict: list[str]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function wordBreak(s, wordDict) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean wordBreak(String s, List<String> wordDict) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool wordBreak(string s, vector<string>& wordDict) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"leetcode\"\n[\"leet\", \"code\"]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "\"leetcode\" can be segmented as \"leet code\"."
            },
            {
                "input_data": "\"applepenapple\"\n[\"apple\", \"pen\"]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Segmented as \"apple pen apple\"."
            },
            {
                "input_data": "\"catsandog\"\n[\"cats\", \"dog\", \"sand\", \"and\", \"cat\"]",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Cannot segment."
            }
        ]
    },
    {
        "title": "House Robber",
        "slug": "house-robber",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "You are a professional robber planning to rob houses along a street. Adjacent houses have security systems connected. Return the maximum amount of money you can rob tonight without alerting the police.",
        "constraints": "1 <= nums.length <= 100\n0 <= nums[i] <= 400\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "rob = max(rob_prev, not_rob_prev + nums[i])."
        ],
        "starter_code": {
            "python": "def rob(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function rob(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int rob(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int rob(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 1]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Rob house 1 (1) and house 3 (3) = 4."
            },
            {
                "input_data": "[2, 7, 9, 3, 1]",
                "expected_output": "12",
                "is_sample": True,
                "explanation": "Rob 2 + 9 + 1 = 12."
            },
            {
                "input_data": "[0]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "0 dollars."
            }
        ]
    },
    {
        "title": "House Robber II",
        "slug": "house-robber-ii",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "All houses at this place are arranged in a circle. Return the maximum amount of money you can rob tonight without alerting the police.",
        "constraints": "1 <= nums.length <= 100\n0 <= nums[i] <= 1000\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Run House Robber I twice: once for nums[:-1] and once for nums[1:]."
        ],
        "starter_code": {
            "python": "def rob2(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function rob2(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int rob2(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int rob2(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 3, 2]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Cannot rob both 2s because they are adjacent."
            },
            {
                "input_data": "[1, 2, 3, 1]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Rob house 1 and 3 = 4."
            },
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "3",
                "is_sample": False,
                "explanation": "Max is 3."
            }
        ]
    },
    {
        "title": "Unique Paths",
        "slug": "unique-paths",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "There is a robot on an `m x n` grid. The robot can only move either down or right at any point in time. Return the number of possible unique paths to the bottom-right corner.",
        "constraints": "1 <= m, n <= 100\nOptimal Time: O(m * n), Space: O(n)",
        "hints": [
            "dp[c] = dp[c] + dp[c - 1] (or combination formula C(m+n-2, m-1))."
        ],
        "starter_code": {
            "python": "def uniquePaths(m: int, n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function uniquePaths(m, n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int uniquePaths(int m, int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int uniquePaths(int m, int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "3\n7",
                "expected_output": "28",
                "is_sample": True,
                "explanation": "28 unique paths."
            },
            {
                "input_data": "3\n2",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 unique paths: D-R-D, D-D-R, R-D-D."
            },
            {
                "input_data": "1\n1",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single cell 1 path."
            }
        ]
    },
    {
        "title": "Unique Paths II",
        "slug": "unique-paths-ii",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "You are given an `m x n` integer array `obstacleGrid` where 1 represents an obstacle and 0 represents space. Return the number of possible unique paths to reach the bottom-right corner.",
        "constraints": "1 <= m, n <= 100\nOptimal Time: O(m * n), Space: O(n)",
        "hints": [
            "If cell has obstacle (1), paths = 0; else paths = from_top + from_left."
        ],
        "starter_code": {
            "python": "def uniquePathsWithObstacles(obstacleGrid: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function uniquePathsWithObstacles(obstacleGrid) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int uniquePathsWithObstacles(int[][] obstacleGrid) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[0, 0, 0], [0, 1, 0], [0, 0, 0]]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 paths around center obstacle."
            },
            {
                "input_data": "[[0, 1], [0, 0]]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 path."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Start blocked."
            }
        ]
    },
    {
        "title": "Jump Game",
        "slug": "jump-game",
        "topic": "Greedy",
        "difficulty": "Medium",
        "description": "You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `True` if you can reach the last index, or `False` otherwise.",
        "constraints": "1 <= nums.length <= 10^4\n0 <= nums[i] <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Keep track of the furthest reachable index."
        ],
        "starter_code": {
            "python": "def canJump(nums: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function canJump(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean canJump(int[] nums) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool canJump(vector<int>& nums) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 3, 1, 1, 4]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Jump 1 step from 0 to 1, then 3 steps to the last index."
            },
            {
                "input_data": "[3, 2, 1, 0, 4]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Stuck at index 3."
            },
            {
                "input_data": "[0]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Already at last index."
            }
        ]
    },
    {
        "title": "Jump Game II",
        "slug": "jump-game-ii",
        "topic": "Greedy",
        "difficulty": "Medium",
        "description": "Return the minimum number of jumps to reach the last index of `nums`.",
        "constraints": "1 <= nums.length <= 10^4\n0 <= nums[i] <= 1000\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "BFS level-by-level greedy: track current_end and furthest_reach."
        ],
        "starter_code": {
            "python": "def jump(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function jump(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int jump(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int jump(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 3, 1, 1, 4]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 jumps: index 0 -> 1 -> 4."
            },
            {
                "input_data": "[2, 3, 0, 1, 4]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 jumps."
            },
            {
                "input_data": "[1]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "0 jumps needed."
            }
        ]
    },
    {
        "title": "Partition Equal Subset Sum",
        "slug": "partition-equal-subset-sum",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal.",
        "constraints": "1 <= nums.length <= 200\n1 <= nums[i] <= 100\nOptimal Time: O(n * sum), Space: O(sum) (0/1 Knapsack)",
        "hints": [
            "Target sum is sum(nums) / 2. If sum is odd, return False immediately."
        ],
        "starter_code": {
            "python": "def canPartition(nums: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function canPartition(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean canPartition(int[] nums) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool canPartition(vector<int>& nums) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 5, 11, 5]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "[1, 5, 5] and [11]."
            },
            {
                "input_data": "[1, 2, 3, 5]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Cannot partition into equal sum."
            },
            {
                "input_data": "[2, 2]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Two equal elements."
            }
        ]
    },
    {
        "title": "Target Sum",
        "slug": "target-sum",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "You are given an integer array `nums` and an integer `target`. You want to build an expression out of nums by adding one of the symbols `'+'` and `'-'` before each integer in nums and then concatenate all the integers. Return the number of different expressions that you can build, which evaluates to `target`.",
        "constraints": "1 <= nums.length <= 20\n0 <= nums[i] <= 1000\n-1000 <= target <= 1000\nOptimal Time: O(n * sum), Space: O(sum)",
        "hints": [
            "Subset sum reduction: P = (target + sum(nums)) / 2."
        ],
        "starter_code": {
            "python": "def findTargetSumWays(nums: list[int], target: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findTargetSumWays(nums, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findTargetSumWays(int[] nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findTargetSumWays(vector<int>& nums, int target) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 1, 1, 1, 1]\n3",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "5 ways to assign symbols to reach 3."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "+1 = 1."
            },
            {
                "input_data": "[1]\n2",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Impossible."
            }
        ]
    },
    {
        "title": "Longest Common Subsequence",
        "slug": "longest-common-subsequence",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.",
        "constraints": "1 <= text1.length, text2.length <= 1000\nOptimal Time: O(m * n), Space: O(min(m, n))",
        "hints": [
            "If text1[i] == text2[j], dp[i][j] = 1 + dp[i-1][j-1]; else max(dp[i-1][j], dp[i][j-1])."
        ],
        "starter_code": {
            "python": "def longestCommonSubsequence(text1: str, text2: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function longestCommonSubsequence(text1, text2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int longestCommonSubsequence(String text1, String text2) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int longestCommonSubsequence(string text1, string text2) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"abcde\"\n\"ace\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "\"ace\" has length 3."
            },
            {
                "input_data": "\"abc\"\n\"abc\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Exact match length 3."
            },
            {
                "input_data": "\"abc\"\n\"def\"",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "No common subsequence."
            }
        ]
    },
    {
        "title": "Decode Ways",
        "slug": "decode-ways",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "A message containing letters from A-Z can be encoded into numbers using 'A' -> '1', ..., 'Z' -> '26'. Given a string `s` containing only digits, return the number of ways to decode it.",
        "constraints": "1 <= s.length <= 100\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Check 1-digit valid transitions (s[i] != '0') and 2-digit valid transitions (10 <= int(s[i-1:i+1]) <= 26)."
        ],
        "starter_code": {
            "python": "def numDecodings(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function numDecodings(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int numDecodings(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int numDecodings(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"12\"",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "\"AB\" (1 2) or \"L\" (12)."
            },
            {
                "input_data": "\"226\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "\"BZ\" (2 26), \"VF\" (22 6), or \"BBF\" (2 2 6)."
            },
            {
                "input_data": "\"06\"",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Leading zero invalid."
            }
        ]
    },
    {
        "title": "Coin Change II",
        "slug": "coin-change-ii",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "You are given an integer array `coins` representing coins of different denominations and an integer `amount`. Return the number of combinations that make up that amount.",
        "constraints": "1 <= coins.length <= 300\n1 <= coins[i] <= 5000\n0 <= amount <= 5000\nOptimal Time: O(amount * len(coins)), Space: O(amount)",
        "hints": [
            "Outer loop iterates over coins, inner loop updates dp[x] += dp[x - coin]."
        ],
        "starter_code": {
            "python": "def change(amount: int, coins: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function change(amount, coins) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int change(int amount, int[] coins) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int change(int amount, vector<int>& coins) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "5\n[1, 2, 5]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "5 = 5, 2+2+1, 2+1+1+1, 1+1+1+1+1 (4 ways)."
            },
            {
                "input_data": "3\n[2]",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "Cannot make 3 using only 2s."
            },
            {
                "input_data": "10\n[10]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "1 way."
            }
        ]
    },
    {
        "title": "Burst Balloons",
        "slug": "burst-balloons",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "You are given `n` balloons, indexed from 0 to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`. You are asked to burst all the balloons. Return the maximum coins you can collect by bursting balloons wisely.",
        "constraints": "n == nums.length\n1 <= n <= 300\n0 <= nums[i] <= 100\nOptimal Time: O(n^3), Space: O(n^2)",
        "hints": [
            "Interval DP: consider the LAST balloon to burst in interval (i, j)."
        ],
        "starter_code": {
            "python": "def maxCoins(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxCoins(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxCoins(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxCoins(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 1, 5, 8]",
                "expected_output": "167",
                "is_sample": True,
                "explanation": "Max coins is 167."
            },
            {
                "input_data": "[1, 5]",
                "expected_output": "10",
                "is_sample": True,
                "explanation": "Max coins 10."
            },
            {
                "input_data": "[7]",
                "expected_output": "7",
                "is_sample": False,
                "explanation": "1 * 7 * 1 = 7."
            }
        ]
    },
    {
        "title": "Russian Doll Envelopes",
        "slug": "russian-doll-envelopes",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "You are given a 2D array of integers `envelopes` where `envelopes[i] = [wi, hi]`. One envelope can fit into another if and only if both the width and height of one envelope are strictly greater than the other. Return the maximum number of envelopes you can Russian doll.",
        "constraints": "1 <= envelopes.length <= 10^5\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Sort by width ascending and height descending, then find LIS on heights."
        ],
        "starter_code": {
            "python": "def maxEnvelopes(envelopes: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxEnvelopes(envelopes) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxEnvelopes(int[][] envelopes) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxEnvelopes(vector<vector<int>>& envelopes) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[5, 4], [6, 4], [6, 7], [2, 3]]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "[2, 3] => [5, 4] => [6, 7] (3 envelopes)."
            },
            {
                "input_data": "[[1, 1], [1, 1], [1, 1]]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Only 1 can be chosen."
            },
            {
                "input_data": "[[10, 8], [1, 12], [6, 15], [2, 18]]",
                "expected_output": "2",
                "is_sample": False,
                "explanation": "Max chain length 2."
            }
        ]
    },
    {
        "title": "Longest Valid Parentheses",
        "slug": "longest-valid-parentheses",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Given a string containing just the characters `'('` and `')'`, return the length of the longest valid (well-formed) parentheses substring.",
        "constraints": "0 <= s.length <= 3 * 10^4\nOptimal Time: O(n), Space: O(n) or O(1)",
        "hints": [
            "Stack initialized with -1 to hold last invalid index, or two-pass counting."
        ],
        "starter_code": {
            "python": "def longestValidParentheses(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function longestValidParentheses(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int longestValidParentheses(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int longestValidParentheses(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"(()\"",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Longest valid is \"()\" length 2."
            },
            {
                "input_data": "\")()())\"",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "\"()()\" length 4."
            },
            {
                "input_data": "\"\"",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Empty string."
            }
        ]
    },
    {
        "title": "Super Egg Drop",
        "slug": "super-egg-drop",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "You are given `k` identical eggs and you have access to a building with `n` floors labeled from 1 to `n`. Find the minimum number of moves that you need to determine with certainty what the highest floor is from which an egg will not break.",
        "constraints": "1 <= k <= 100\n1 <= n <= 10^4\nOptimal Time: O(k log n), Space: O(k)",
        "hints": [
            "Invert the problem: dp[m][k] is the maximum floors we can test with m moves and k eggs."
        ],
        "starter_code": {
            "python": "def superEggDrop(k: int, n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function superEggDrop(k, n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int superEggDrop(int k, int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int superEggDrop(int k, int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "1\n2",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Drop from floor 1, if it doesn't break, drop from floor 2."
            },
            {
                "input_data": "2\n6",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 drops with 2 eggs."
            },
            {
                "input_data": "3\n14",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "4 drops."
            }
        ]
    }
]
