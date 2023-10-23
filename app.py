from git import Repo

DIFF_HEADER = 'change_type,a_mode,a_blob,file,a_rawpath,new_file,deleted_file,copied_file,' \
              'raw_rename_from,raw_rename_to,diff,score'

if __name__ == '__main__':
    repo_local_path = "/Users/reza/projects/workforce/pf-config2"

    if repo_local_path == None or len(repo_local_path) == 0:
        print("ERROR: Please update repo_local_path variable to your local git rpeo and run the code")
        exit(-1)

    # init repo
    repo = Repo(repo_local_path)

    commits = list(repo.iter_commits(all=True)) # only the last 2 commits

    if len(commits) == 0 or len(commits) == 1:
        print("INFO: No previous change detected.")
        exit(0)

    diffs = None

    if len(commits[0].parents) > 1:
        current_commit = repo.commit(commits[0].parents[0])
        last_commit = repo.commit(commits[0].parents[1])
        print(f"INFO: Comparing Hash with '{commits[0]}' with '{commits[1]}'")
        diffs = last_commit.diff(current_commit)

    else:
        print(f"INFO: Comparing Head with '{commits[1]}'")
        diffs = repo.head.commit.diff(commits[1])

    print(DIFF_HEADER)
    for d in diffs:
        if d.change_type != "R":
            print(d.change_type, ",",
                  d.a_mode, ",",
                  d.a_blob, ",",
                  d.a_path, ",",
                  d.a_rawpath, ",",
                  d.new_file, ",",
                  d.deleted_file, ",",
                  d.copied_file, ",",
                  d.raw_rename_from, ",",
                  d.raw_rename_to, ",",
                  d.diff, ",",
                  d.score)
