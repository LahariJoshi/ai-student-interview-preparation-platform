"""
strings.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "topic": "String",
        "difficulty": "Easy",
        "description": "Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.",
        "constraints": "1 <= s.length, t.length <= 5 * 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Count frequency of each character in both strings."
        ],
        "starter_code": {
            "python": "def isAnagram(s: str, t: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isAnagram(s, t) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isAnagram(String s, String t) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"anagram\"\n\"nagaram\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Both contain same characters."
            },
            {
                "input_data": "\"rat\"\n\"car\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Not an anagram."
            },
            {
                "input_data": "\"a\"\n\"ab\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Different lengths."
            }
        ]
    },
    {
        "title": "Longest Common Prefix",
        "slug": "longest-common-prefix",
        "topic": "String",
        "difficulty": "Easy",
        "description": "Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string `\"\"`.",
        "constraints": "1 <= strs.length <= 200\n0 <= strs[i].length <= 200\nOptimal Time: O(S), Space: O(1)",
        "hints": [
            "Compare characters column by column across all strings."
        ],
        "starter_code": {
            "python": "def longestCommonPrefix(strs: list[str]) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function longestCommonPrefix(strs) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String longestCommonPrefix(String[] strs) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string longestCommonPrefix(vector<string>& strs) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"flower\", \"flow\", \"flight\"]",
                "expected_output": "\"fl\"",
                "is_sample": True,
                "explanation": "\"fl\" is common to all."
            },
            {
                "input_data": "[\"dog\", \"racecar\", \"car\"]",
                "expected_output": "\"\"",
                "is_sample": True,
                "explanation": "No common prefix."
            },
            {
                "input_data": "[\"a\"]",
                "expected_output": "\"a\"",
                "is_sample": False,
                "explanation": "Single string."
            }
        ]
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.",
        "constraints": "1 <= s.length <= 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Push opening brackets to a stack, and pop when closing bracket matches."
        ],
        "starter_code": {
            "python": "def isValid(s: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isValid(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isValid(String s) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isValid(string s) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"()\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Balanced."
            },
            {
                "input_data": "\"()[]{}\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "All valid."
            },
            {
                "input_data": "\"(]\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Mismatched type."
            },
            {
                "input_data": "\"([)]\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Incorrect nesting."
            }
        ]
    },
    {
        "title": "Roman to Integer",
        "slug": "roman-to-integer",
        "topic": "Math",
        "difficulty": "Easy",
        "description": "Given a roman numeral `s`, convert it to an integer.",
        "constraints": "1 <= s.length <= 15\ns contains only valid Roman numerals: ('I', 'V', 'X', 'L', 'C', 'D', 'M').\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "If smaller numeral precedes larger numeral, subtract it; otherwise add it."
        ],
        "starter_code": {
            "python": "def romanToInt(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function romanToInt(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int romanToInt(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int romanToInt(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"III\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "III = 3."
            },
            {
                "input_data": "\"LVIII\"",
                "expected_output": "58",
                "is_sample": True,
                "explanation": "L = 50, V= 5, III = 3."
            },
            {
                "input_data": "\"MCMXCIV\"",
                "expected_output": "1994",
                "is_sample": False,
                "explanation": "M = 1000, CM = 900, XC = 90 and IV = 4."
            }
        ]
    },
    {
        "title": "First Unique Character in a String",
        "slug": "first-unique-character-in-a-string",
        "topic": "String",
        "difficulty": "Easy",
        "description": "Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return `-1`.",
        "constraints": "1 <= s.length <= 10^5\ns consists of only lowercase English letters.\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Build a count map of all characters, then find first character with count 1."
        ],
        "starter_code": {
            "python": "def firstUniqChar(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function firstUniqChar(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int firstUniqChar(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int firstUniqChar(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"leetcode\"",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "'l' at index 0 is first unique."
            },
            {
                "input_data": "\"loveleetcode\"",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "'v' at index 2 is first unique."
            },
            {
                "input_data": "\"aabb\"",
                "expected_output": "-1",
                "is_sample": False,
                "explanation": "No unique character."
            }
        ]
    },
    {
        "title": "Reverse String",
        "slug": "reverse-string",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Write a function that reverses a string. The input string is given as an array of characters `s`. You must do this by modifying the input array in-place.",
        "constraints": "1 <= s.length <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use two pointers swapping characters from ends inward."
        ],
        "starter_code": {
            "python": "def reverseString(s: list[str]) -> list[str]:\n    # Write your solution here\n    pass\n",
            "javascript": "function reverseString(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public void reverseString(char[] s) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    void reverseString(vector<char>& s) {\n        // Write your solution here\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"h\", \"e\", \"l\", \"l\", \"o\"]",
                "expected_output": "[\"o\", \"l\", \"l\", \"e\", \"h\"]",
                "is_sample": True,
                "explanation": "Reversed array."
            },
            {
                "input_data": "[\"H\", \"a\", \"n\", \"n\", \"a\", \"h\"]",
                "expected_output": "[\"h\", \"a\", \"n\", \"n\", \"a\", \"H\"]",
                "is_sample": True,
                "explanation": "Reversed."
            },
            {
                "input_data": "[\"a\"]",
                "expected_output": "[\"a\"]",
                "is_sample": False,
                "explanation": "Single char."
            }
        ]
    },
    {
        "title": "Ransom Note",
        "slug": "ransom-note",
        "topic": "Hash Table",
        "difficulty": "Easy",
        "description": "Given two strings `ransomNote` and `magazine`, return `True` if `ransomNote` can be constructed by using the letters from `magazine` and `False` otherwise.",
        "constraints": "1 <= ransomNote.length, magazine.length <= 10^5\nOptimal Time: O(m + n), Space: O(1)",
        "hints": [
            "Count letters in magazine and decrement for each letter in ransomNote."
        ],
        "starter_code": {
            "python": "def canConstruct(ransomNote: str, magazine: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function canConstruct(ransomNote, magazine) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean canConstruct(String ransomNote, String magazine) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool canConstruct(string ransomNote, string magazine) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"a\"\n\"b\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "'a' not in 'b'."
            },
            {
                "input_data": "\"aa\"\n\"ab\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Not enough 'a's."
            },
            {
                "input_data": "\"aa\"\n\"aab\"",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Can construct."
            }
        ]
    },
    {
        "title": "Is Subsequence",
        "slug": "is-subsequence",
        "topic": "Two Pointers",
        "difficulty": "Easy",
        "description": "Given two strings `s` and `t`, return `True` if `s` is a subsequence of `t`, or `False` otherwise.",
        "constraints": "0 <= s.length <= 100\n0 <= t.length <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use two pointers moving through both strings."
        ],
        "starter_code": {
            "python": "def isSubsequence(s: str, t: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isSubsequence(s, t) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isSubsequence(String s, String t) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isSubsequence(string s, string t) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"abc\"\n\"ahbgdc\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "'a', 'b', 'c' appear in order."
            },
            {
                "input_data": "\"axc\"\n\"ahbgdc\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "'x' not found."
            },
            {
                "input_data": "\"\"\n\"ahbgdc\"",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Empty string is always subsequence."
            }
        ]
    },
    {
        "title": "Length of Last Word",
        "slug": "length-of-last-word",
        "topic": "String",
        "difficulty": "Easy",
        "description": "Given a string `s` consisting of words and spaces, return the length of the last word in the string.",
        "constraints": "1 <= s.length <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Scan backwards from the end, skipping trailing spaces."
        ],
        "starter_code": {
            "python": "def lengthOfLastWord(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function lengthOfLastWord(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int lengthOfLastWord(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int lengthOfLastWord(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"Hello World\"",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "\"World\" length 5."
            },
            {
                "input_data": "\"   fly me   to   the moon  \"",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "\"moon\" length 4."
            },
            {
                "input_data": "\"luffy is still joyboy\"",
                "expected_output": "6",
                "is_sample": False,
                "explanation": "\"joyboy\" length 6."
            }
        ]
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "topic": "Hash Table",
        "difficulty": "Medium",
        "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        "constraints": "1 <= strs.length <= 10^4\n0 <= strs[i].length <= 100\nOptimal Time: O(n * k log k), Space: O(n * k)",
        "hints": [
            "Sort each string as key in hash map or use 26-element character count tuple."
        ],
        "starter_code": {
            "python": "def groupAnagrams(strs: list[str]) -> list[list[str]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function groupAnagrams(strs) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<String>> groupAnagrams(String[] strs) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<string>> groupAnagrams(vector<string>& strs) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]",
                "expected_output": "[[\"bat\"], [\"nat\", \"tan\"], [\"ate\", \"eat\", \"tea\"]]",
                "is_sample": True,
                "explanation": "Grouped anagrams."
            },
            {
                "input_data": "[\"\"]",
                "expected_output": "[[\"\"]]",
                "is_sample": True,
                "explanation": "Empty string."
            },
            {
                "input_data": "[\"a\"]",
                "expected_output": "[[\"a\"]]",
                "is_sample": False,
                "explanation": "Single item."
            }
        ]
    },
    {
        "title": "Longest Palindromic Substring",
        "slug": "longest-palindromic-substring",
        "topic": "String",
        "difficulty": "Medium",
        "description": "Given a string `s`, return the longest palindromic substring in `s`.",
        "constraints": "1 <= s.length <= 1000\nOptimal Time: O(n^2), Space: O(1)",
        "hints": [
            "Expand around center for each index (both odd and even centers)."
        ],
        "starter_code": {
            "python": "def longestPalindrome(s: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function longestPalindrome(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String longestPalindrome(String s) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string longestPalindrome(string s) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"babad\"",
                "expected_output": "\"bab\"",
                "is_sample": True,
                "explanation": "\"bab\" (or \"aba\") is a valid answer."
            },
            {
                "input_data": "\"cbbd\"",
                "expected_output": "\"bb\"",
                "is_sample": True,
                "explanation": "\"bb\" is longest palindrome."
            },
            {
                "input_data": "\"a\"",
                "expected_output": "\"a\"",
                "is_sample": False,
                "explanation": "Single char."
            }
        ]
    },
    {
        "title": "String to Integer (atoi)",
        "slug": "string-to-integer-atoi",
        "topic": "String",
        "difficulty": "Medium",
        "description": "Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer (similar to C/C++'s `atoi` function). Clamp to `[-2^31, 2^31 - 1]`.",
        "constraints": "0 <= s.length <= 200\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Trim leading whitespaces, parse sign, convert digits and check clamping."
        ],
        "starter_code": {
            "python": "def myAtoi(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function myAtoi(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int myAtoi(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int myAtoi(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"42\"",
                "expected_output": "42",
                "is_sample": True,
                "explanation": "Integer 42."
            },
            {
                "input_data": "\" -042\"",
                "expected_output": "-42",
                "is_sample": True,
                "explanation": "Negative 42."
            },
            {
                "input_data": "\"1337c0d3\"",
                "expected_output": "1337",
                "is_sample": False,
                "explanation": "Stops at non-digit."
            },
            {
                "input_data": "\"0-1\"",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Zero parsed."
            }
        ]
    },
    {
        "title": "Multiply Strings",
        "slug": "multiply-strings",
        "topic": "Math",
        "difficulty": "Medium",
        "description": "Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.",
        "constraints": "1 <= num1.length, num2.length <= 200\nnum1 and num2 consist of digits only.\nOptimal Time: O(m * n), Space: O(m + n)",
        "hints": [
            "Position i of num1 and j of num2 affects positions i+j and i+j+1 in output."
        ],
        "starter_code": {
            "python": "def multiply(num1: str, num2: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function multiply(num1, num2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String multiply(String num1, String num2) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string multiply(string num1, string num2) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"2\"\n\"3\"",
                "expected_output": "\"6\"",
                "is_sample": True,
                "explanation": "2 * 3 = 6."
            },
            {
                "input_data": "\"123\"\n\"456\"",
                "expected_output": "\"56088\"",
                "is_sample": True,
                "explanation": "123 * 456 = 56088."
            },
            {
                "input_data": "\"0\"\n\"52\"",
                "expected_output": "\"0\"",
                "is_sample": False,
                "explanation": "Multiply by 0."
            }
        ]
    },
    {
        "title": "Generate Parentheses",
        "slug": "generate-parentheses",
        "topic": "Backtracking",
        "difficulty": "Medium",
        "description": "Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
        "constraints": "1 <= n <= 8\nOptimal Time: O(4^n / sqrt(n)), Space: O(n)",
        "hints": [
            "Backtrack with open < n and close < open constraints."
        ],
        "starter_code": {
            "python": "def generateParenthesis(n: int) -> list[str]:\n    # Write your solution here\n    pass\n",
            "javascript": "function generateParenthesis(n) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<String> generateParenthesis(int n) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<string> generateParenthesis(int n) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "3",
                "expected_output": "[\"((()))\", \"(()())\", \"(())()\", \"()(())\", \"()()()\"]",
                "is_sample": True,
                "explanation": "5 valid combinations."
            },
            {
                "input_data": "1",
                "expected_output": "[\"()\"]",
                "is_sample": True,
                "explanation": "Single pair."
            },
            {
                "input_data": "2",
                "expected_output": "[\"(())\", \"()()\"]",
                "is_sample": False,
                "explanation": "Two pairs."
            }
        ]
    },
    {
        "title": "Palindromic Substrings",
        "slug": "palindromic-substrings",
        "topic": "String",
        "difficulty": "Medium",
        "description": "Given a string `s`, return the number of palindromic substrings in it.",
        "constraints": "1 <= s.length <= 1000\nOptimal Time: O(n^2), Space: O(1)",
        "hints": [
            "Expand outward from each index (both odd and even length centers) and count."
        ],
        "starter_code": {
            "python": "def countSubstrings(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function countSubstrings(s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int countSubstrings(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int countSubstrings(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"abc\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "\"a\", \"b\", \"c\"."
            },
            {
                "input_data": "\"aaa\"",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "\"a\", \"a\", \"a\", \"aa\", \"aa\", \"aaa\"."
            },
            {
                "input_data": "\"a\"",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single char."
            }
        ]
    },
    {
        "title": "Simplify Path",
        "slug": "simplify-path",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Given an absolute path for a Unix-style file system, convert it to the simplified canonical path.",
        "constraints": "1 <= path.length <= 3000\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Split by '/' and use a stack. Pop for '..', ignore '.' and empty segments."
        ],
        "starter_code": {
            "python": "def simplifyPath(path: str) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function simplifyPath(path) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String simplifyPath(String path) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string simplifyPath(string path) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"/home/\"",
                "expected_output": "\"/home\"",
                "is_sample": True,
                "explanation": "Trailing slash removed."
            },
            {
                "input_data": "\"/home//foo/\"",
                "expected_output": "\"/home/foo\"",
                "is_sample": True,
                "explanation": "Multiple consecutive slashes replaced."
            },
            {
                "input_data": "\"/home/user/Documents/../Pictures\"",
                "expected_output": "\"/home/user/Pictures\"",
                "is_sample": False,
                "explanation": "'..' moves up one level."
            }
        ]
    },
    {
        "title": "Regular Expression Matching",
        "slug": "regular-expression-matching",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Given an input string `s` and a pattern `p`, implement regular expression matching with support for `'.'` (matches any single character) and `'*'` (matches zero or more of preceding element).",
        "constraints": "1 <= s.length <= 20\n1 <= p.length <= 20\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "2D dynamic programming dp[i][j] representing if s[:i] matches p[:j]."
        ],
        "starter_code": {
            "python": "def isMatch(s: str, p: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isMatch(s, p) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isMatch(String s, String p) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isMatch(string s, string p) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"aa\"\n\"a\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "'a' does not match the entire string \"aa\"."
            },
            {
                "input_data": "\"aa\"\n\"a*\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "'*' matches zero or more of 'a'."
            },
            {
                "input_data": "\"ab\"\n\".*\"",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "\".*\" matches any sequence."
            }
        ]
    },
    {
        "title": "Wildcard Matching",
        "slug": "wildcard-matching",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Given an input string `s` and a pattern `p`, implement wildcard pattern matching with support for `'?'` (matches any single character) and `'*'` (matches any sequence of characters including empty).",
        "constraints": "0 <= s.length, p.length <= 2000\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "Use dynamic programming or greedy two pointers."
        ],
        "starter_code": {
            "python": "def isMatch(s: str, p: str) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isMatch(s, p) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isMatch(String s, String p) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isMatch(string s, string p) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"aa\"\n\"a\"",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Does not match entire string."
            },
            {
                "input_data": "\"aa\"\n\"*\"",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "'*' matches any sequence."
            },
            {
                "input_data": "\"cb\"\n\"?a\"",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "'?' matches 'c', but 'b' != 'a'."
            }
        ]
    },
    {
        "title": "Edit Distance",
        "slug": "edit-distance",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2` (insert, delete, or replace).",
        "constraints": "0 <= word1.length, word2.length <= 500\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "2D DP table: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])."
        ],
        "starter_code": {
            "python": "def minDistance(word1: str, word2: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function minDistance(word1, word2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int minDistance(String word1, String word2) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int minDistance(string word1, string word2) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"horse\"\n\"ros\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "horse -> rorse -> rose -> ros (3 ops)."
            },
            {
                "input_data": "\"intention\"\n\"execution\"",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "5 operations required."
            },
            {
                "input_data": "\"\"\n\"a\"",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Insert 'a'."
            }
        ]
    },
    {
        "title": "Distinct Subsequences",
        "slug": "distinct-subsequences",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.",
        "constraints": "1 <= s.length, t.length <= 1000\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "If s[i-1] == t[j-1], dp[i][j] = dp[i-1][j-1] + dp[i-1][j]."
        ],
        "starter_code": {
            "python": "def numDistinct(s: str, t: str) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function numDistinct(s, t) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int numDistinct(String s, String t) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int numDistinct(string s, string t) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"rabbbit\"\n\"rabbit\"",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Three ways to pick 'b's."
            },
            {
                "input_data": "\"babgbag\"\n\"bag\"",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "5 subsequences equal 'bag'."
            },
            {
                "input_data": "\"a\"\n\"b\"",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "No match."
            }
        ]
    }
]
