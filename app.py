import utils

if __name__ == "__main__":
    repo_local_path = "/Users/reza/projects/workforce/pf-config"
    file_changes = utils.git_changes(repo_local_path, branch="main", commit_depth=1)
    for f in file_changes:
        print(f"status: {f['status']}, file: {f['file']}" )
