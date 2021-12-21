import git
from pathlib import Path

class Grepo(git.Repo):
    def __init__(self) -> None:
        super().__init__()
        
    def path():
        file_path = Path(__file__).resolve()
        repo = git.Repo(file_path,search_parent_directories=True)
        return Path(repo.working_tree_dir).resolve()

if __name__ == '__main__':
    grepo = Grepo.path()
    print(grepo)