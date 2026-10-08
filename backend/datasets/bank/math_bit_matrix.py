"""
math_bit_matrix.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Number of 1 Bits",
        "slug": "number-of-1-bits",
        "topic": "Bit Manipulation",
        "difficulty": "Easy",
        "description": "Given a positive integer `n`, write a function that returns the number of set bits it has (also known as the Hamming weight).",
        "constraints": "1 <= n <= 2^31 - 1\nOptimal Time: O(1), Space: O(1)",
        "hints": [
            "Repeatedly drop the lowest set bit using n & (n - 1)."
        ],
        "starter_code": {
            "python": "def hammingWeight(n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function hammingWeight(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int hammingWeight(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int hammingWeight(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "11",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "11 in binary is 1011 (3 set bits)."
            },
            {
                "input_data": "128",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "128 in binary is 10000000 (1 set bit)."
            },
            {
                "input_data": "2147483645",
                "expected_output": "30",
                "is_sample": False,
                "explanation": "30 set bits."
            }
        ]
    },
    {
        "title": "Reverse Bits",
        "slug": "reverse-bits",
        "topic": "Bit Manipulation",
        "difficulty": "Easy",
        "description": "Reverse bits of a given 32 bits unsigned integer.",
        "constraints": "The input must be a binary string of length 32.\nOptimal Time: O(1), Space: O(1)",
        "hints": [
            "Extract last bit with n & 1 and shift into reversed result."
        ],
        "starter_code": {
            "python": "def reverseBits(n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function reverseBits(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int reverseBits(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int reverseBits(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "43261596",
                "expected_output": "964176192",
                "is_sample": True,
                "explanation": "Bits reversed."
            },
            {
                "input_data": "1",
                "expected_output": "2147483648",
                "is_sample": True,
                "explanation": "Bit 0 becomes bit 31."
            },
            {
                "input_data": "0",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Zero reversed is zero."
            }
        ]
    },
    {
        "title": "Missing Number",
        "slug": "missing-number",
        "topic": "Bit Manipulation",
        "difficulty": "Easy",
        "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "constraints": "n == nums.length\n1 <= n <= 10^4\n0 <= nums[i] <= n\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "XOR all numbers from 0 to n and all elements in nums, or use Gauss formula n*(n+1)//2 - sum(nums)."
        ],
        "starter_code": {
            "python": "def missingNumber(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function missingNumber(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int missingNumber(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int missingNumber(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 0, 1]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "n = 3, 2 is missing."
            },
            {
                "input_data": "[0, 1]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "n = 2, 2 is missing."
            },
            {
                "input_data": "[9, 6, 4, 2, 3, 5, 7, 0, 1]",
                "expected_output": "8",
                "is_sample": False,
                "explanation": "8 is missing."
            }
        ]
    },
    {
        "title": "Palindrome Number",
        "slug": "palindrome-number",
        "topic": "Math",
        "difficulty": "Easy",
        "description": "Given an integer `x`, return `True` if `x` is a palindrome, and `False` otherwise.",
        "constraints": "-2^31 <= x <= 2^31 - 1\nOptimal Time: O(log10(x)), Space: O(1)",
        "hints": [
            "Negative numbers cannot be palindromes. Reverse half the number and compare."
        ],
        "starter_code": {
            "python": "def isPalindromeNum(x: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isPalindromeNum(x) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isPalindromeNum(int x) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isPalindromeNum(int x) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "121",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "121 reads same both ways."
            },
            {
                "input_data": "-121",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "-121 reads 121- backwards."
            },
            {
                "input_data": "10",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "01 != 10."
            }
        ]
    },
    {
        "title": "Excel Sheet Column Title",
        "slug": "excel-sheet-column-title",
        "topic": "Math",
        "difficulty": "Easy",
        "description": "Given an integer `columnNumber`, return its corresponding column title as it appears in an Excel sheet (e.g. 1 -> 'A', 28 -> 'AB').",
        "constraints": "1 <= columnNumber <= 2^31 - 1\nOptimal Time: O(log26(n)), Space: O(1)",
        "hints": [
            "Base-26 with 1-based indexing: columnNumber = (columnNumber - 1) // 26."
        ],
        "starter_code": {
            "python": "def convertToTitle(columnNumber: int) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function convertToTitle(columnNumber) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String convertToTitle(int columnNumber) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string convertToTitle(int columnNumber) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "1",
                "expected_output": "\"A\"",
                "is_sample": True,
                "explanation": "1 -> \"A\"."
            },
            {
                "input_data": "28",
                "expected_output": "\"AB\"",
                "is_sample": True,
                "explanation": "28 -> \"AB\"."
            },
            {
                "input_data": "701",
                "expected_output": "\"ZY\"",
                "is_sample": False,
                "explanation": "701 -> \"ZY\"."
            }
        ]
    },
    {
        "title": "Plus One",
        "slug": "plus-one",
        "topic": "Array",
        "difficulty": "Easy",
        "description": "You are given a large integer represented as an integer array `digits`. Increment the large integer by one and return the resulting array of digits.",
        "constraints": "1 <= digits.length <= 100\n0 <= digits[i] <= 9\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Traverse backwards: if digit < 9, increment and return; if 9, set to 0 and carry."
        ],
        "starter_code": {
            "python": "def plusOne(digits: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function plusOne(digits) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] plusOne(int[] digits) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> plusOne(vector<int>& digits) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "[1, 2, 4]",
                "is_sample": True,
                "explanation": "123 + 1 = 124."
            },
            {
                "input_data": "[4, 3, 2, 1]",
                "expected_output": "[4, 3, 2, 2]",
                "is_sample": True,
                "explanation": "4321 + 1 = 4322."
            },
            {
                "input_data": "[9]",
                "expected_output": "[1, 0]",
                "is_sample": False,
                "explanation": "9 + 1 = 10."
            }
        ]
    },
    {
        "title": "Add Binary",
        "slug": "add-binary",
        "topic": "Math",
        "difficulty": "Easy",
        "description": "Given two binary strings `a` and `b`, return their sum as a binary string.",
        "constraints": "1 <= a.length, b.length <= 10^4\na and b consist only of '0' or '1' characters.\nOptimal Time: O(max(a, b)), Space: O(max(a, b))",
        "hints": [
            "Simulate binary addition with carry."
        ],
        "starter_code": {
            "python": "def addBinary(a: str, b: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function addBinary(a, b) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String addBinary(String a, String b) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string addBinary(string a, string b) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"11\"\n\"1\"",
                "expected_output": "\"100\"",
                "is_sample": True,
                "explanation": "3 + 1 = 4 (\"100\")."
            },
            {
                "input_data": "\"1010\"\n\"1011\"",
                "expected_output": "\"10101\"",
                "is_sample": True,
                "explanation": "10 + 11 = 21 (\"10101\")."
            },
            {
                "input_data": "\"0\"\n\"0\"",
                "expected_output": "\"0\"",
                "is_sample": False,
                "explanation": "0 + 0 = 0."
            }
        ]
    },
    {
        "title": "Power of Three",
        "slug": "power-of-three",
        "topic": "Math",
        "difficulty": "Easy",
        "description": "Given an integer `n`, return `True` if it is a power of three. Otherwise, return `False`.",
        "constraints": "-2^31 <= n <= 2^31 - 1\nOptimal Time: O(1), Space: O(1)",
        "hints": [
            "The maximum 32-bit power of 3 is 3^19 = 1162261467; n > 0 and 1162261467 % n == 0."
        ],
        "starter_code": {
            "python": "def isPowerOfThree(n: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isPowerOfThree(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isPowerOfThree(int n) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isPowerOfThree(int n) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "27",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "27 = 3^3."
            },
            {
                "input_data": "0",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "0 is not a power of 3."
            },
            {
                "input_data": "-1",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Negative is not power of 3."
            }
        ]
    },
    {
        "title": "Matrix Diagonal Sum",
        "slug": "matrix-diagonal-sum",
        "topic": "Matrix",
        "difficulty": "Easy",
        "description": "Given a square matrix `mat`, return the sum of the matrix diagonals (primary and secondary). Only include the center element once if n is odd.",
        "constraints": "n == mat.length == mat[i].length\n1 <= n <= 100\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Primary diagonal: mat[i][i]; Secondary diagonal: mat[i][n - 1 - i]."
        ],
        "starter_code": {
            "python": "def diagonalSum(mat: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function diagonalSum(mat) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int diagonalSum(int[][] mat) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int diagonalSum(vector<vector<int>>& mat) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                "expected_output": "25",
                "is_sample": True,
                "explanation": "(1 + 5 + 9) + (3 + 7) = 25."
            },
            {
                "input_data": "[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]",
                "expected_output": "8",
                "is_sample": True,
                "explanation": "8 ones on diagonals."
            },
            {
                "input_data": "[[5]]",
                "expected_output": "5",
                "is_sample": False,
                "explanation": "Single cell."
            }
        ]
    },
    {
        "title": "Transpose Matrix",
        "slug": "transpose-matrix",
        "topic": "Matrix",
        "difficulty": "Easy",
        "description": "Given a 2D integer array `matrix`, return the transpose of `matrix`.",
        "constraints": "1 <= m, n <= 1000\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "transpose[j][i] = matrix[i][j]."
        ],
        "starter_code": {
            "python": "def transpose(matrix: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function transpose(matrix) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[][] transpose(int[][] matrix) {\n        // Write your solution here\n        return new int[][]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> transpose(vector<vector<int>>& matrix) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                "expected_output": "[[1, 4, 7], [2, 5, 8], [3, 6, 9]]",
                "is_sample": True,
                "explanation": "Transposed matrix."
            },
            {
                "input_data": "[[1, 2, 3], [4, 5, 6]]",
                "expected_output": "[[1, 4], [2, 5], [3, 6]]",
                "is_sample": True,
                "explanation": "2x3 becomes 3x2."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "Single cell."
            }
        ]
    },
    {
        "title": "Reshape the Matrix",
        "slug": "reshape-the-matrix",
        "topic": "Matrix",
        "difficulty": "Easy",
        "description": "Given an `m x n` matrix `mat` and two integers `r` and `c`, reshape `mat` into an `r x c` matrix with the same row-traversing order. If impossible, return the original matrix.",
        "constraints": "1 <= m, n <= 100\n1 <= r, c <= 300\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "Check if m * n == r * c."
        ],
        "starter_code": {
            "python": "def matrixReshape(mat: list[list[int]], r: int, c: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function matrixReshape(mat, r, c) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[][] matrixReshape(int[][] mat, int r, int c) {\n        // Write your solution here\n        return new int[][]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> matrixReshape(vector<vector<int>>& mat, int r, int c) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2], [3, 4]]\n1\n4",
                "expected_output": "[[1, 2, 3, 4]]",
                "is_sample": True,
                "explanation": "Reshaped into 1x4."
            },
            {
                "input_data": "[[1, 2], [3, 4]]\n2\n4",
                "expected_output": "[[1, 2], [3, 4]]",
                "is_sample": True,
                "explanation": "Impossible, return original."
            },
            {
                "input_data": "[[1]]\n1\n1",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "1x1."
            }
        ]
    },
    {
        "title": "Richest Customer Wealth",
        "slug": "richest-customer-wealth",
        "topic": "Matrix",
        "difficulty": "Easy",
        "description": "You are given an `m x n` integer grid `accounts` where `accounts[i][j]` is the amount of money the `i-th` customer has in the `j-th` bank. Return the wealth that the richest customer has.",
        "constraints": "1 <= m, n <= 50\n1 <= accounts[i][j] <= 100\nOptimal Time: O(m * n), Space: O(1)",
        "hints": [
            "Calculate the sum of each row and find the maximum."
        ],
        "starter_code": {
            "python": "def maximumWealth(accounts: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maximumWealth(accounts) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maximumWealth(int[][] accounts) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maximumWealth(vector<vector<int>>& accounts) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2, 3], [3, 2, 1]]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "Both have wealth 6."
            },
            {
                "input_data": "[[1, 5], [7, 3], [3, 5]]",
                "expected_output": "10",
                "is_sample": True,
                "explanation": "2nd customer has wealth 10."
            },
            {
                "input_data": "[[2, 8, 7], [7, 1, 3], [1, 9, 5]]",
                "expected_output": "17",
                "is_sample": False,
                "explanation": "1st customer has 17."
            }
        ]
    },
    {
        "title": "Bitwise AND of Numbers Range",
        "slug": "bitwise-and-of-numbers-range",
        "topic": "Bit Manipulation",
        "difficulty": "Medium",
        "description": "Given two integers `left` and `right` that represent the range `[left, right]`, return the bitwise AND of all numbers in this range, inclusive.",
        "constraints": "0 <= left <= right <= 2^31 - 1\nOptimal Time: O(1), Space: O(1)",
        "hints": [
            "Find common prefix of binary representations of left and right."
        ],
        "starter_code": {
            "python": "def rangeBitwiseAnd(left: int, right: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function rangeBitwiseAnd(left, right) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int rangeBitwiseAnd(int left, int right) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int rangeBitwiseAnd(int left, int right) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "5\n7",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "5 & 6 & 7 = 4."
            },
            {
                "input_data": "0\n0",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "0 & 0 = 0."
            },
            {
                "input_data": "1\n2147483647",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Wide range results in 0."
            }
        ]
    },
    {
        "title": "Single Number II",
        "slug": "single-number-ii",
        "topic": "Bit Manipulation",
        "difficulty": "Medium",
        "description": "Given an integer array `nums` where every element appears three times except for one, which appears exactly once. Find the single element and return it in `O(n)` time and `O(1)` space.",
        "constraints": "1 <= nums.length <= 3 * 10^4\n-2^31 <= nums[i] <= 2^31 - 1\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Count bits modulo 3 across all 32 bit positions, or use digital logic state machine."
        ],
        "starter_code": {
            "python": "def singleNumber2(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function singleNumber2(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int singleNumber2(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int singleNumber2(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 2, 3, 2]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 appears once."
            },
            {
                "input_data": "[0, 1, 0, 1, 0, 1, 99]",
                "expected_output": "99",
                "is_sample": True,
                "explanation": "99 appears once."
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
        "title": "Single Number III",
        "slug": "single-number-iii",
        "topic": "Bit Manipulation",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once.",
        "constraints": "2 <= nums.length <= 3 * 10^4\n-2^31 <= nums[i] <= 2^31 - 1\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "XOR all numbers to get a ^ b; isolate lowest differing bit to partition into two groups."
        ],
        "starter_code": {
            "python": "def singleNumber3(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function singleNumber3(nums) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] singleNumber3(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> singleNumber3(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 1, 3, 2, 5]",
                "expected_output": "[3, 5]",
                "is_sample": True,
                "explanation": "3 and 5 appear once."
            },
            {
                "input_data": "[-1, 0]",
                "expected_output": "[-1, 0]",
                "is_sample": True,
                "explanation": "-1 and 0."
            },
            {
                "input_data": "[0, 1]",
                "expected_output": "[0, 1]",
                "is_sample": False,
                "explanation": "0 and 1."
            }
        ]
    },
    {
        "title": "Pow(x, n)",
        "slug": "powx-n",
        "topic": "Math",
        "difficulty": "Medium",
        "description": "Implement `pow(x, n)`, which calculates `x` raised to the power `n` (`x^n`) in `O(log n)` time.",
        "constraints": "-100.0 < x < 100.0\n-2^31 <= n <= 2^31 - 1\nOptimal Time: O(log n), Space: O(1) (Binary Exponentiation)",
        "hints": [
            "Binary exponentiation: square x when n is even; multiply and decrement when n is odd."
        ],
        "starter_code": {
            "python": "def myPow(x: float, n: int) -> float:\n    # Write your solution here\n    pass\n",
            "javascript": "function myPow(x, n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public double myPow(double x, int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    double myPow(double x, int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2.0\n10",
                "expected_output": "1024.0",
                "is_sample": True,
                "explanation": "2^10 = 1024.0."
            },
            {
                "input_data": "2.1\n3",
                "expected_output": "9.261",
                "is_sample": True,
                "explanation": "2.1^3 = 9.261."
            },
            {
                "input_data": "2.0\n-2",
                "expected_output": "0.25",
                "is_sample": False,
                "explanation": "2^-2 = 1/4 = 0.25."
            }
        ]
    },
    {
        "title": "Integer to Roman",
        "slug": "integer-to-roman",
        "topic": "Math",
        "difficulty": "Medium",
        "description": "Seven different symbols represent Roman numerals. Given an integer `num`, convert it to a Roman numeral.",
        "constraints": "1 <= num <= 3999\nOptimal Time: O(1), Space: O(1)",
        "hints": [
            "Greedily subtract largest Roman value symbol from values table."
        ],
        "starter_code": {
            "python": "def intToRoman(num: int) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function intToRoman(num) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String intToRoman(int num) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string intToRoman(int num) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "3749",
                "expected_output": "\"MMMDCCXLIX\"",
                "is_sample": True,
                "explanation": "3749 = MMMDCCXLIX."
            },
            {
                "input_data": "58",
                "expected_output": "\"LVIII\"",
                "is_sample": True,
                "explanation": "58 = LVIII."
            },
            {
                "input_data": "1994",
                "expected_output": "\"MCMXCIV\"",
                "is_sample": False,
                "explanation": "1994 = MCMXCIV."
            }
        ]
    },
    {
        "title": "Factorial Trailing Zeroes",
        "slug": "factorial-trailing-zeroes",
        "topic": "Math",
        "difficulty": "Medium",
        "description": "Given an integer `n`, return the number of trailing zeroes in `n!` in logarithmic time.",
        "constraints": "0 <= n <= 10^4\nOptimal Time: O(log5(n)), Space: O(1)",
        "hints": [
            "Count how many factors of 5 are in 1 * 2 * ... * n: n//5 + n//25 + n//125 + ..."
        ],
        "starter_code": {
            "python": "def trailingZeroes(n: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function trailingZeroes(n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int trailingZeroes(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int trailingZeroes(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "3",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "3! = 6 (0 zeroes)."
            },
            {
                "input_data": "5",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "5! = 120 (1 zero)."
            },
            {
                "input_data": "0",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "0! = 1."
            }
        ]
    },
    {
        "title": "Set Matrix Zeroes",
        "slug": "set-matrix-zeroes",
        "topic": "Matrix",
        "difficulty": "Medium",
        "description": "Given an `m x n` integer matrix `matrix`, if an element is 0, set its entire row and column to 0's. You must do it in place with `O(1)` auxiliary space.",
        "constraints": "1 <= m, n <= 200\nOptimal Time: O(m * n), Space: O(1)",
        "hints": [
            "Use first row and first column as markers."
        ],
        "starter_code": {
            "python": "def setZeroes(matrix: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function setZeroes(matrix) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public void setZeroes(int[][] matrix) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    void setZeroes(vector<vector<int>>& matrix) {\n        // Write your solution here\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 1, 1], [1, 0, 1], [1, 1, 1]]",
                "expected_output": "[[1, 0, 1], [0, 0, 0], [1, 0, 1]]",
                "is_sample": True,
                "explanation": "Row 1 and col 1 zeroed."
            },
            {
                "input_data": "[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]",
                "expected_output": "[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]",
                "is_sample": True,
                "explanation": "Rows and columns set to 0."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "No zeroes."
            }
        ]
    },
    {
        "title": "Spiral Matrix",
        "slug": "spiral-matrix",
        "topic": "Matrix",
        "difficulty": "Medium",
        "description": "Given an `m x n` `matrix`, return all elements of the `matrix` in spiral order.",
        "constraints": "1 <= m, n <= 10\nOptimal Time: O(m * n), Space: O(1)",
        "hints": [
            "Maintain four boundaries: top, bottom, left, right."
        ],
        "starter_code": {
            "python": "def spiralOrder(matrix: list[list[int]]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function spiralOrder(matrix) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> spiralOrder(int[][] matrix) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> spiralOrder(vector<vector<int>>& matrix) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                "expected_output": "[1, 2, 3, 6, 9, 8, 7, 4, 5]",
                "is_sample": True,
                "explanation": "Spiral traversal."
            },
            {
                "input_data": "[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]",
                "expected_output": "[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]",
                "is_sample": True,
                "explanation": "Spiral 3x4."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Single cell."
            }
        ]
    },
    {
        "title": "Rotate Image",
        "slug": "rotate-image",
        "topic": "Matrix",
        "difficulty": "Medium",
        "description": "You are given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees (clockwise) in-place.",
        "constraints": "n == matrix.length == matrix[i].length\n1 <= n <= 20\nOptimal Time: O(n^2), Space: O(1)",
        "hints": [
            "Transpose matrix, then reverse each row."
        ],
        "starter_code": {
            "python": "def rotateMatrix(matrix: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function rotateMatrix(matrix) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public void rotateMatrix(int[][] matrix) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    void rotateMatrix(vector<vector<int>>& matrix) {\n        // Write your solution here\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                "expected_output": "[[7, 4, 1], [8, 5, 2], [9, 6, 3]]",
                "is_sample": True,
                "explanation": "Rotated 90 degrees."
            },
            {
                "input_data": "[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]",
                "expected_output": "[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]",
                "is_sample": True,
                "explanation": "4x4 rotated."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "1x1 unchanged."
            }
        ]
    },
    {
        "title": "Search a 2D Matrix II",
        "slug": "search-a-2d-matrix-ii",
        "topic": "Matrix",
        "difficulty": "Medium",
        "description": "Write an efficient algorithm that searches for a value `target` in an `m x n` integer matrix where integers in each row are sorted left-to-right, and integers in each column are sorted top-to-bottom.",
        "constraints": "1 <= m, n <= 300\nOptimal Time: O(m + n), Space: O(1)",
        "hints": [
            "Start from top-right corner; move left if val > target, move down if val < target."
        ],
        "starter_code": {
            "python": "def searchMatrix2(matrix: list[list[int]], target: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function searchMatrix2(matrix, target) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean searchMatrix2(int[][] matrix, int target) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool searchMatrix2(vector<vector<int>>& matrix, int target) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]\n5",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "5 is found."
            },
            {
                "input_data": "[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]\n20",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "20 not in matrix."
            },
            {
                "input_data": "[[-5]]\n-5",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "-5 found."
            }
        ]
    },
    {
        "title": "Game of Life",
        "slug": "game-of-life",
        "topic": "Matrix",
        "difficulty": "Medium",
        "description": "According to Conway's Game of Life rules, compute the next state of the board in-place.",
        "constraints": "1 <= m, n <= 25\nboard[i][j] is 0 or 1\nOptimal Time: O(m * n), Space: O(1) in-place",
        "hints": [
            "Use bit transitions: 2 for (0->1) and -1 for (1->0)."
        ],
        "starter_code": {
            "python": "def gameOfLife(board: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function gameOfLife(board) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public void gameOfLife(int[][] board) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    void gameOfLife(vector<vector<int>>& board) {\n        // Write your solution here\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]",
                "expected_output": "[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]",
                "is_sample": True,
                "explanation": "Next state."
            },
            {
                "input_data": "[[1, 1], [1, 0]]",
                "expected_output": "[[1, 1], [1, 1]]",
                "is_sample": True,
                "explanation": "Next state."
            },
            {
                "input_data": "[[0]]",
                "expected_output": "[[0]]",
                "is_sample": False,
                "explanation": "Remains dead."
            }
        ]
    }
]
