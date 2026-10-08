"""
backtracking.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Subsets",
        "slug": "subsets",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets.",
        "constraints": "1 <= nums.length <= 10\n-10 <= nums[i] <= 10\nAll the numbers of nums are unique.\nOptimal Time: O(n * 2^n), Space: O(n)",
        "hints": [
            "Each element can either be included or excluded from a subset."
        ],
        "starter_code": {
            "python": "def subsets(nums: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function subsets(nums) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> subsets(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> subsets(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "[[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]",
                "is_sample": True,
                "explanation": "All 8 subsets."
            },
            {
                "input_data": "[0]",
                "expected_output": "[[], [0]]",
                "is_sample": True,
                "explanation": "2 subsets."
            },
            {
                "input_data": "[1, 2]",
                "expected_output": "[[], [1], [2], [1, 2]]",
                "is_sample": False,
                "explanation": "4 subsets."
            }
        ]
    },
    {
        "title": "Subsets II",
        "slug": "subsets-ii",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` that may contain duplicates, return all possible subsets. The solution set must not contain duplicate subsets.",
        "constraints": "1 <= nums.length <= 10\nOptimal Time: O(n * 2^n), Space: O(n)",
        "hints": [
            "Sort array first; skip duplicates when nums[i] == nums[i-1] in same recursion level."
        ],
        "starter_code": {
            "python": "def subsetsWithDup(nums: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function subsetsWithDup(nums) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> subsetsWithDup(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> subsetsWithDup(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 2]",
                "expected_output": "[[], [1], [2], [1, 2], [2, 2], [1, 2, 2]]",
                "is_sample": True,
                "explanation": "Unique subsets without duplicates."
            },
            {
                "input_data": "[0]",
                "expected_output": "[[], [0]]",
                "is_sample": True,
                "explanation": "Single item."
            },
            {
                "input_data": "[4, 4, 4, 1, 4]",
                "expected_output": "[[], [1], [4], [1, 4], [4, 4], [1, 4, 4], [4, 4, 4], [1, 4, 4, 4], [4, 4, 4, 4], [1, 4, 4, 4, 4]]",
                "is_sample": False,
                "explanation": "Multiple duplicates."
            }
        ]
    },
    {
        "title": "Combination Sum",
        "slug": "combination-sum",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. The same number may be chosen from candidates an unlimited number of times.",
        "constraints": "1 <= candidates.length <= 30\n2 <= candidates[i] <= 40\n1 <= target <= 40\nOptimal Time: O(N^(T/M)), Space: O(T/M)",
        "hints": [
            "Backtrack allowing reuse of candidate at current index."
        ],
        "starter_code": {
            "python": "def combinationSum(candidates: list[int], target: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function combinationSum(candidates, target) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> combinationSum(int[] candidates, int target) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 3, 6, 7]\n7",
                "expected_output": "[[2, 2, 3], [7]]",
                "is_sample": True,
                "explanation": "Combinations summing to 7."
            },
            {
                "input_data": "[2, 3, 5]\n8",
                "expected_output": "[[2, 2, 2, 2], [2, 3, 3], [3, 5]]",
                "is_sample": True,
                "explanation": "Combinations summing to 8."
            },
            {
                "input_data": "[2]\n1",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Cannot form 1."
            }
        ]
    },
    {
        "title": "Combination Sum II",
        "slug": "combination-sum-ii",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given a collection of candidate numbers (`candidates`) and a target number (`target`), find all unique combinations in `candidates` where the candidate numbers sum to `target`. Each number in `candidates` may only be used once in the combination.",
        "constraints": "1 <= candidates.length <= 100\n1 <= target <= 30\nOptimal Time: O(2^n), Space: O(n)",
        "hints": [
            "Sort array and advance start index to i + 1; skip duplicate elements at same depth."
        ],
        "starter_code": {
            "python": "def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function combinationSum2(candidates, target) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> combinationSum2(int[] candidates, int target) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[10, 1, 2, 7, 6, 1, 5]\n8",
                "expected_output": "[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]",
                "is_sample": True,
                "explanation": "Unique combinations."
            },
            {
                "input_data": "[2, 5, 2, 1, 2]\n5",
                "expected_output": "[[1, 2, 2], [5]]",
                "is_sample": True,
                "explanation": "Combinations summing to 5."
            },
            {
                "input_data": "[1, 1]\n1",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "Single combination."
            }
        ]
    },
    {
        "title": "Permutations",
        "slug": "permutations",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.",
        "constraints": "1 <= nums.length <= 6\n-10 <= nums[i] <= 10\nOptimal Time: O(n * n!), Space: O(n)",
        "hints": [
            "Backtrack by swapping or maintaining a visited set of elements."
        ],
        "starter_code": {
            "python": "def permute(nums: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function permute(nums) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> permute(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> permute(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]",
                "is_sample": True,
                "explanation": "All 6 permutations."
            },
            {
                "input_data": "[0, 1]",
                "expected_output": "[[0, 1], [1, 0]]",
                "is_sample": True,
                "explanation": "2 permutations."
            },
            {
                "input_data": "[1]",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "Single item."
            }
        ]
    },
    {
        "title": "Permutations II",
        "slug": "permutations-ii",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given a collection of numbers, `nums`, that might contain duplicates, return all possible unique permutations in any order.",
        "constraints": "1 <= nums.length <= 8\nOptimal Time: O(n * n!), Space: O(n)",
        "hints": [
            "Use frequency map or sort and skip duplicates if previous duplicate not visited."
        ],
        "starter_code": {
            "python": "def permuteUnique(nums: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function permuteUnique(nums) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> permuteUnique(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> permuteUnique(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 1, 2]",
                "expected_output": "[[1, 1, 2], [1, 2, 1], [2, 1, 1]]",
                "is_sample": True,
                "explanation": "3 unique permutations."
            },
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]",
                "is_sample": True,
                "explanation": "All unique."
            },
            {
                "input_data": "[1, 1]",
                "expected_output": "[[1, 1]]",
                "is_sample": False,
                "explanation": "Single permutation."
            }
        ]
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "slug": "letter-combinations-of-a-phone-number",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent.",
        "constraints": "0 <= digits.length <= 4\nOptimal Time: O(4^n), Space: O(n)",
        "hints": [
            "Map each digit to letters, and backtrack build combinations."
        ],
        "starter_code": {
            "python": "def letterCombinations(digits: str) -> list[str]:\n    # Write your solution here\n    pass\n",
            "javascript": "function letterCombinations(digits) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<String> letterCombinations(String digits) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<string> letterCombinations(string digits) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"23\"",
                "expected_output": "[\"ad\", \"ae\", \"af\", \"bd\", \"be\", \"bf\", \"cd\", \"ce\", \"cf\"]",
                "is_sample": True,
                "explanation": "Letter combinations."
            },
            {
                "input_data": "\"\"",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty string returns empty list."
            },
            {
                "input_data": "\"2\"",
                "expected_output": "[\"a\", \"b\", \"c\"]",
                "is_sample": False,
                "explanation": "Single digit."
            }
        ]
    },
    {
        "title": "Word Search",
        "slug": "word-search",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given an `m x n` grid of characters `board` and a string `word`, return `True` if `word` exists in the grid.",
        "constraints": "1 <= m, n <= 6\n1 <= word.length <= 15\nOptimal Time: O(m * n * 3^L), Space: O(L)",
        "hints": [
            "Backtrack DFS with 4-directional search and cell marking."
        ],
        "starter_code": {
            "python": "def exist(board: list[list[str]], word: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function exist(board, word) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean exist(char[][] board, String word) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool exist(vector<vector<char>>& board, string word) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[\"A\", \"B\", \"C\", \"E\"], [\"S\", \"F\", \"C\", \"S\"], [\"A\", \"D\", \"E\", \"E\"]]\n\"ABCCED\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "\"ABCCED\" exists."
            },
            {
                "input_data": "[[\"A\", \"B\", \"C\", \"E\"], [\"S\", \"F\", \"C\", \"S\"], [\"A\", \"D\", \"E\", \"E\"]]\n\"SEE\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "\"SEE\" exists."
            },
            {
                "input_data": "[[\"A\", \"B\", \"C\", \"E\"], [\"S\", \"F\", \"C\", \"S\"], [\"A\", \"D\", \"E\", \"E\"]]\n\"ABCB\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Cannot reuse letter 'B'."
            }
        ]
    },
    {
        "title": "Palindrome Partitioning",
        "slug": "palindrome-partitioning",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitionings of `s`.",
        "constraints": "1 <= s.length <= 16\nOptimal Time: O(N * 2^N), Space: O(N)",
        "hints": [
            "Backtrack over all possible cut points; only recurse if current prefix is a palindrome."
        ],
        "starter_code": {
            "python": "def partitionPalindromes(s: str) -> list[list[str]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function partitionPalindromes(s) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<String>> partitionPalindromes(String s) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<string>> partitionPalindromes(string s) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"aab\"",
                "expected_output": "[[\"a\", \"a\", \"b\"], [\"aa\", \"b\"]]",
                "is_sample": True,
                "explanation": "2 valid partitionings."
            },
            {
                "input_data": "\"a\"",
                "expected_output": "[[\"a\"]]",
                "is_sample": True,
                "explanation": "Single char."
            },
            {
                "input_data": "\"racecar\"",
                "expected_output": "[[\"r\", \"a\", \"c\", \"e\", \"c\", \"a\", \"r\"], [\"r\", \"a\", \"cec\", \"a\", \"r\"], [\"r\", \"aceca\", \"r\"], [\"racecar\"]]",
                "is_sample": False,
                "explanation": "Multiple palindrome options."
            }
        ]
    },
    {
        "title": "Restore IP Addresses",
        "slug": "restore-ip-addresses",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "A valid IP address consists of exactly four integers separated by single dots. Each integer is between 0 and 255 (inclusive) and cannot have leading zeros. Return all possible valid IP addresses that can be formed from `s`.",
        "constraints": "1 <= s.length <= 20\nOptimal Time: O(3^4), Space: O(1)",
        "hints": [
            "Backtrack with 4 segments, each length 1 to 3."
        ],
        "starter_code": {
            "python": "def restoreIpAddresses(s: str) -> list[str]:\n    # Write your solution here\n    pass\n",
            "javascript": "function restoreIpAddresses(s) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<String> restoreIpAddresses(String s) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<string> restoreIpAddresses(string s) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"25525511135\"",
                "expected_output": "[\"255.255.11.135\", \"255.255.111.35\"]",
                "is_sample": True,
                "explanation": "2 valid IP configurations."
            },
            {
                "input_data": "\"0000\"",
                "expected_output": "[\"0.0.0.0\"]",
                "is_sample": True,
                "explanation": "\"0.0.0.0\"."
            },
            {
                "input_data": "\"101023\"",
                "expected_output": "[\"1.0.10.23\", \"1.0.102.3\", \"10.1.0.23\", \"10.10.2.3\", \"101.0.2.3\"]",
                "is_sample": False,
                "explanation": "Valid parses."
            }
        ]
    },
    {
        "title": "N-Queens",
        "slug": "n-queens",
        "topic": "Backtracking",
        "difficulty": "Hard",
        "description": "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Return all distinct solutions to the n-queens puzzle.",
        "constraints": "1 <= n <= 9\nOptimal Time: O(N!), Space: O(N)",
        "hints": [
            "Backtrack row by row; track occupied columns, positive diagonals (r + c), and negative diagonals (r - c)."
        ],
        "starter_code": {
            "python": "def solveNQueens(n: int) -> list[list[str]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function solveNQueens(n) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<String>> solveNQueens(int n) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<string>> solveNQueens(int n) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "4",
                "expected_output": "[[\".Q..\", \"...Q\", \"Q...\", \"..Q.\"], [\"..Q.\", \"Q...\", \"...Q\", \".Q..\"]]",
                "is_sample": True,
                "explanation": "2 distinct solutions for 4-queens."
            },
            {
                "input_data": "1",
                "expected_output": "[[\"Q\"]]",
                "is_sample": True,
                "explanation": "Single cell."
            },
            {
                "input_data": "2",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "No solutions for 2-queens."
            }
        ]
    },
    {
        "title": "Sudoku Solver",
        "slug": "sudoku-solver",
        "topic": "Backtracking",
        "difficulty": "Hard",
        "description": "Write a program to solve a Sudoku puzzle by filling the empty cells. Empty cells are indicated by the character `'.'`. You may assume that the given Sudoku puzzle has only one unique solution.",
        "constraints": "board.length == 9, board[i].length == 9\nOptimal Time: O(9^(empty cells)), Space: O(1)",
        "hints": [
            "Backtrack through each empty cell, trying digits '1' to '9' that satisfy row, col, and 3x3 box constraints."
        ],
        "starter_code": {
            "python": "def solveSudoku(board: list[list[str]]) -> list[list[str]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function solveSudoku(board) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public void solveSudoku(char[][] board) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    void solveSudoku(vector<vector<char>>& board) {\n        // Write your solution here\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[\"5\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"],[\"6\",\".\",\".\",\"1\",\"9\",\"5\",\".\",\".\",\".\"],[\".\",\"9\",\"8\",\".\",\".\",\".\",\".\",\"6\",\".\"],[\"8\",\".\",\".\",\".\",\"6\",\".\",\".\",\".\",\"3\"],[\"4\",\".\",\".\",\"8\",\".\",\"3\",\".\",\".\",\"1\"],[\"7\",\".\",\".\",\".\",\"2\",\".\",\".\",\".\",\"6\"],[\".\",\"6\",\".\",\".\",\".\",\".\",\"2\",\"8\",\".\"],[\".\",\".\",\".\",\"4\",\"1\",\"9\",\".\",\".\",\"5\"],[\".\",\".\",\".\",\".\",\"8\",\".\",\".\",\"7\",\"9\"]]",
                "expected_output": "[[\"5\", \"3\", \"4\", \"6\", \"7\", \"8\", \"9\", \"1\", \"2\"], [\"6\", \"7\", \"2\", \"1\", \"9\", \"5\", \"3\", \"4\", \"8\"], [\"1\", \"9\", \"8\", \"3\", \"4\", \"2\", \"5\", \"6\", \"7\"], [\"8\", \"5\", \"9\", \"7\", \"6\", \"1\", \"4\", \"2\", \"3\"], [\"4\", \"2\", \"6\", \"8\", \"5\", \"3\", \"7\", \"9\", \"1\"], [\"7\", \"1\", \"3\", \"9\", \"2\", \"4\", \"8\", \"5\", \"6\"], [\"9\", \"6\", \"1\", \"5\", \"3\", \"7\", \"2\", \"8\", \"4\"], [\"2\", \"8\", \"7\", \"4\", \"1\", \"9\", \"6\", \"3\", \"5\"], [\"3\", \"4\", \"5\", \"2\", \"8\", \"6\", \"1\", \"7\", \"9\"]]",
                "is_sample": True,
                "explanation": "Completed Sudoku solution."
            },
            {
                "input_data": "[[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],[\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"]]",
                "expected_output": "[[\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"], [\"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"1\", \"2\", \"3\"], [\"7\", \"8\", \"9\", \"1\", \"2\", \"3\", \"4\", \"5\", \"6\"], [\"2\", \"1\", \"4\", \"3\", \"6\", \"5\", \"8\", \"9\", \"7\"], [\"3\", \"6\", \"5\", \"8\", \"9\", \"7\", \"2\", \"1\", \"4\"], [\"8\", \"9\", \"7\", \"2\", \"1\", \"4\", \"3\", \"6\", \"5\"], [\"5\", \"3\", \"1\", \"6\", \"4\", \"2\", \"9\", \"7\", \"8\"], [\"6\", \"4\", \"2\", \"9\", \"7\", \"8\", \"5\", \"3\", \"1\"], [\"9\", \"7\", \"8\", \"5\", \"3\", \"1\", \"6\", \"4\", \"2\"]]",
                "is_sample": True,
                "explanation": "Valid board."
            },
            {
                "input_data": "[[\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\"],[\"4\",\"5\",\"6\",\"7\",\"8\",\"9\",\"1\",\"2\",\"3\"],[\"7\",\"8\",\"9\",\"1\",\"2\",\"3\",\"4\",\"5\",\"6\"],[\"2\",\"1\",\"4\",\"3\",\"6\",\"5\",\"8\",\"9\",\"7\"],[\"3\",\"6\",\"5\",\"8\",\"9\",\"7\",\"2\",\"1\",\"4\"],[\"8\",\"9\",\"7\",\"2\",\"1\",\"4\",\"3\",\"6\",\"5\"],[\"5\",\"3\",\"1\",\"6\",\"4\",\"2\",\"9\",\"7\",\"8\"],[\"6\",\"4\",\"2\",\"9\",\"7\",\"8\",\"5\",\"3\",\"1\"],[\"9\",\"7\",\"8\",\"5\",\"3\",\"1\",\"6\",\"4\",\".\"]]",
                "expected_output": "[[\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\"], [\"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"1\", \"2\", \"3\"], [\"7\", \"8\", \"9\", \"1\", \"2\", \"3\", \"4\", \"5\", \"6\"], [\"2\", \"1\", \"4\", \"3\", \"6\", \"5\", \"8\", \"9\", \"7\"], [\"3\", \"6\", \"5\", \"8\", \"9\", \"7\", \"2\", \"1\", \"4\"], [\"8\", \"9\", \"7\", \"2\", \"1\", \"4\", \"3\", \"6\", \"5\"], [\"5\", \"3\", \"1\", \"6\", \"4\", \"2\", \"9\", \"7\", \"8\"], [\"6\", \"4\", \"2\", \"9\", \"7\", \"8\", \"5\", \"3\", \"1\"], [\"9\", \"7\", \"8\", \"5\", \"3\", \"1\", \"6\", \"4\", \"2\"]]",
                "is_sample": False,
                "explanation": "Last cell filled."
            }
        ]
    }
]
