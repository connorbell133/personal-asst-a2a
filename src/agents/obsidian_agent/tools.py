"""Tools module."""

import base64
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
        response = requests.get(url, headers=headers, timeout=10)
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


def get_github_file_contents(owner: str, repo: str, path: str) -> dict:
    """
    Fetches the contents of a given file in a GitHub repository.
    """

    # check if the file is a markdown file
    if not path.endswith(".md"):
        return {
            "success": False,
            "error": "File is not a markdown file.",
        }

    # get the file contents
    url = f"{BASE_URL}/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # load contents from  the content base64 encoded
    return {
        "success": True,
        "file_contents": base64.b64decode(response.json()["content"]).decode("utf-8"),
    }


def print_folder_tree(tree, indent=0, prefix="", is_last_item=True):
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


def send_new_content_to_github(
    note_path: str, content: str, owner: str, repo: str
) -> dict:
    """Send the new content to github."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{note_path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = {
        "message": "my commit message",
        "committer": {"name": "Monalisa Octocat", "email": "octocat@github.com"},
        "content": base64.b64encode(content.encode()).decode(),
    }
    response = requests.put(url, headers=headers, json=data, timeout=10)
    return response.json()


def delete_note_from_github(note_path: str, owner: str, repo: str) -> dict:
    """Delete the given note from github."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{note_path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    response = requests.delete(url, headers=headers, timeout=10)
    return response.json()
