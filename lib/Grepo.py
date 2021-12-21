import git
from pathlib import Path
file_path = Path(__file__).resolve()

class Grepo(git.Repo):
    def __init__(self) -> None:
        super().__init__()
        self.repository = git.Repo(file_path,search_parent_directories=True)
        self.origin = self.repository.remote('origin')
        self.ERROR = 128
        self.FAST_FORWARD = 64
        self.HEAD_UPTODATE = 4

        
    def path():
        rep = git.Repo(file_path,search_parent_directories=True)
        return Path(rep.working_tree_dir).resolve()
    
    def hasUpdate(self):
        flag = self.origin.fetch()[0].flags
        return flag
    
    def pull(self):
        self.repository.head.reset('HEAD~1', index=True, working_tree=True)
        self.origin.pull()
        
        
if __name__ == '__main__':
    grepo = Grepo()
    print(grepo.ERROR)