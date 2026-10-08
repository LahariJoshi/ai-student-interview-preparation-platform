"""
trees.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Maximum Depth of Binary Tree",
        "slug": "maximum-depth-of-binary-tree",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the `root` of a binary tree (represented as level-order array with `None` for missing nodes), return its maximum depth.",
        "constraints": "0 <= number of nodes <= 10^4\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Depth = 1 + max(depth(left), depth(right))."
        ],
        "starter_code": {
            "python": "def maxDepth(root: list) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxDepth(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxDepth(Integer[] root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxDepth(vector<int>& root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 9, 20, None, None, 15, 7]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Depth is 3."
            },
            {
                "input_data": "[1, None, 2]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Depth is 2."
            },
            {
                "input_data": "[]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Empty tree depth 0."
            }
        ]
    },
    {
        "title": "Invert Binary Tree",
        "slug": "invert-binary-tree",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the `root` of a binary tree, invert the tree, and return its root.",
        "constraints": "0 <= number of nodes <= 100\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Swap left and right children recursively."
        ],
        "starter_code": {
            "python": "def invertTree(root: list) -> list:\n    # Write your solution here\n    pass\n",
            "javascript": "function invertTree(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public Integer[] invertTree(Integer[] root) {\n        // Write your solution here\n        return None;\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> invertTree(vector<int>& root) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[4, 2, 7, 1, 3, 6, 9]",
                "expected_output": "[4, 7, 2, 9, 6, 3, 1]",
                "is_sample": True,
                "explanation": "Inverted tree."
            },
            {
                "input_data": "[2, 1, 3]",
                "expected_output": "[2, 3, 1]",
                "is_sample": True,
                "explanation": "Inverted tree."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty tree."
            }
        ]
    },
    {
        "title": "Same Tree",
        "slug": "same-tree",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.",
        "constraints": "0 <= number of nodes <= 100\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Compare root values, then recurse on left and right subtrees."
        ],
        "starter_code": {
            "python": "def isSameTree(p: list, q: list) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isSameTree(p, q) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isSameTree(Integer[] p, Integer[] q) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isSameTree(vector<int>& p, vector<int>& q) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]\n[1, 2, 3]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Both trees are identical."
            },
            {
                "input_data": "[1, 2]\n[1, None, 2]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Different structures."
            },
            {
                "input_data": "[]\n[]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Both empty."
            }
        ]
    },
    {
        "title": "Symmetric Tree",
        "slug": "symmetric-tree",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the `root` of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).",
        "constraints": "1 <= number of nodes <= 1000\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "A tree is symmetric if left subtree is mirror reflection of right subtree."
        ],
        "starter_code": {
            "python": "def isSymmetric(root: list) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isSymmetric(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isSymmetric(Integer[] root) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isSymmetric(vector<int>& root) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 2, 3, 4, 4, 3]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Symmetric tree."
            },
            {
                "input_data": "[1, 2, 2, None, 3, None, 3]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Asymmetric."
            },
            {
                "input_data": "[1]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Single node."
            }
        ]
    },
    {
        "title": "Subtree of Another Tree",
        "slug": "subtree-of-another-tree",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the roots of two binary trees `root` and `subRoot`, return `True` if there is a subtree of `root` with the same structure and node values of `subRoot` and `False` otherwise.",
        "constraints": "1 <= root.length <= 2000\n1 <= subRoot.length <= 1000\nOptimal Time: O(m * n), Space: O(h)",
        "hints": [
            "Check if sameTree(root, subRoot) or recurse on left and right children."
        ],
        "starter_code": {
            "python": "def isSubtree(root: list, subRoot: list) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isSubtree(root, subRoot) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isSubtree(Integer[] root, Integer[] subRoot) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isSubtree(vector<int>& root, vector<int>& subRoot) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 4, 5, 1, 2]\n[4, 1, 2]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Is subtree."
            },
            {
                "input_data": "[3, 4, 5, 1, 2, None, None, None, None, 0]\n[4, 1, 2]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Not exact match."
            },
            {
                "input_data": "[1, 1]\n[1]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Subtree found."
            }
        ]
    },
    {
        "title": "Lowest Common Ancestor of a BST",
        "slug": "lowest-common-ancestor-of-a-bst",
        "topic": "BST",
        "difficulty": "Easy",
        "description": "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes `p` and `q`.",
        "constraints": "2 <= nodes <= 10^5\nOptimal Time: O(h), Space: O(1)",
        "hints": [
            "If both p and q are greater than root, go right; if both smaller, go left; otherwise root is LCA."
        ],
        "starter_code": {
            "python": "def lowestCommonAncestorBST(root_val: int, p: int, q: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function lowestCommonAncestorBST(root_val, p, q) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int lowestCommonAncestorBST(int root_val, int p, int q) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int lowestCommonAncestorBST(int root_val, int p, int q) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "6\n2\n8",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "LCA of 2 and 8 in tree with root 6 is 6."
            },
            {
                "input_data": "6\n2\n4",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "LCA in tree."
            },
            {
                "input_data": "2\n1\n2",
                "expected_output": "2",
                "is_sample": False,
                "explanation": "LCA of 1 and 2 is 2."
            }
        ]
    },
    {
        "title": "Diameter of Binary Tree",
        "slug": "diameter-of-binary-tree",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the `root` of a binary tree, return the length of the diameter of the tree (longest path between any two nodes).",
        "constraints": "1 <= number of nodes <= 10^4\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "At each node, diameter through this node = depth(left) + depth(right)."
        ],
        "starter_code": {
            "python": "def diameterOfBinaryTree(root: list) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function diameterOfBinaryTree(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int diameterOfBinaryTree(Integer[] root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int diameterOfBinaryTree(vector<int>& root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Length 3 path: [4, 2, 1, 3] or [5, 2, 1, 3]."
            },
            {
                "input_data": "[1, 2]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Length 1."
            },
            {
                "input_data": "[1]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Single node diameter 0."
            }
        ]
    },
    {
        "title": "Path Sum",
        "slug": "path-sum",
        "topic": "Tree",
        "difficulty": "Easy",
        "description": "Given the `root` of a binary tree and an integer `targetSum`, return `True` if the tree has a root-to-leaf path such that adding up all the values along the path equals `targetSum`.",
        "constraints": "0 <= number of nodes <= 5000\n-1000 <= targetSum <= 1000\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Subtract node.val from targetSum and recurse down to leaf nodes."
        ],
        "starter_code": {
            "python": "def hasPathSum(nums: list, targetSum: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function hasPathSum(nums, targetSum) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean hasPathSum(Integer[] nums, int targetSum) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool hasPathSum(vector<int>& nums, int targetSum) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]\n22",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "5 -> 4 -> 11 -> 2 sums to 22."
            },
            {
                "input_data": "[1, 2, 3]\n5",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "No root-to-leaf path sums to 5."
            },
            {
                "input_data": "[]\n0",
                "expected_output": "False",
                "is_sample": False,
                "explanation": "Empty tree."
            }
        ]
    },
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-binary-search-tree",
        "topic": "BST",
        "difficulty": "Medium",
        "description": "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).",
        "constraints": "1 <= number of nodes <= 10^4\n-2^31 <= Node.val <= 2^31 - 1\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Pass down valid range (min_val, max_val) to each recursive call."
        ],
        "starter_code": {
            "python": "def isValidBST(vals: list) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isValidBST(vals) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isValidBST(Integer[] vals) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isValidBST(vector<int>& vals) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[2, 1, 3]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Valid BST."
            },
            {
                "input_data": "[5, 1, 4, None, None, 3, 6]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Root 5 has right child 4 < 5."
            },
            {
                "input_data": "[1]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Single node is valid BST."
            }
        ]
    },
    {
        "title": "Lowest Common Ancestor of a Binary Tree",
        "slug": "lowest-common-ancestor-of-a-binary-tree",
        "topic": "Tree",
        "difficulty": "Medium",
        "description": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes `p` and `q`.",
        "constraints": "2 <= nodes <= 10^5\nAll Node.val are unique.\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Post-order traversal: if left and right both return non-None, current node is LCA."
        ],
        "starter_code": {
            "python": "def lowestCommonAncestorBT(root_val: int, p: int, q: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function lowestCommonAncestorBT(root_val, p, q) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int lowestCommonAncestorBT(int root_val, int p, int q) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int lowestCommonAncestorBT(int root_val, int p, int q) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "3\n5\n1",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "LCA of 5 and 1 is 3."
            },
            {
                "input_data": "5\n5\n4",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "LCA of 5 and 4 is 5."
            },
            {
                "input_data": "1\n1\n2",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Root is LCA."
            }
        ]
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "slug": "binary-tree-level-order-traversal",
        "topic": "Tree",
        "difficulty": "Medium",
        "description": "Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
        "constraints": "0 <= number of nodes <= 2000\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Use a queue for standard BFS level order."
        ],
        "starter_code": {
            "python": "def levelOrder(root: list) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function levelOrder(root) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> levelOrder(Integer[] root) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> levelOrder(vector<int>& root) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 9, 20, None, None, 15, 7]",
                "expected_output": "[[3], [9, 20], [15, 7]]",
                "is_sample": True,
                "explanation": "Level order traversal."
            },
            {
                "input_data": "[1]",
                "expected_output": "[[1]]",
                "is_sample": True,
                "explanation": "Single node."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty tree."
            }
        ]
    },
    {
        "title": "Binary Tree Right Side View",
        "slug": "binary-tree-right-side-view",
        "topic": "Tree",
        "difficulty": "Medium",
        "description": "Given the `root` of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.",
        "constraints": "0 <= number of nodes <= 100\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "BFS level order taking the last element of each level, or DFS visiting right subtree first."
        ],
        "starter_code": {
            "python": "def rightSideView(root: list) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function rightSideView(root) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> rightSideView(Integer[] root) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> rightSideView(vector<int>& root) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, None, 5, None, 4]",
                "expected_output": "[1, 3, 4]",
                "is_sample": True,
                "explanation": "Right side view is [1, 3, 4]."
            },
            {
                "input_data": "[1, None, 3]",
                "expected_output": "[1, 3]",
                "is_sample": True,
                "explanation": "Right side view."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty tree."
            }
        ]
    },
    {
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "slug": "construct-binary-tree-from-preorder-and-inorder-traversal",
        "topic": "Tree",
        "difficulty": "Medium",
        "description": "Given two integer arrays `preorder` and `inorder`, construct and return the binary tree (as level-order array).",
        "constraints": "1 <= preorder.length <= 3000\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "First element in preorder is root; split inorder at that element into left and right subtrees."
        ],
        "starter_code": {
            "python": "def buildTree(preorder: list[int], inorder: list[int]) -> list:\n    # Write your solution here\n    pass\n",
            "javascript": "function buildTree(preorder, inorder) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public Integer[] buildTree(int[] preorder, int[] inorder) {\n        // Write your solution here\n        return None;\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> buildTree(vector<int>& preorder, vector<int>& inorder) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 9, 20, 15, 7]\n[9, 3, 15, 20, 7]",
                "expected_output": "[3, 9, 20, None, None, 15, 7]",
                "is_sample": True,
                "explanation": "Reconstructed binary tree."
            },
            {
                "input_data": "[-1]\n[-1]",
                "expected_output": "[-1]",
                "is_sample": True,
                "explanation": "Single node tree."
            },
            {
                "input_data": "[1, 2]\n[2, 1]",
                "expected_output": "[1, 2]",
                "is_sample": False,
                "explanation": "Two nodes."
            }
        ]
    },
    {
        "title": "Kth Smallest Element in a BST",
        "slug": "kth-smallest-element-in-a-bst",
        "topic": "BST",
        "difficulty": "Medium",
        "description": "Given the `root` of a binary search tree and an integer `k`, return the `k-th` smallest value (1-indexed) of all the values of the nodes in the tree.",
        "constraints": "1 <= k <= n <= 10^4\nOptimal Time: O(H + k), Space: O(H)",
        "hints": [
            "In-order traversal of a BST visits nodes in strictly ascending order."
        ],
        "starter_code": {
            "python": "def kthSmallest(root: list, k: int) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function kthSmallest(root, k) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int kthSmallest(Integer[] root, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int kthSmallest(vector<int>& root, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[3, 1, 4, None, 2]\n1",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1st smallest element is 1."
            },
            {
                "input_data": "[5, 3, 6, 2, 4, None, None, 1]\n3",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3rd smallest element is 3."
            },
            {
                "input_data": "[10]\n1",
                "expected_output": "10",
                "is_sample": False,
                "explanation": "Single node."
            }
        ]
    },
    {
        "title": "Flatten Binary Tree to Linked List",
        "slug": "flatten-binary-tree-to-linked-list",
        "topic": "Tree",
        "difficulty": "Medium",
        "description": "Given the `root` of a binary tree, flatten the tree into a 'linked list' in-place (following pre-order traversal order, with right pointers).",
        "constraints": "0 <= number of nodes <= 2000\nOptimal Time: O(n), Space: O(1) Morris traversal",
        "hints": [
            "For each node with left child, find the rightmost node of left subtree and attach right child there."
        ],
        "starter_code": {
            "python": "def flattenTree(root: list) -> list:\n    # Write your solution here\n    pass\n",
            "javascript": "function flattenTree(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public Integer[] flattenTree(Integer[] root) {\n        // Write your solution here\n        return None;\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> flattenTree(vector<int>& root) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 5, 3, 4, None, 6]",
                "expected_output": "[1, None, 2, None, 3, None, 4, None, 5, None, 6]",
                "is_sample": True,
                "explanation": "Pre-order flattened linked list."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty tree."
            },
            {
                "input_data": "[0]",
                "expected_output": "[0]",
                "is_sample": False,
                "explanation": "Single node."
            }
        ]
    },
    {
        "title": "Path Sum II",
        "slug": "path-sum-ii",
        "topic": "Tree",
        "difficulty": "Medium",
        "description": "Given the `root` of a binary tree and an integer `targetSum`, return all root-to-leaf paths where the sum of the node values in the path equals `targetSum`.",
        "constraints": "0 <= number of nodes <= 5000\n-1000 <= targetSum <= 1000\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Backtracking DFS tracking current path and remaining targetSum."
        ],
        "starter_code": {
            "python": "def pathSum(root: list, targetSum: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function pathSum(root, targetSum) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> pathSum(Integer[] root, int targetSum) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> pathSum(vector<int>& root, int targetSum) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]\n22",
                "expected_output": "[[5, 4, 11, 2], [5, 8, 4, 5]]",
                "is_sample": True,
                "explanation": "Two root-to-leaf paths sum to 22."
            },
            {
                "input_data": "[1, 2, 3]\n5",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "No paths."
            },
            {
                "input_data": "[1, 2]\n0",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "No path with sum 0."
            }
        ]
    },
    {
        "title": "Implement Trie (Prefix Tree)",
        "slug": "implement-trie-prefix-tree",
        "topic": "Trie",
        "difficulty": "Medium",
        "description": "A trie (pronounced as 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement the `Trie` class with `insert`, `search`, and `startsWith`.",
        "constraints": "1 <= word.length, prefix.length <= 2000\nOptimal Time: O(m) per operation, Space: O(total characters * alphabet size)",
        "hints": [
            "Each node contains 26 children (or a dict) and a boolean is_end_of_word."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"Trie\", \"insert\", \"search\", \"search\", \"startsWith\", \"insert\", \"search\"]\n[[], [\"apple\"], [\"apple\"], [\"app\"], [\"app\"], [\"app\"], [\"app\"]]",
                "expected_output": "[None, None, True, False, True, None, True]",
                "is_sample": True,
                "explanation": "Trie operations."
            },
            {
                "input_data": "[\"Trie\", \"search\"]\n[[], [\"a\"]]",
                "expected_output": "[None, False]",
                "is_sample": True,
                "explanation": "Search empty trie."
            },
            {
                "input_data": "[\"Trie\", \"insert\", \"startsWith\"]\n[[], [\"hello\"], [\"hell\"]]",
                "expected_output": "[None, None, True]",
                "is_sample": False,
                "explanation": "Prefix lookup."
            }
        ]
    },
    {
        "title": "Design Add and Search Words Data Structure",
        "slug": "design-add-and-search-words-data-structure",
        "topic": "Trie",
        "difficulty": "Medium",
        "description": "Design a data structure that supports adding new words and finding if a string matches any previously added string, where `.` can match any letter.",
        "constraints": "1 <= word.length <= 25\nAt most 10^4 calls\nOptimal Time: O(m) insert, O(26^dots * m) search",
        "hints": [
            "Trie with DFS for handling '.' wildcard."
        ],
        "starter_code": {
            "python": "    def __init__(self):\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"WordDictionary\", \"addWord\", \"addWord\", \"addWord\", \"search\", \"search\", \"search\", \"search\"]\n[[], [\"bad\"], [\"dad\"], [\"mad\"], [\"pad\"], [\"bad\"], [\".ad\"], [\"b..\"]]",
                "expected_output": "[None, None, None, None, False, True, True, True]",
                "is_sample": True,
                "explanation": "Wildcard searching."
            },
            {
                "input_data": "[\"WordDictionary\", \"search\"]\n[[], [\"a\"]]",
                "expected_output": "[None, False]",
                "is_sample": True,
                "explanation": "Empty dictionary."
            },
            {
                "input_data": "[\"WordDictionary\", \"addWord\", \"search\"]\n[[], [\"a\"], [\".\"]]",
                "expected_output": "[None, None, True]",
                "is_sample": False,
                "explanation": "Single dot matches 'a'."
            }
        ]
    },
    {
        "title": "Binary Tree Maximum Path Sum",
        "slug": "binary-tree-maximum-path-sum",
        "topic": "Tree",
        "difficulty": "Hard",
        "description": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. Return the maximum path sum of any non-empty path.",
        "constraints": "1 <= number of nodes <= 3 * 10^4\n-1000 <= Node.val <= 1000\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Post-order traversal: compute max gain from each subtree max(0, gain), update global max with left + right + node.val."
        ],
        "starter_code": {
            "python": "def maxPathSum(root: list) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function maxPathSum(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int maxPathSum(Integer[] root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int maxPathSum(vector<int>& root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]",
                "expected_output": "6",
                "is_sample": True,
                "explanation": "2 + 1 + 3 = 6."
            },
            {
                "input_data": "[-10, 9, 20, None, None, 15, 7]",
                "expected_output": "42",
                "is_sample": True,
                "explanation": "15 + 20 + 7 = 42."
            },
            {
                "input_data": "[-3]",
                "expected_output": "-3",
                "is_sample": False,
                "explanation": "Single negative node."
            }
        ]
    },
    {
        "title": "Serialize and Deserialize Binary Tree",
        "slug": "serialize-and-deserialize-binary-tree",
        "topic": "Tree",
        "difficulty": "Hard",
        "description": "Design an algorithm to serialize and deserialize a binary tree (convert to string and recover the tree).",
        "constraints": "0 <= number of nodes <= 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Pre-order traversal with 'None' / '#' tokens for None nodes."
        ],
        "starter_code": {
            "python": "    def serialize(self, root: list) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function solve() {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    // Write your solution here\n}\n",
            "cpp": "class Solution {\npublic:\n    // Write your solution here\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, None, None, 4, 5]",
                "expected_output": "[1, 2, 3, None, None, 4, 5]",
                "is_sample": True,
                "explanation": "Round-trip serialization."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Empty tree."
            },
            {
                "input_data": "[1]",
                "expected_output": "[1]",
                "is_sample": False,
                "explanation": "Single node."
            }
        ]
    },
    {
        "title": "Binary Tree Cameras",
        "slug": "binary-tree-cameras",
        "topic": "Tree",
        "difficulty": "Hard",
        "description": "You are given the `root` of a binary tree. We install cameras on the nodes of the tree. Each camera at a node can monitor its parent, itself, and its immediate children. Return the minimum number of cameras needed to monitor all nodes of the tree.",
        "constraints": "1 <= number of nodes <= 1000\nOptimal Time: O(n), Space: O(h)",
        "hints": [
            "Greedy post-order: place cameras on parents of uncovered leaves."
        ],
        "starter_code": {
            "python": "def minCameraCover(root: list) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function minCameraCover(root) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int minCameraCover(Integer[] root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int minCameraCover(vector<int>& root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[0, 0, None, 0, 0]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 camera is sufficient."
            },
            {
                "input_data": "[0, 0, None, 0, None, 0, None, None, 0]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 cameras needed."
            },
            {
                "input_data": "[0]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single node needs 1 camera."
            }
        ]
    },
    {
        "title": "Word Search II",
        "slug": "word-search-ii",
        "topic": "Trie",
        "difficulty": "Hard",
        "description": "Given an `m x n` `board` of characters and a list of strings `words`, return all words on the board.",
        "constraints": "1 <= m, n <= 12\n1 <= words.length <= 3 * 10^4\n1 <= words[i].length <= 10\nOptimal Time: O(M * 4 * 3^(L-1)), Space: O(N) where N is total characters in words",
        "hints": [
            "Insert all words into a Trie, then perform DFS backtracking on the board."
        ],
        "starter_code": {
            "python": "def findWords(board: list[list[str]], words: list[str]) -> list[str]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findWords(board, words) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<String> findWords(char[][] board, String[] words) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[\"o\", \"a\", \"a\", \"n\"], [\"e\", \"t\", \"a\", \"e\"], [\"i\", \"h\", \"k\", \"r\"], [\"i\", \"f\", \"l\", \"v\"]]\n[\"oath\", \"pea\", \"eat\", \"rain\"]",
                "expected_output": "[\"eat\", \"oath\"]",
                "is_sample": True,
                "explanation": "\"eat\" and \"oath\" are on board."
            },
            {
                "input_data": "[[\"a\", \"b\"], [\"c\", \"d\"]]\n[\"abcb\"]",
                "expected_output": "[]",
                "is_sample": True,
                "explanation": "Letters cannot be reused."
            },
            {
                "input_data": "[[\"a\"]]\n[\"a\"]",
                "expected_output": "[\"a\"]",
                "is_sample": False,
                "explanation": "Single cell."
            }
        ]
    }
]
