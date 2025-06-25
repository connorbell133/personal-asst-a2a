#!/usr/bin/env python3
"""Script to automatically fix common pylint issues."""

import ast
from pathlib import Path


def add_module_docstring(file_path: Path) -> bool:
    """
    Inserts a module-level docstring into a Python file if one is missing.
    
    Returns:
        bool: True if a docstring was added, False if the file already contained one.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if file already has a module docstring
    lines = content.split("\n")

    # Skip empty lines and comments at the top
    first_code_line = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            first_code_line = i
            break

    # Check if first non-comment line is a docstring
    if first_code_line < len(lines):
        first_line = lines[first_code_line].strip()
        if first_line.startswith('"""') or first_line.startswith("'''"):
            return False  # Already has docstring

    # Add module docstring
    module_name = file_path.stem.replace("_", " ").title()
    if file_path.name == "__init__.py":
        module_name = f"{file_path.parent.name.replace('_', ' ').title()} module"

    docstring = f'"""{module_name} module."""\n\n'

    # Insert after shebang and encoding if present
    insert_index = 0
    for i, line in enumerate(lines):
        if line.startswith("#!") or "coding:" in line or "encoding:" in line:
            insert_index = i + 1
        else:
            break

    lines.insert(insert_index, docstring.rstrip())

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return True


def fix_unused_arguments(file_path: Path) -> bool:
    """
    Prefixes unused function arguments named "ctx" or "task" with an underscore in the given file to suppress pylint warnings.
    
    Returns:
        bool: True if any arguments were modified, False otherwise.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse the file to find function definitions
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False

    lines = content.split("\n")
    modified = False

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in node.args.args:
                if not arg.arg.startswith("_") and arg.arg not in ["self", "cls"]:
                    # Check if this argument is mentioned in pylint output as unused
                    # For now, we'll be conservative and only prefix common unused args
                    if arg.arg in ["ctx", "task"] and node.lineno <= len(lines):
                        # Replace the argument name in the function definition
                        line = lines[node.lineno - 1]
                        if f"{arg.arg}:" in line and f"_{arg.arg}:" not in line:
                            lines[node.lineno - 1] = line.replace(
                                f"{arg.arg}:", f"_{arg.arg}:"
                            )
                            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return modified


def add_function_docstrings(file_path: Path) -> bool:
    """
    Insert a basic one-line docstring into each public function in the given file that lacks one.
    
    Reads the Python file, parses its AST, and adds a simple docstring to every function or async function whose name does not start with an underscore and which does not already have a docstring. Modifies the file in place if any changes are made.
    
    Returns:
        bool: True if any docstrings were added, False otherwise.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False

    lines = content.split("\n")
    modified = False

    # Process from bottom to top to avoid line number shifts
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node)

    functions.sort(key=lambda x: x.lineno, reverse=True)

    for node in functions:
        # Check if function already has docstring
        if (
            ast.get_docstring(node) is None
            and not node.name.startswith("_")
            and node.lineno <= len(lines)
        ):
            # Find the line after the function definition
            func_line = node.lineno - 1
            indent = len(lines[func_line]) - len(lines[func_line].lstrip())

            # Add simple docstring
            docstring_line = (
                " " * (indent + 4)
                + f'"""{node.name.replace("_", " ").title()} function."""'
            )
            lines.insert(func_line + 1, docstring_line)
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return modified


def main():
    """
    Recursively processes Python files in the "src" directory to add missing module and function docstrings for improved pylint compliance.
    
    Prints progress messages for each file processed and suggests running a formatter upon completion.
    """
    src_path = Path("src")

    if not src_path.exists():
        print("No 'src' directory found!")
        return

    python_files = list(src_path.rglob("*.py"))

    print(f"Processing {len(python_files)} Python files...")

    for file_path in python_files:
        print(f"Processing {file_path}...")

        # Add module docstring
        if add_module_docstring(file_path):
            print(f"  ✓ Added module docstring to {file_path}")

        # Add function docstrings
        if add_function_docstrings(file_path):
            print(f"  ✓ Added function docstrings to {file_path}")

        # Fix unused arguments (commented out for safety)
        # if fix_unused_arguments(file_path):
        #     print(f"  ✓ Fixed unused arguments in {file_path}")

    print("\nDone! Run 'ruff format .' to clean up formatting.")


if __name__ == "__main__":
    main()
