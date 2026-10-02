"""
linked_lists.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Given the `head` of a singly linked list (represented as an array of values), reverse the list, and return the reversed list.",
        "constraints": "0 <= number of nodes <= 5000\n-5000 <= Node.val <= 5000\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Iterate through the list, re-pointing current.next to previous node."
        ],
        "starter_code": {
            "python": "def reverseList(head: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function reverseList(head) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] reverseList(int[] head) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> reverseList(vector<int>& head) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]",
                "expected_output": "[5, 4, 3, 2, 1]",
                "is_sample": True,
                "explanation": "Reversed list."
            },
            {
                "input_data": "[1, 2]",
                "expected_output": "[2, 1]",
                "is_sample": True,
                "explanation": "Reversed two elements."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty list reversed is empty."
            }
        ]
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list.",
        "constraints": "0 <= list1.length, list2.length <= 50\n-100 <= Node.val <= 100\nOptimal Time: O(n + m), Space: O(1)",
        "hints": [
            "Compare heads of both lists and advance pointer of smaller element."
        ],
        "starter_code": {
            "python": "def mergeTwoLists(list1: list[int], list2: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function mergeTwoLists(list1, list2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] mergeTwoLists(int[] list1, int[] list2) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> mergeTwoLists(vector<int>& list1, vector<int>& list2) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 4]\n[1, 3, 4]",
                "expected_output": "[1, 1, 2, 3, 4, 4]",
                "is_sample": True,
                "explanation": "Merged sorted list."
            },
            {
                "input_data": "[]\n[]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Both empty."
            },
            {
                "input_data": "[]\n[0]",
                "expected_output": "[0]",
                "is_sample": False,
                "explanation": "One empty list."
            }
        ]
    },
    {
        "title": "Linked List Cycle",
        "slug": "linked-list-cycle",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Given `head`, the head of a linked list, determine if the linked list has a cycle in it (pos is -1 if no cycle).",
        "constraints": "0 <= number of nodes <= 10^4\nOptimal Time: O(n), Space: O(1) (Floyd's Tortoise and Hare)",
        "hints": [
            "Use two pointers: slow moves by 1, fast moves by 2. If they meet, there is a cycle."
        ],
        "starter_code": {
            "python": "def hasCycle(head: list[int], pos: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function hasCycle(head, pos) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean hasCycle(int[] head, int pos) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool hasCycle(vector<int>& head, int pos) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 2, 0, -4]\n1",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Cycle exists pointing back to index 1."
            },
            {
                "input_data": "[1, 2]\n0",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Cycle exists pointing back to 0."
            },
            {
                "input_data": "[1]\n-1",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "No cycle."
            }
        ]
    },
    {
        "title": "Palindrome Linked List",
        "slug": "palindrome-linked-list",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Given the `head` of a singly linked list, return `True` if it is a palindrome or `False` otherwise.",
        "constraints": "1 <= number of nodes <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Find the middle node, reverse the second half, and compare with the first half."
        ],
        "starter_code": {
            "python": "def isPalindromeList(head: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isPalindromeList(head) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isPalindromeList(int[] head) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isPalindromeList(vector<int>& head) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 2, 1]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Is palindrome."
            },
            {
                "input_data": "[1, 2]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Not a palindrome."
            },
            {
                "input_data": "[1]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Single item is palindrome."
            }
        ]
    },
    {
        "title": "Remove Linked List Elements",
        "slug": "remove-linked-list-elements",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Given the `head` of a linked list and an integer `val`, remove all nodes of the linked list that have `Node.val == val`, and return the new head.",
        "constraints": "0 <= number of nodes <= 10^4\n1 <= Node.val <= 50\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use a dummy sentinel head node to handle deletion of the head node seamlessly."
        ],
        "starter_code": {
            "python": "def removeElements(head: list[int], val: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function removeElements(head, val) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] removeElements(int[] head, int val) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> removeElements(vector<int>& head, int val) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 6, 3, 4, 5, 6]\n6",
                "expected_output": "[1, 2, 3, 4, 5]",
                "is_sample": True,
                "explanation": "Removed all 6s."
            },
            {
                "input_data": "[]\n1",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty list."
            },
            {
                "input_data": "[7, 7, 7, 7]\n7",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "All elements removed."
            }
        ]
    },
    {
        "title": "Middle of the Linked List",
        "slug": "middle-of-the-linked-list",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Given the `head` of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.",
        "constraints": "1 <= number of nodes <= 100\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Fast and slow pointer: fast advances by 2 steps, slow advances by 1."
        ],
        "starter_code": {
            "python": "def middleNode(head: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function middleNode(head) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] middleNode(int[] head) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> middleNode(vector<int>& head) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]",
                "expected_output": "[3, 4, 5]",
                "is_sample": True,
                "explanation": "Middle node is 3."
            },
            {
                "input_data": "[1, 2, 3, 4, 5, 6]",
                "expected_output": "[4, 5, 6]",
                "is_sample": True,
                "explanation": "Second middle node is 4."
            },
            {
                "input_data": "[1]",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Single item."
            }
        ]
    },
    {
        "title": "Add Two Numbers",
        "slug": "add-two-numbers",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
        "constraints": "1 <= l1.length, l2.length <= 100\n0 <= Node.val <= 9\nOptimal Time: O(max(m, n)), Space: O(max(m, n))",
        "hints": [
            "Simulate column addition with a carry variable."
        ],
        "starter_code": {
            "python": "def addTwoNumbers(l1: list[int], l2: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function addTwoNumbers(l1, l2) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] addTwoNumbers(int[] l1, int[] l2) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> addTwoNumbers(vector<int>& l1, vector<int>& l2) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 4, 3]\n[5, 6, 4]",
                "expected_output": "[7, 0, 8]",
                "is_sample": True,
                "explanation": "342 + 465 = 807."
            },
            {
                "input_data": "[0]\n[0]",
                "expected_output": "[0]",
                "is_sample": True,
                "explanation": "0 + 0 = 0."
            },
            {
                "input_data": "[9, 9, 9, 9, 9, 9, 9]\n[9, 9, 9, 9]",
                "expected_output": "[8, 9, 9, 9, 0, 0, 0, 1]",
                "is_sample": False,
                "explanation": "Addition with carries."
            }
        ]
    },
    {
        "title": "Remove Nth Node From End of List",
        "slug": "remove-nth-node-from-end-of-list",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Given the `head` of a linked list, remove the `n-th` node from the end of the list and return its head.",
        "constraints": "1 <= sz <= 30\n0 <= Node.val <= 100\n1 <= n <= sz\nOptimal Time: O(sz), Space: O(1)",
        "hints": [
            "Maintain two pointers spaced n nodes apart."
        ],
        "starter_code": {
            "python": "def removeNthFromEnd(head: list[int], n: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function removeNthFromEnd(head, n) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] removeNthFromEnd(int[] head, int n) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> removeNthFromEnd(vector<int>& head, int n) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]\n2",
                "expected_output": "[1, 2, 3, 5]",
                "is_sample": True,
                "explanation": "Removed 4."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty list."
            },
            {
                "input_data": "[1, 2]\n1",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Removed tail node."
            }
        ]
    },
    {
        "title": "Reorder List",
        "slug": "reorder-list",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "You are given the head of a singly linked-list: L0 -> L1 -> ... -> Ln - 1 -> Ln. Reorder the list to be on the following form: L0 -> Ln -> L1 -> Ln - 1 -> L2 -> Ln - 2 -> ...",
        "constraints": "1 <= number of nodes <= 5 * 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Split in half, reverse second half, and merge alternately."
        ],
        "starter_code": {
            "python": "def reorderList(head: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function reorderList(head) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] reorderList(int[] head) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> reorderList(vector<int>& head) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4]",
                "expected_output": "[1, 4, 2, 3]",
                "is_sample": True,
                "explanation": "Reordered list."
            },
            {
                "input_data": "[1, 2, 3, 4, 5]",
                "expected_output": "[1, 5, 2, 4, 3]",
                "is_sample": True,
                "explanation": "Reordered list."
            },
            {
                "input_data": "[1]",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Single item."
            }
        ]
    },
    {
        "title": "Swap Nodes in Pairs",
        "slug": "swap-nodes-in-pairs",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes.",
        "constraints": "0 <= number of nodes <= 100\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Use dummy node and re-link pointers."
        ],
        "starter_code": {
            "python": "def swapPairs(head: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function swapPairs(head) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] swapPairs(int[] head) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> swapPairs(vector<int>& head) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4]",
                "expected_output": "[2, 1, 4, 3]",
                "is_sample": True,
                "explanation": "Adjacent nodes swapped."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty list."
            },
            {
                "input_data": "[1]",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Single element."
            }
        ]
    },
    {
        "title": "Rotate List",
        "slug": "rotate-list",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Given the head of a linked list, rotate the list to the right by `k` places.",
        "constraints": "0 <= number of nodes <= 500\n0 <= k <= 2 * 10^9\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Connect tail to head into a ring, then break at length - (k % length)."
        ],
        "starter_code": {
            "python": "def rotateRight(head: list[int], k: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function rotateRight(head, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] rotateRight(int[] head, int k) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> rotateRight(vector<int>& head, int k) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]\n2",
                "expected_output": "[4, 5, 1, 2, 3]",
                "is_sample": True,
                "explanation": "Rotated 2 places."
            },
            {
                "input_data": "[0, 1, 2]\n4",
                "expected_output": "[2, 0, 1]",
                "is_sample": True,
                "explanation": "Rotated 4 places (4 % 3 = 1)."
            },
            {
                "input_data": "[]\n0",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty list."
            }
        ]
    },
    {
        "title": "Odd Even Linked List",
        "slug": "odd-even-linked-list",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Given the `head` of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.",
        "constraints": "0 <= number of nodes <= 10^4\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Maintain odd and even pointers and weave them together."
        ],
        "starter_code": {
            "python": "def oddEvenList(head: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function oddEvenList(head) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] oddEvenList(int[] head) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> oddEvenList(vector<int>& head) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]",
                "expected_output": "[1, 3, 5, 2, 4]",
                "is_sample": True,
                "explanation": "Odds [1, 3, 5] then evens [2, 4]."
            },
            {
                "input_data": "[2, 1, 3, 5, 6, 4, 7]",
                "expected_output": "[2, 3, 6, 7, 1, 5, 4]",
                "is_sample": True,
                "explanation": "Odds then evens."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty."
            }
        ]
    },
    {
        "title": "Partition List",
        "slug": "partition-list",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Given the `head` of a linked list and a value `x`, partition it such that all nodes less than `x` come before nodes greater than or equal to `x`, preserving relative order.",
        "constraints": "0 <= number of nodes <= 200\n-100 <= Node.val <= 100\n-200 <= x <= 200\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Maintain two separate chains: before_x and after_x."
        ],
        "starter_code": {
            "python": "def partition(head: list[int], x: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function partition(head, x) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] partition(int[] head, int x) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> partition(vector<int>& head, int x) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 4, 3, 2, 5, 2]\n3",
                "expected_output": "[1, 2, 2, 4, 3, 5]",
                "is_sample": True,
                "explanation": "Values < 3 placed first."
            },
            {
                "input_data": "[2, 1]\n2",
                "expected_output": "[1, 2]",
                "is_sample": True,
                "explanation": "1 < 2."
            },
            {
                "input_data": "[]\n0",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty list."
            }
        ]
    },
    {
        "title": "Merge k Sorted Lists",
        "slug": "merge-k-sorted-lists",
        "topic": "Linked List",
        "difficulty": "Hard",
        "description": "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.",
        "constraints": "k == lists.length\n0 <= k <= 10^4\n0 <= lists[i].length <= 500\nOptimal Time: O(N log k), Space: O(k)",
        "hints": [
            "Use a min-heap to keep track of the current smallest element among all k lists."
        ],
        "starter_code": {
            "python": "def mergeKLists(lists: list[list[int]]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function mergeKLists(lists) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] mergeKLists(int[][] lists) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> mergeKLists(vector<vector<int>>& lists) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 4, 5], [1, 3, 4], [2, 6]]",
                "expected_output": "[1, 1, 2, 3, 4, 4, 5, 6]",
                "is_sample": True,
                "explanation": "Merged all 3 lists."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty list of lists."
            },
            {
                "input_data": "[[]]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Single empty list."
            }
        ]
    },
    {
        "title": "Reverse Nodes in k-Group",
        "slug": "reverse-nodes-in-k-group",
        "topic": "Linked List",
        "difficulty": "Hard",
        "description": "Given the `head` of a linked list, reverse the nodes of the list `k` at a time, and return the modified list. If the number of nodes is not a multiple of `k` then left-out nodes in the end should remain as it is.",
        "constraints": "1 <= k <= sz <= 5000\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Check if k nodes exist first; if so, reverse that chunk."
        ],
        "starter_code": {
            "python": "def reverseKGroup(head: list[int], k: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function reverseKGroup(head, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] reverseKGroup(int[] head, int k) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> reverseKGroup(vector<int>& head, int k) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]\n2",
                "expected_output": "[2, 1, 4, 3, 5]",
                "is_sample": True,
                "explanation": "Reversed in groups of 2."
            },
            {
                "input_data": "[1, 2, 3, 4, 5]\n3",
                "expected_output": "[3, 2, 1, 4, 5]",
                "is_sample": True,
                "explanation": "Reversed first 3; remaining 2 unchanged."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "k=1 unchanged."
            }
        ]
    },
    {
        "title": "LRU Cache",
        "slug": "lru-cache",
        "topic": "Linked List",
        "difficulty": "Hard",
        "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.",
        "constraints": "1 <= capacity <= 3000\nAt most 2 * 10^5 calls\nOptimal Time: O(1) for get and put, Space: O(capacity)",
        "hints": [
            "Hash map combined with doubly linked list."
        ],
        "starter_code": {
            "python": "    def __init__(self, capacity: int):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"LRUCache\", \"put\", \"put\", \"get\", \"put\", \"get\", \"put\", \"get\", \"get\", \"get\"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]",
                "expected_output": "[None, None, None, 1, None, -1, None, -1, 3, 4]",
                "is_sample": True,
                "explanation": "Standard LRU behavior."
            },
            {
                "input_data": "[\"LRUCache\", \"get\"]\n[[1], [10]]",
                "expected_output": "[None, -1]",
                "is_sample": True,
                "explanation": "Key not found."
            },
            {
                "input_data": "[\"LRUCache\", \"put\", \"get\"]\n[[1], [2, 1], [2]]",
                "expected_output": "[None, None, 1]",
                "is_sample": False,
                "explanation": "Put and get."
            }
        ]
    }
]
