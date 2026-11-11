
import ast

from suggestions import generate_suggestions


class LoopAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.for_loops = 0
        self.while_loops = 0
        self.loop_depth = 0

        self.nested_loops = []
        self.membership_checks = []
        self.collection_types = {}

    # Detect list, set and dictionary assignments
    def visit_Assign(self, node):
        value = node.value

        if isinstance(value, ast.List):
            collection_type = "list"
        elif isinstance(value, ast.Set):
            collection_type = "set"
        elif isinstance(value, ast.Dict):
            collection_type = "dictionary"
        else:
            collection_type = None

        if collection_type:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.collection_types[target.id] = collection_type

        self.generic_visit(node)

    # Detect for loops
    def visit_For(self, node):
        self.for_loops += 1

        if self.loop_depth > 0:
            self.nested_loops.append(node.lineno)

        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    # Detect while loops
    def visit_While(self, node):
        self.while_loops += 1

        if self.loop_depth > 0:
            self.nested_loops.append(node.lineno)

        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    # Detect membership checks inside loops
    def visit_Compare(self, node):
        if self.loop_depth > 0:
            for operation, comparator in zip(
                node.ops, node.comparators
            ):
                if isinstance(operation, (ast.In, ast.NotIn)):

                    if isinstance(comparator, ast.Name):
                        collection_name = comparator.id
                        collection_type = self.collection_types.get(
                            collection_name, "unknown"
                        )
                    else:
                        collection_name = "unknown"
                        collection_type = "unknown"

                    self.membership_checks.append({
                        "line": node.lineno,
                        "collection": collection_name,
                        "type": collection_type
                    })

        self.generic_visit(node)


# Ask user for Python file path
file_path = input("Enter Python file path: ").strip()

# Read selected Python file
try:
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

except FileNotFoundError:
    print("Error: File not found.")
    raise SystemExit

except PermissionError:
    print("Error: Permission denied.")
    raise SystemExit

except OSError as error:
    print("File reading error:", error)
    raise SystemExit


# Convert source code into AST
try:
    tree = ast.parse(source_code)

except SyntaxError as error:
    print("\n--- Syntax Error Detected ---")
    print("Error:", error.msg)
    print("Line Number:", error.lineno)
    print("Column Number:", error.offset)
    raise SystemExit


# Analyze the AST
analyzer = LoopAnalyzer()
analyzer.visit(tree)


# Display static analysis report
print("\n--- GreenCode Static Analysis ---")

print("For Loops:", analyzer.for_loops)
print("While Loops:", analyzer.while_loops)
print("Nested Loops:", len(analyzer.nested_loops))

if analyzer.nested_loops:
    print("\nPotential Nested Loop Warnings:")

    for line in analyzer.nested_loops:
        print("Nested loop detected at line:", line)
else:
    print("\nNo nested loops detected.")


# Display membership check report
print(
    "\nMembership Checks Inside Loops:",
    len(analyzer.membership_checks)
)

for check in analyzer.membership_checks:
    print(
        f"Line {check['line']}: "
        f"{check['collection']} "
        f"({check['type']})"
    )


# Generate optimization suggestions
suggestions = generate_suggestions(
    analyzer.nested_loops,
    analyzer.for_loops,
    analyzer.while_loops,
    analyzer.membership_checks
)


# Display optimization suggestions
print("\n--- Optimization Suggestions ---")

for item in suggestions:
    print("\nIssue:", item["issue"])
    print("Severity:", item["severity"])
    print("Suggestion:", item["suggestion"])
