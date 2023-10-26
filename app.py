import os.path

from git import Repo
import logging

DIFF_HEADER = 'change_type,a_mode,a_blob,file,a_rawpath,new_file,deleted_file,copied_file,' \
              'raw_rename_from,raw_rename_to,diff,score'


# Literal["A: Added", "D: Deleted", "C: Copied", "M: Modified", "R: Rename", "T: Do Nothing", "U: Undefind"]

def get_git_diff(repo_path):
    if repo_local_path == None or len(repo_local_path) == 0:
        logging.error('Please update repo_local_path variable to your local git rpeo and run the code')
        exit(-1)

    # init repo
    repo = Repo(repo_local_path)

    commits = list(repo.iter_commits(all=True))  # only the last 2 commits

    if len(commits) == 0 or len(commits) == 1:
        logging.info("No previous change detected.")
        exit(0)

    diffs = None

    # when there is a pull request merge from feature branch to Main/Master branch
    if len(commits[0].parents) > 1:
        current_commit = repo.commit(commits[0].parents[0])
        last_commit = repo.commit(commits[0].parents[1])
        logging.info(f"Comparing Hash with '{commits[0]}' with '{commits[1]}'")
        diffs = last_commit.diff(current_commit)

    else:
        current_commit = repo.commit(commits[0])
        last_commit = repo.commit(commits[1])
        logging.info(f"Comparing Hash with '{commits[1]}' with '{commits[0]}'")
        diffs = last_commit.diff(current_commit)

    results = list()

    logging.debug(DIFF_HEADER)
    for diff in diffs:
        diff_a_path = None
        diff_a_rawpath = None
        diff_raw_rename_from = None
        diff_raw_rename_to = None

        if diff.a_path is not None:
            diff_a_path = f"{repo_local_path}/{diff.a_path}"
        if diff.a_rawpath is not None:
            diff_a_rawpath = f"{repo_local_path}/{diff.a_rawpath.decode('utf-8')}"
        if diff.raw_rename_from is not None:
            diff_raw_rename_from = f"{repo_local_path}/{diff.raw_rename_from.decode('utf-8')}"
        if diff.raw_rename_to is not None:
            diff_raw_rename_to = f"{repo_local_path}/{diff.raw_rename_to.decode('utf-8')}"
        results.append({
            "file": diff_a_path,
            "os_path_exists": os.path.exists(diff_a_path),
            "change_type": diff.change_type,
            "is_new_file": diff.new_file,
            "is_deleted_file": diff.deleted_file,
            "is_copied_file": diff.copied_file,
            "renamed_from": diff_raw_rename_from,
            "rename_to": diff_raw_rename_to
        })
        logging.debug(
            f"{diff.change_type},{diff.a_mode},{diff.a_blob},{diff_a_path},{diff_a_rawpath},{diff.new_file}"
            f"{diff.deleted_file},{diff.copied_file},{diff_raw_rename_from},{diff_raw_rename_to},{diff.diff},"
            f"{diff.score}")

    return results


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    repo_local_path = "/Users/reza/projects/workforce/pf-config2"

    # List of Diff Entries
    git_diffs = get_git_diff(repo_local_path)

    print(git_diffs)
