"""
greedy_intervals.py - Coding Question Bank module: sanitized starter code.
"""

from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Assign Cookies",
        "slug": "assign-cookies",
        "topic": "Greedy",
        "difficulty": "Easy",
        "description": "Assume you are an awesome parent and want to give your children some cookies. Each child `i` has a greed factor `g[i]`, and each cookie `j` has a size `s[j]`. Return the maximum number of children you can make content.",
        "constraints": "1 <= g.length, s.length <= 3 * 10^4\n1 <= g[i], s[j] <= 2^31 - 1\nOptimal Time: O(n log n + m log m), Space: O(1)",
        "hints": [
            "Sort both greed factors and cookie sizes; greedily satisfy the least greedy child first."
        ],
        "starter_code": {
            "python": "def findContentChildren(g: list[int], s: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findContentChildren(g, s) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findContentChildren(int[] g, int[] s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findContentChildren(vector<int>& g, vector<int>& s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3]\n[1, 1]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Only 1 child can be made content."
            },
            {
                "input_data": "[1, 2]\n[1, 2, 3]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Both children made content."
            },
            {
                "input_data": "[2]\n[1]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Cookie too small."
            }
        ]
    },
    {
        "title": "Lemonade Change",
        "slug": "lemonade-change",
        "topic": "Greedy",
        "difficulty": "Easy",
        "description": "At a lemonade stand, each lemonade costs $5. Customers pay with $5, $10, or $20 bills. Return `True` if you can provide every customer with correct change, or `False` otherwise.",
        "constraints": "1 <= bills.length <= 10^5\nbills[i] is 5, 10, or 20\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "Greedily prefer giving $10 + $5 as change for a $20 bill to preserve $5 bills."
        ],
        "starter_code": {
            "python": "def lemonadeChange(bills: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function lemonadeChange(bills) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean lemonadeChange(int[] bills) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool lemonadeChange(vector<int>& bills) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[5, 5, 5, 10, 20]",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "All change provided successfully."
            },
            {
                "input_data": "[5, 5, 10, 10, 20]",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "Not enough $5 bills for the last customer."
            },
            {
                "input_data": "[5]",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Exact change."
            }
        ]
    },
    {
        "title": "Gas Station",
        "slug": "gas-station",
        "topic": "Greedy",
        "difficulty": "Medium",
        "description": "There are `n` gas stations along a circular route. You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i-th` station to the next `(i + 1)-th` station. Return the starting gas station's index if you can travel around the circuit once, or `-1`.",
        "constraints": "n == gas.length == cost.length\n1 <= n <= 10^5\nOptimal Time: O(n), Space: O(1)",
        "hints": [
            "If total gas < total cost, it's impossible. Otherwise, whenever tank drops below 0, reset start to next station."
        ],
        "starter_code": {
            "python": "def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function canCompleteCircuit(gas, cost) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int canCompleteCircuit(int[] gas, int[] cost) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 4, 5]\n[3, 4, 5, 1, 2]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Start at station 3."
            },
            {
                "input_data": "[2, 3, 4]\n[3, 4, 3]",
                "expected_output": "-1",
                "is_sample": True,
                "explanation": "Impossible to complete circuit."
            },
            {
                "input_data": "[5, 1, 2, 3, 4]\n[4, 4, 1, 5, 1]",
                "expected_output": "4",
                "is_sample": False,
                "explanation": "Start index 4."
            }
        ]
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "topic": "Intervals",
        "difficulty": "Medium",
        "description": "Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals.",
        "constraints": "1 <= intervals.length <= 10^4\n0 <= starti <= endi <= 10^4\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Sort intervals by start time; merge if next start <= previous end."
        ],
        "starter_code": {
            "python": "def merge(intervals: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function merge(intervals) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[][] merge(int[][] intervals) {\n        // Write your solution here\n        return new int[][]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> merge(vector<vector<int>>& intervals) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 3], [2, 6], [8, 10], [15, 18]]",
                "expected_output": "[[1, 6], [8, 10], [15, 18]]",
                "is_sample": True,
                "explanation": "[1, 3] and [2, 6] overlap into [1, 6]."
            },
            {
                "input_data": "[[1, 4], [4, 5]]",
                "expected_output": "[[1, 5]]",
                "is_sample": True,
                "explanation": "Boundary overlap merges into [1, 5]."
            },
            {
                "input_data": "[[1, 4]]",
                "expected_output": "[[1, 4]]",
                "is_sample": False,
                "explanation": "Single interval."
            }
        ]
    },
    {
        "title": "Insert Interval",
        "slug": "insert-interval",
        "topic": "Intervals",
        "difficulty": "Medium",
        "description": "You are given an array of non-overlapping intervals sorted by start time and a `newInterval`. Insert `newInterval` into `intervals` such that intervals are still sorted and non-overlapping.",
        "constraints": "0 <= intervals.length <= 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Three stages: add before intervals, merge overlapping, add after intervals."
        ],
        "starter_code": {
            "python": "def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "javascript": "function insert(intervals, newInterval) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int[][] insert(int[][] intervals, int[] newInterval) {\n        // Write your solution here\n        return new int[][]{};\n    }\n}\n",
            "cpp": "#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 3], [6, 9]]\n[2, 5]",
                "expected_output": "[[1, 5], [6, 9]]",
                "is_sample": True,
                "explanation": "Merged into [1, 5]."
            },
            {
                "input_data": "[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]\n[4, 8]",
                "expected_output": "[[1, 2], [3, 10], [12, 16]]",
                "is_sample": True,
                "explanation": "Merged [3, 5], [6, 7], [8, 10] into [3, 10]."
            },
            {
                "input_data": "[]\n[5, 7]",
                "expected_output": "[[5, 7]]",
                "is_sample": False,
                "explanation": "Empty list insert."
            }
        ]
    },
    {
        "title": "Non-overlapping Intervals",
        "slug": "non-overlapping-intervals",
        "topic": "Intervals",
        "difficulty": "Medium",
        "description": "Given an array of intervals `intervals`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "constraints": "1 <= intervals.length <= 10^5\nOptimal Time: O(n log n), Space: O(1)",
        "hints": [
            "Sort intervals by end time; greedily keep interval that ends earliest."
        ],
        "starter_code": {
            "python": "def eraseOverlapIntervals(intervals: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function eraseOverlapIntervals(intervals) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int eraseOverlapIntervals(int[][] intervals) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int eraseOverlapIntervals(vector<vector<int>>& intervals) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[1, 2], [2, 3], [3, 4], [1, 3]]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "Remove [1, 3] to leave non-overlapping intervals."
            },
            {
                "input_data": "[[1, 2], [1, 2], [1, 2]]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Remove 2 intervals."
            },
            {
                "input_data": "[[1, 2], [2, 3]]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "Already non-overlapping."
            }
        ]
    },
    {
        "title": "Meeting Rooms II",
        "slug": "meeting-rooms-ii",
        "topic": "Intervals",
        "difficulty": "Medium",
        "description": "Given an array of meeting time intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of conference rooms required.",
        "constraints": "1 <= intervals.length <= 10^4\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Sort start times and end times separately, then use two pointers."
        ],
        "starter_code": {
            "python": "def minMeetingRooms(intervals: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function minMeetingRooms(intervals) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int minMeetingRooms(int[][] intervals) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int minMeetingRooms(vector<vector<int>>& intervals) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[0, 30], [5, 10], [15, 20]]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "2 rooms required."
            },
            {
                "input_data": "[[7, 10], [2, 4]]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 room required."
            },
            {
                "input_data": "[[1, 5], [5, 6]]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Adjacent meetings share 1 room."
            }
        ]
    },
    {
        "title": "Minimum Number of Arrows to Burst Balloons",
        "slug": "minimum-number-of-arrows-to-burst-balloons",
        "topic": "Greedy",
        "difficulty": "Medium",
        "description": "There are spherical balloons taped to a flat wall that represents the XY-plane. Return the minimum number of arrows that must be shot to burst all balloons.",
        "constraints": "1 <= points.length <= 10^5\nOptimal Time: O(n log n), Space: O(1)",
        "hints": [
            "Sort by end coordinate and greedily shoot arrow at end coordinate."
        ],
        "starter_code": {
            "python": "def findMinArrowShots(points: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function findMinArrowShots(points) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int findMinArrowShots(int[][] points) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int findMinArrowShots(vector<vector<int>>& points) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[10, 16], [2, 8], [1, 6], [7, 12]]",
                "expected_output": "2",
                "is_sample": True,
                "explanation": "Shoot at x = 6 and x = 12."
            },
            {
                "input_data": "[[1, 2], [3, 4], [5, 6], [7, 8]]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "4 distinct balloons."
            },
            {
                "input_data": "[[1, 2], [2, 3], [3, 4], [4, 5]]",
                "expected_output": "2",
                "is_sample": False,
                "explanation": "2 arrows."
            }
        ]
    },
    {
        "title": "Hand of Straights",
        "slug": "hand-of-straights",
        "topic": "Greedy",
        "difficulty": "Medium",
        "description": "Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size `groupSize`, and consists of `groupSize` consecutive cards. Return `True` if she can.",
        "constraints": "1 <= hand.length <= 10^4\n1 <= groupSize <= hand.length\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Count cards and greedily try to complete runs starting from smallest available card."
        ],
        "starter_code": {
            "python": "def isNStraightHand(hand: list[int], groupSize: int) -> bool:\n    # Write your solution here\n    pass\n",
            "javascript": "function isNStraightHand(hand, groupSize) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public boolean isNStraightHand(int[] hand, int groupSize) {\n        // Write your solution here\n        return False;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    bool isNStraightHand(vector<int>& hand, int groupSize) {\n        // Write your solution here\n        return False;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 2, 3, 6, 2, 3, 4, 7, 8]\n3",
                "expected_output": "True",
                "is_sample": True,
                "explanation": "[1, 2, 3], [2, 3, 4], [6, 7, 8]."
            },
            {
                "input_data": "[1, 2, 3, 4, 5]\n4",
                "expected_output": "False",
                "is_sample": True,
                "explanation": "5 is not divisible by 4."
            },
            {
                "input_data": "[1]\n1",
                "expected_output": "True",
                "is_sample": False,
                "explanation": "Single card."
            }
        ]
    },
    {
        "title": "Candy",
        "slug": "candy",
        "topic": "Greedy",
        "difficulty": "Hard",
        "description": "There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`. Children with a higher rating get more candies than their neighbors. Each child must have at least one candy. Return the minimum number of candies you need to distribute.",
        "constraints": "n == ratings.length\n1 <= n <= 2 * 10^4\n0 <= ratings[i] <= 2 * 10^4\nOptimal Time: O(n), Space: O(n)",
        "hints": [
            "Two passes: left-to-right (if ratings[i] > ratings[i-1]), then right-to-left (if ratings[i] > ratings[i+1])."
        ],
        "starter_code": {
            "python": "def candy(ratings: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function candy(ratings) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int candy(int[] ratings) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int candy(vector<int>& ratings) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[1, 0, 2]",
                "expected_output": "5",
                "is_sample": True,
                "explanation": "Candies allocated: [2, 1, 2] = 5."
            },
            {
                "input_data": "[1, 2, 2]",
                "expected_output": "4",
                "is_sample": True,
                "explanation": "Candies allocated: [1, 2, 1] = 4."
            },
            {
                "input_data": "[1]",
                "expected_output": "1",
                "is_sample": False,
                "explanation": "Single child 1 candy."
            }
        ]
    },
    {
        "title": "Course Schedule III",
        "slug": "course-schedule-iii",
        "topic": "Greedy",
        "difficulty": "Hard",
        "description": "There are `n` different online courses numbered from 1 to `n`. You are given an array `courses` where `courses[i] = [durationi, lastDayi]`. Return the maximum number of courses you can take.",
        "constraints": "1 <= courses.length <= 10^4\n1 <= durationi, lastDayi <= 10^4\nOptimal Time: O(n log n), Space: O(n)",
        "hints": [
            "Sort courses by deadline; maintain a max-heap of durations and evict longest course if schedule exceeds deadline."
        ],
        "starter_code": {
            "python": "def scheduleCourse(courses: list[list[int]]) -> int:\n    # Write your solution here\n    pass\n",
            "javascript": "function scheduleCourse(courses) {\n    // Write your solution here\n}\n",
            "java": "class Solution {\n    public int scheduleCourse(int[][] courses) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "class Solution {\npublic:\n    int scheduleCourse(vector<vector<int>>& courses) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "test_cases": [
            {
                "input_data": "[[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]",
                "expected_output": "3",
                "is_sample": True,
                "explanation": "Take course 1, 2, and 4 (total 3)."
            },
            {
                "input_data": "[[1, 2]]",
                "expected_output": "1",
                "is_sample": True,
                "explanation": "1 course."
            },
            {
                "input_data": "[[3, 2], [4, 3]]",
                "expected_output": "0",
                "is_sample": False,
                "explanation": "None can be completed."
            }
        ]
    }
]
