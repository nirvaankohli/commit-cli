
import subprocess

def get_staged_diff() -> str:

    """

    Get the staged diff of the current git repository.

    We do this by essentially running "git diff --staged --no-color" and returning the output.

    """

    result = subprocess.run(

        ["git", "diff", "--staged", "--no-color"],

        capture_output=True,

        text=True,

        check = True

    )

    return result.stdout

if __name__ == "__main__":

    # TEST: GET RID OF IN DEPLOYMENT

    print(get_staged_diff())