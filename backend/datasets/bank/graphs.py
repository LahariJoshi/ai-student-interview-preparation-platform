"""
graphs.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Find the Town Judge",
        "slug": "find-the-town-judge",
        "topic": "Graph",
        "difficulty": "Easy",
        "description": "In a town, there are `n` people labeled from 1 to `n`. There is a rumor that one of these people is secretly the town judge. The judge trusts nobody and everybody (except the judge) trusts the judge. Return the label of the town judge if they exist, or `-1` otherwise.",
        "constraints": "1 <= n <= 1000\n0 <= trust.length <= 10^4\nOptimal Time: O(n + trust.length), Space: O(n)",
        "hints": [
            "Compute trust score = in_degree - out_degree. Judge has score n - 1."
        ],
        "starter_code": {
            "python": "def findJudge(n: int, trust: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findJudge(n, trust) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findJudge(int n, int[][] trust) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findJudge(int n, vector<vector<int>>& trust) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2\n[[1, 2]]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Person 1 trusts person 2. Judge is 2."
            },
            {
                "input_data": "3\n[[1, 3], [2, 3]]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Person 3 is trusted by everyone."
            },
            {
                "input_data": "3\n[[1, 3], [2, 3], [3, 1]]",
                "expected_output": "-1",
                "is_sample": False,
                "explanation": "Judge trusts someone, so no judge."
            }
        ]
    },
    {
        "title": "Flood Fill",
        "slug": "flood-fill",
        "topic": "Graph",
        "difficulty": "Easy",
        "description": "An image is represented by an `m x n` integer grid `image` where `image[i][j]` represents the pixel value of the image. Perform a flood fill on the image starting from the pixel `(sr, sc)` with `color`.",
        "constraints": "1 <= m, n <= 50\n0 <= image[i][j], color < 65536\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "DFS or BFS starting at (sr, sc), replacing original color with new color."
        ],
        "starter_code": {
            "python": "def floodFill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function floodFill(image, sr, sc, color) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[][] floodFill(int[][] image, int sr, int sc, int color) {\n        // Write your solution here\n        return new int[][]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 1, 1], [1, 1, 0], [1, 0, 1]]\n1\n1\n2",
                "expected_output": "[[2, 2, 2], [2, 2, 0], [2, 0, 1]]",
                "is_sample": True,
                "explanation": "Connected 1s changed to 2."
            },
            {
                "input_data": "[[0, 0, 0], [0, 0, 0]]\n0\n0\n0",
                "expected_output": "[[0, 0, 0], [0, 0, 0]]",
                "is_sample": True,
                "explanation": "Target color is same as starting color."
            },
            {
                "input_data": "[[0]]\n0\n0\n1",
                "expected_output": "[[1]]",
                "is_sample": False,
                "explanation": "Single cell."
            }
        ]
    },
    {
        "title": "Island Perimeter",
        "slug": "island-perimeter",
        "topic": "Graph",
        "difficulty": "Easy",
        "description": "You are given `row x col` `grid` representing a map where `grid[i][j] = 1` represents land and `grid[i][j] = 0` represents water. Grid cells are connected horizontally/vertically. Determine the perimeter of the island.",
        "constraints": "1 <= row, col <= 100\nOptimal Time: O(row * col), Space: O(1)",
        "hints": [
            "Each land cell adds 4 to perimeter, minus 2 for every shared internal edge with neighboring land."
        ],
        "starter_code": {
            "python": "def islandPerimeter(grid: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function islandPerimeter(grid) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int islandPerimeter(int[][] grid) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int islandPerimeter(vector<vector<int>>& grid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]",
                "expected_output": "16",
                "is_sample": True,
                "explanation": "Perimeter is 16."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Single cell perimeter is 4."
            },
            {
                "input_data": "[[1, 0]]",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "Perimeter 4."
            }
        ]
    },
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.",
        "constraints": "1 <= m, n <= 300\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "Iterate over grid; upon finding '1', increment count and run BFS/DFS to sink the island."
        ],
        "starter_code": {
            "python": "def numIslands(grid: list[list[str]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function numIslands(grid) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int numIslands(char[][] grid) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[\"1\", \"1\", \"1\", \"1\", \"0\"], [\"1\", \"1\", \"0\", \"1\", \"0\"], [\"1\", \"1\", \"0\", \"0\", \"0\"], [\"0\", \"0\", \"0\", \"0\", \"0\"]]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 connected island."
            },
            {
                "input_data": "[[\"1\", \"1\", \"0\", \"0\", \"0\"], [\"1\", \"1\", \"0\", \"0\", \"0\"], [\"0\", \"0\", \"1\", \"0\", \"0\"], [\"0\", \"0\", \"0\", \"1\", \"1\"]]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 distinct islands."
            },
            {
                "input_data": "[[\"0\"]]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Water only."
            }
        ]
    },
    {
        "title": "Clone Graph",
        "slug": "clone-graph",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.",
        "constraints": "0 <= number of nodes <= 100\nOptimal Time: O(V + E), Space: O(V)",
        "hints": [
            "Use a hash map mapping original_node -> cloned_node with BFS or DFS."
        ],
        "starter_code": {
            "python": "def cloneGraph(adjList: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function cloneGraph(adjList) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[][] cloneGraph(int[][] adjList) {\n        // Write your solution here\n        return new int[][]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> cloneGraph(vector<vector<int>>& adjList) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[2, 4], [1, 3], [2, 4], [1, 3]]",
                "expected_output": "[[2, 4], [1, 3], [2, 4], [1, 3]]",
                "is_sample": True,
                "explanation": "Deep copy has identical adjacency list."
            },
            {
                "input_data": "[[]]",
                "expected_output": "[[]]",
                "is_sample": True,
                "explanation": "Single node with no neighbors."
            },
            {
                "input_data": "[]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Empty graph."
            }
        ]
    },
    {
        "title": "Course Schedule",
        "slug": "course-schedule",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "There are a total of `numCourses` courses you have to take, labeled from 0 to `numCourses - 1`. Some courses have prerequisites. Return `True` if you can finish all courses, or `False` otherwise.",
        "constraints": "1 <= numCourses <= 2000\n0 <= prerequisites.length <= 5000\nOptimal Time: O(V + E), Space: O(V + E) (Kahn's Algorithm)",
        "hints": [
            "Detect directed cycle using topological sort with in-degree array."
        ],
        "starter_code": {
            "python": "def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function canFinish(numCourses, prerequisites) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean canFinish(int numCourses, int[][] prerequisites) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2\n[[1, 0]]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "Course 0 -> Course 1 is possible."
            },
            {
                "input_data": "2\n[[1, 0], [0, 1]]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Cycle exists: impossible."
            },
            {
                "input_data": "1\n[]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "No prerequisites."
            }
        ]
    },
    {
        "title": "Course Schedule II",
        "slug": "course-schedule-ii",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "Return the ordering of courses you should take to finish all courses. If it is impossible to finish all courses, return an empty array.",
        "constraints": "1 <= numCourses <= 2000\nOptimal Time: O(V + E), Space: O(V + E)",
        "hints": [
            "Kahn's algorithm: record nodes as they are popped from the queue."
        ],
        "starter_code": {
            "python": "def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findOrder(numCourses, prerequisites) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] findOrder(int numCourses, int[][] prerequisites) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "2\n[[1, 0]]",
                "expected_output": "[0, 1]",
                "is_sample": True,
                "explanation": "Take course 0 then 1."
            },
            {
                "input_data": "4\n[[1, 0], [2, 0], [3, 1], [3, 2]]",
                "expected_output": "[0, 1, 2, 3]",
                "is_sample": True,
                "explanation": "Valid topological order."
            },
            {
                "input_data": "2\n[[0, 1], [1, 0]]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Cycle produces empty array."
            }
        ]
    },
    {
        "title": "Pacific Atlantic Water Flow",
        "slug": "pacific-atlantic-water-flow",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "Given an `m x n` matrix of non-negative integers representing the height of each unit cell in a continent, return a list of grid coordinates where water can flow to both the Pacific and Atlantic oceans.",
        "constraints": "1 <= m, n <= 200\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "Run two DFS/BFS traversals starting from the oceans inwards."
        ],
        "starter_code": {
            "python": "def pacificAtlantic(heights: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function pacificAtlantic(heights) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> pacificAtlantic(int[][] heights) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]",
                "expected_output": "[[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]",
                "is_sample": True,
                "explanation": "Cells flowing to both oceans."
            },
            {
                "input_data": "[[1]]",
                "expected_output": "[[0, 0]]",
                "is_sample": True,
                "explanation": "Single cell flows to both oceans."
            },
            {
                "input_data": "[[1, 1], [1, 1]]",
                "expected_output": "[[0, 0], [0, 1], [1, 0], [1, 1]]",
                "is_sample": False,
                "explanation": "Flat plain."
            }
        ]
    },
    {
        "title": "Surrounded Regions",
        "slug": "surrounded-regions",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "Given an `m x n` matrix `board` containing `'X'` and `'O'`, capture all regions that are 4-directionally surrounded by `'X'`. A region is captured by flipping all `'O'`s into `'X'`s in that surrounded region.",
        "constraints": "1 <= m, n <= 200\nOptimal Time: O(m * n), Space: O(m * n)",
        "hints": [
            "Flood fill from borders: mark 'O's connected to border as safe (e.g. 'S'), then flip remaining 'O' to 'X'."
        ],
        "starter_code": {
            "python": "def solveSurrounded(board: list[list[str]]) -> list[list[str]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function solveSurrounded(board) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public char[][] solveSurrounded(char[][] board) {\n        // Write your solution here\n        return None;\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<char>> solveSurrounded(vector<vector<char>>& board) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[\"X\", \"X\", \"X\", \"X\"], [\"X\", \"O\", \"O\", \"X\"], [\"X\", \"X\", \"O\", \"X\"], [\"X\", \"O\", \"X\", \"X\"]]",
                "expected_output": "[[\"X\", \"X\", \"X\", \"X\"], [\"X\", \"X\", \"X\", \"X\"], [\"X\", \"X\", \"X\", \"X\"], [\"X\", \"O\", \"X\", \"X\"]]",
                "is_sample": True,
                "explanation": "Surrounded regions captured."
            },
            {
                "input_data": "[[\"X\"]]",
                "expected_output": "[[\"X\"]]",
                "is_sample": True,
                "explanation": "Single X."
            },
            {
                "input_data": "[[\"O\"]]",
                "expected_output": "[[\"O\"]]",
                "is_sample": False,
                "explanation": "Border O remains."
            }
        ]
    },
    {
        "title": "Rotting Oranges",
        "slug": "rotting-oranges",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "You are given an `m x n` grid where each cell has values: 0 (empty), 1 (fresh orange), 2 (rotten orange). Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes until no fresh orange remains, or `-1`.",
        "constraints": "1 <= m, n <= 10\nOptimal Time: O(m * n), Space: O(m * n) (Multi-source BFS)",
        "hints": [
            "Multi-source BFS initialized with all initial rotten oranges."
        ],
        "starter_code": {
            "python": "def orangesRotting(grid: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function orangesRotting(grid) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int orangesRotting(int[][] grid) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int orangesRotting(vector<vector<int>>& grid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[2, 1, 1], [1, 1, 0], [0, 1, 1]]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "All rot in 4 minutes."
            },
            {
                "input_data": "[[2, 1, 1], [0, 1, 1], [1, 0, 1]]",
                "expected_output": "-1",
                "is_sample": True,
                "explanation": "Bottom left orange is unreachable."
            },
            {
                "input_data": "[[0, 2]]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "No fresh oranges."
            }
        ]
    },
    {
        "title": "Redundant Connection",
        "slug": "redundant-connection",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "In this problem, a tree is an undirected graph that is connected and has no cycles. Return an edge that can be removed so that the resulting graph is a tree of `n` nodes.",
        "constraints": "n == edges.length\n3 <= n <= 1000\nOptimal Time: O(n alpha(n)), Space: O(n) (Union-Find)",
        "hints": [
            "Union-Find: the edge whose two endpoints already belong to the same connected component creates a cycle."
        ],
        "starter_code": {
            "python": "def findRedundantConnection(edges: list[list[int]]) -> list[int]:\n    # Write your solution here\n    pass\n",
            "javascript": "function findRedundantConnection(edges) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[] findRedundantConnection(int[][] edges) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findRedundantConnection(vector<vector<int>>& edges) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2], [1, 3], [2, 3]]",
                "expected_output": "[2, 3]",
                "is_sample": True,
                "explanation": "Edge [2, 3] creates cycle."
            },
            {
                "input_data": "[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]",
                "expected_output": "[1, 4]",
                "is_sample": True,
                "explanation": "Edge [1, 4] creates cycle."
            },
            {
                "input_data": "[[1, 2], [2, 3], [1, 3]]",
                "expected_output": "[1, 3]",
                "is_sample": False,
                "explanation": "Cycle edge [1, 3]."
            }
        ]
    },
    {
        "title": "Number of Provinces",
        "slug": "number-of-provinces",
        "topic": "Graph",
        "difficulty": "Medium",
        "description": "There are `n` cities. A province is a group of directly or indirectly connected cities and no other cities outside of the group. Return the total number of provinces.",
        "constraints": "1 <= n <= 200\nisConnected[i][j] is 1 or 0.\nOptimal Time: O(n^2), Space: O(n)",
        "hints": [
            "Find connected components using DFS or Union-Find."
        ],
        "starter_code": {
            "python": "def findCircleNum(isConnected: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findCircleNum(isConnected) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findCircleNum(int[][] isConnected) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findCircleNum(vector<vector<int>>& isConnected) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 1, 0], [1, 1, 0], [0, 0, 1]]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 provinces: {0, 1} and {2}."
            },
            {
                "input_data": "[[1, 0, 0], [0, 1, 0], [0, 0, 1]]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "3 isolated cities."
            },
            {
                "input_data": "[[1, 1], [1, 1]]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "All connected."
            }
        ]
    },
    {
        "title": "Word Ladder",
        "slug": "word-ladder",
        "topic": "Graph",
        "difficulty": "Hard",
        "description": "Given two words `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, or 0 if no such sequence exists.",
        "constraints": "1 <= beginWord.length <= 10\n1 <= wordList.length <= 5000\nOptimal Time: O(M^2 * N), Space: O(M^2 * N) (BFS)",
        "hints": [
            "Bidirectional BFS or BFS exploring word transformations char by char."
        ],
        "starter_code": {
            "python": "def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function ladderLength(beginWord, endWord, wordList) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int ladderLength(String beginWord, String endWord, List<String> wordList) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "\"hit\"\n\"cog\"\n[\"hot\", \"dot\", \"dog\", \"lot\", \"log\", \"cog\"]",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "\"hit\" -> \"hot\" -> \"dot\" -> \"dog\" -> \"cog\" (length 5)."
            },
            {
                "input_data": "\"hit\"\n\"cog\"\n[\"hot\", \"dot\", \"dog\", \"lot\", \"log\"]",
                "expected_output": "0",
                "is_sample": True,
                "explanation": "\"cog\" is not in wordList."
            },
            {
                "input_data": "\"a\"\n\"c\"\n[\"a\", \"b\", \"c\"]",
                "expected_output": "2",
                "is_sample": False,
                "explanation": "\"a\" -> \"c\"."
            }
        ]
    },
    {
        "title": "Alien Dictionary",
        "slug": "alien-dictionary",
        "topic": "Graph",
        "difficulty": "Hard",
        "description": "There is a new alien language that uses the English alphabet. Given a list of words from the alien language's dictionary sorted lexicographically, return a string of the unique letters in the new alien language sorted in lexicographically increasing order.",
        "constraints": "1 <= words.length <= 100\n1 <= words[i].length <= 100\nOptimal Time: O(C) total characters, Space: O(1) alphabet size",
        "hints": [
            "Compare adjacent words to find first differing character; build directed graph and topological sort."
        ],
        "starter_code": {
            "python": "def alienOrder(words: list[str]) -> str:\n    # Write your solution here\n    pass\n",
            "javascript": "function alienOrder(words) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public String alienOrder(String[] words) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    string alienOrder(vector<string>& words) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[\"wrt\", \"wrf\", \"er\", \"ett\", \"rftt\"]",
                "expected_output": "\"wertf\"",
                "is_sample": True,
                "explanation": "Valid alien alphabetical order."
            },
            {
                "input_data": "[\"z\", \"x\"]",
                "expected_output": "\"zx\"",
                "is_sample": True,
                "explanation": "'z' comes before 'x'."
            },
            {
                "input_data": "[\"z\", \"x\", \"z\"]",
                "expected_output": "\"\"",
                "is_sample": False,
                "explanation": "Invalid cycle."
            }
        ]
    },
    {
        "title": "Critical Connections in a Network",
        "slug": "critical-connections-in-a-network",
        "topic": "Graph",
        "difficulty": "Hard",
        "description": "There are `n` servers numbered from 0 to `n - 1` connected by undirected server-to-server `connections`. Return all critical connections in the network in any order (bridges).",
        "constraints": "2 <= n <= 10^5\nn - 1 <= connections.length <= 10^5\nOptimal Time: O(V + E), Space: O(V + E) (Tarjan's Bridge-Finding)",
        "hints": [
            "Use Tarjan's or Floyd's algorithm tracking discovery time and lowest reachable timestamp."
        ],
        "starter_code": {
            "python": "def criticalConnections(n: int, connections: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function criticalConnections(n, connections) {\n    // Write your solution here\n}\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> criticalConnections(int n, List<List<Integer>> connections) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "4\n[[0, 1], [1, 2], [2, 0], [1, 3]]",
                "expected_output": "[[1, 3]]",
                "is_sample": True,
                "explanation": "[1, 3] is the only bridge."
            },
            {
                "input_data": "2\n[[0, 1]]",
                "expected_output": "[[0, 1]]",
                "is_sample": True,
                "explanation": "[0, 1] is critical."
            },
            {
                "input_data": "3\n[[0, 1], [1, 2], [2, 0]]",
                "expected_output": "[]",
                "is_sample": False,
                "explanation": "Cycle has no bridges."
            }
        ]
    }
]
