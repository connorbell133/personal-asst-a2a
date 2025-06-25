import os

import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Get token from environment variable
BASE_URL = "https://api.github.com/repos"


def get_github_folder_contents(owner: str, repo: str, path: str = "") -> dict:
    """
    Fetches the contents of a given folder in a GitHub repository.
    Recursively fetches contents of subfolders to build a complete tree.
    """
    url = f"{BASE_URL}/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        contents = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching contents for {path}: {e}")
        return None

    folder_tree = {}
    for item in contents:
        name = item["name"]
        item_type = item["type"]

        if item_type == "dir":
            # Recursively get contents of subdirectories
            sub_folder_path = f"{path}/{name}" if path else name
            folder_tree[name] = get_github_folder_contents(owner, repo, sub_folder_path)
        elif item_type == "file":
            folder_tree[name] = "file"  # You can store more info here if needed
    return folder_tree


def print_folder_tree(
    tree: dict, indent: int = 0, prefix: str = "", is_last: bool = True
):
    """Prints the folder tree in an organized format using tree-style syntax."""
    items = list(tree.items())
    for i, (name, content) in enumerate(items):
        is_last_item = i == len(items) - 1

        # Choose the appropriate tree character
        if is_last_item:
            current_prefix = "└── "
            next_prefix = "    "
        else:
            current_prefix = "├── "
            next_prefix = "│   "

        if content == "file":
            print(f"{prefix}{current_prefix}{name}")
        else:
            print(f"{prefix}{current_prefix}{name}")
            print_folder_tree(content, indent + 1, prefix + next_prefix, is_last_item)


# --- Example Usage ---
if __name__ == "__main__":
    owner = "connorbell133"
    repo = "obsidian"
    target_folder = "meetings"  # Or "" for the root

    # Make sure to set your GITHUB_TOKEN environment variable
    if GITHUB_TOKEN:
        print(f"Listing contents of '{target_folder}' in '{owner}/{repo}':")
        repo_tree = get_github_folder_contents(owner, repo, target_folder)

        if repo_tree:
            print_folder_tree(repo_tree)
        else:
            print("Could not retrieve folder tree.")
    else:
        print(
            "GITHUB_TOKEN environment variable not set. Please set it before running."
        )
