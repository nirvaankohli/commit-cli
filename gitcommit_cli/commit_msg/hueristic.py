
import re
import subprocess
from pathlib import Path

CONVENTIONAL = {

    'feat' : ["add", "create", "implement", "introduce", "add feature"],
    'fix' : ['error', 'bug', 'issue', 'problem', 'fix', 'fail', 'wrong'],
    'docs' : ['doc', 'readme', 'comment'],
    'test': ['test', 'unittest', 'integration test', 'e2e test'],
    'chore': ['ci', 'config', 'setup', 'build', 'maintenance', 'deps', 'version'],

}

class hueristic:
    
    """
    
    A class to create heuristic commit messages based on the diff of a git commit.
    
    """

    def __init__(self):

        pass


    def generate_commit_message(self, diff: str) -> str:

        """
        
        Generate a commit message based on the provided diff.
        
        This method uses a simple heuristic to create a commit message by extracting the first line of the diff.
        
        Args:
            diff (str): The diff string from which to generate the commit message.
        
        Returns:
            str: A simple commit message derived from the diff.
        
     """

        stats = self.classify_files(diff)
        prefix = self.choose_prefix(stats)
        scope  = self.choose_scope(diff)

        # simple subject: “X insertions, Y deletions”

        subject = f"{stats['added']} insertions, {stats['deleted']} deletions"

        if scope:

            return f"{prefix}({scope}): {subject}"
        
        return f"{prefix}: {subject}"

    def classify_files(self, diff) -> dict:

        stats = {

            'added': 0,

            'deleted': 0,

            'modified': 0,

            'files': set(), 
            
            'keywords':set()
            
            }
        
        for line in diff.splitlines():

            if line.startswith('+++ ') or line.startswith('--- '):
                
                path = line[6:] if line.startswith('+++ b/') else line[6:] 
                
                stats['files'].add(Path(path).suffix)

            elif line.startswith('+') and not line.startswith('+++ '):
                
                stats['added'] += 1
                
            elif line.startswith('-') and not line.startswith('--- '):
                
                stats['deleted'] += 1

            for kw in ('TODO','FIXME','BUG'):

                if kw in line:

                    stats['keywords'].add(kw)
        
        return stats
    
    def choose_prefix(self, stats: dict) -> str:

        text = ' '.join(stats['keywords']).lower()

        for prefix, triggers in CONVENTIONAL.items():

            if any(w in text for w in triggers):

                return prefix
            
        # fallback

        total = stats['added'] + stats['deleted']

        if total > 200:

            return 'refactor'
        
        return 'chore'
    
    def choose_scope(self, diff):

        roots = {Path(p[6:]).parts[0] for p in diff.splitlines() if p.startswith('+++ b/')}

        return roots.pop() if len(roots) == 1 else ''


def get_staged_diff() -> str:

    """
    
    Get the staged diff of the current git repository.
    
    We do this by essentially running "git diff --staged --no-color" and returning the output.
    
    """
    
    result = subprocess.run(

            ["git", "diff", "--staged", "--no-color"],

            capture_output=True,

            text=True,

            encoding="utf-8",

            check = True

        )
    
    # DELETE IN DEPLOYMENT

    return result.stdout

if __name__ == "__main__":

    diff_example = get_staged_diff()   

    print("Diff Example:\n", diff_example)

    msgcli = hueristic()

    print(msgcli.generate_commit_message(diff_example))