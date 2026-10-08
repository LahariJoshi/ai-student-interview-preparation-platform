"""
sanitize_bank_files.py - Rewrite backend/datasets/bank/*.py starter_code to be skeleton-only.
"""

import os
import sys
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from datasets.bank import arrays, strings, hash_tables, linked_lists, stacks_queues, binary_search, trees, heaps, graphs, dp, backtracking, greedy_intervals, math_bit_matrix

def clean_python_starter(code: str) -> str:
    lines = code.splitlines()
    sig_lines = []
    in_sig = False
    is_class = False
    class_header = ""

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("class ") and "Solution" in stripped:
            is_class = True
            class_header = line
            continue
        if stripped.startswith("def ") or in_sig:
            sig_lines.append(line)
            if stripped.endswith(":") or "):" in stripped or (") -> " in stripped and stripped.endswith(":")):
                break
            in_sig = True

    if sig_lines:
        sig = "\n".join(sig_lines)
        if is_class:
            return f"{class_header}\n    {sig.strip()}\n        # Write your solution here\n        pass\n"
        return f"{sig}\n    # Write your solution here\n    pass\n"
    return "def solve():\n    # Write your solution here\n    pass\n"


def clean_javascript_starter(code: str) -> str:
    lines = code.splitlines()
    fn_line = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("function ") or " = function(" in stripped or stripped.startswith("var ") or stripped.startswith("const "):
            if "{" in stripped:
                fn_line = stripped[:stripped.index("{")].strip()
            else:
                fn_line = stripped
            break
    if fn_line:
        return f"{fn_line} {{\n    // Write your solution here\n}}\n"
    return "function solve() {\n    // Write your solution here\n}\n"


def clean_java_starter(code: str) -> str:
    method_match = re.search(r"public\s+([A-Za-z0-9_<>[\]]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)", code)
    if method_match:
        ret_type = method_match.group(1).strip()
        method_name = method_match.group(2).strip()
        params = method_match.group(3).strip()

        ret_val = "null"
        if ret_type in ("int", "long", "double", "float"):
            ret_val = "0"
        elif ret_type == "boolean":
            ret_val = "false"
        elif ret_type == "char":
            ret_val = "' '"
        elif ret_type == "String":
            ret_val = "\"\""
        elif ret_type == "int[]":
            ret_val = "new int[]{}"
        elif ret_type == "int[][]":
            ret_val = "new int[][]{}"
        elif ret_type == "String[]":
            ret_val = "new String[]{}"
        elif ret_type.startswith("List"):
            ret_val = "new ArrayList<>()"

        if ret_type == "void":
            body = "        // Write your solution here\n"
        else:
            body = f"        // Write your solution here\n        return {ret_val};\n"

        imports = "import java.util.*;\n\n" if "List" in ret_type or "ArrayList" in body else ""
        return f"{imports}class Solution {{\n    public {ret_type} {method_name}({params}) {{\n{body}    }}\n}}\n"

    return "class Solution {\n    // Write your solution here\n}\n"


def clean_cpp_starter(code: str) -> str:
    method_match = re.search(r"(?:public:\s*)?([A-Za-z0-9_<>[\]:*&]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)", code)
    if method_match:
        ret_type = method_match.group(1).replace("public:", "").strip()
        method_name = method_match.group(2).strip()
        params = method_match.group(3).strip()

        ret_val = "0"
        if ret_type == "bool":
            ret_val = "false"
        elif ret_type == "string":
            ret_val = "\"\""
        elif "vector" in ret_type:
            ret_val = "{}"
        elif "*" in ret_type:
            ret_val = "nullptr"

        if ret_type == "void":
            body = "        // Write your solution here\n"
        else:
            body = f"        // Write your solution here\n        return {ret_val};\n"

        includes = "#include <vector>\n#include <string>\nusing namespace std;\n\n" if "vector" in ret_type or "string" in ret_type else ""
        return f"{includes}class Solution {{\npublic:\n    {ret_type} {method_name}({params}) {{\n{body}    }}\n}};\n"

    return "class Solution {\npublic:\n    // Write your solution here\n};\n"


MODULE_MAP = {
    "arrays": arrays,
    "strings": strings,
    "hash_tables": hash_tables,
    "linked_lists": linked_lists,
    "stacks_queues": stacks_queues,
    "binary_search": binary_search,
    "trees": trees,
    "heaps": heaps,
    "graphs": graphs,
    "dp": dp,
    "backtracking": backtracking,
    "greedy_intervals": greedy_intervals,
    "math_bit_matrix": math_bit_matrix,
}


def sanitize_all_bank_files():
    for name, mod in MODULE_MAP.items():
        questions = getattr(mod, "QUESTIONS", [])
        for q in questions:
            st = q.get("starter_code", {})
            if "python" in st:
                st["python"] = clean_python_starter(st["python"])
            if "javascript" in st:
                st["javascript"] = clean_javascript_starter(st["javascript"])
            if "java" in st:
                st["java"] = clean_java_starter(st["java"])
            if "cpp" in st:
                st["cpp"] = clean_cpp_starter(st["cpp"])
            q["starter_code"] = st

        file_path = os.path.join(BASE_DIR, "datasets", "bank", f"{name}.py")
        header = f'"""\n{name}.py - Coding Question Bank module: sanitized starter code.\n"""\n\nfrom typing import List, Dict, Any\n\nQUESTIONS: List[Dict[str, Any]] = '
        content = header + json.dumps(questions, indent=4) + "\n"
        # Replace json booleans with Python booleans
        content = content.replace("true", "True").replace("false", "False").replace("null", "None")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Sanitized {len(questions)} questions in {name}.py")


if __name__ == "__main__":
    sanitize_all_bank_files()
    print("Done sanitizing all bank files.")
