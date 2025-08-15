import subprocess

class DiffReader:
    
    def __init__(self):
        
        pass


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
            
            check=True

        )
        
        return result

if __name__ == "__main__":
    
    print(DiffReader.get_staged_diff())