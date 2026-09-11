import subprocess
import os

def _project_root():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

def fossil_commit(message: str, path: str):
    repo_root = _project_root()
    rel_path = os.path.relpath(path, repo_root)

    # Add new/changed files (no --clean needed)
    subprocess.run(
        ["fossil", "add", "--force", rel_path],
        cwd=repo_root,
        check=True
    )

    # Commit and capture hash
    result = subprocess.run(
        ["fossil", "commit", "-m", message],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True
    )

    # Extract commit hash from "New_Version: abc1234 ..." output
    for line in result.stdout.splitlines():
        if line.startswith("New_Version:"):
            commit_hash = line.split()[1]
            break
    else:
        raise ValueError("Could not parse commit hash from fossil output")
    
    return commit_hash
