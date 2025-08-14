import argparse
import sys

# --- The Terminal Art --

ASCII_BANNER = r"""
  _______  __  .___________.          ______   ______   .___  ___. .___  ___.  __  .___________.  ______  __       __  
 /  _____||  | |           |         /      | /  __  \  |   \/   | |   \/   | |  | |           | /      ||  |     |  | 
|  |  __  |  | `---|  |----` ______ |  ,----'|  |  |  | |  \  /  | |  \  /  | |  | `---|  |----`|  ,----'|  |     |  | 
|  | |_ | |  |     |  |     |______||  |     |  |  |  | |  |\/|  | |  |\/|  | |  |     |  |     |  |     |  |     |  | 
|  |__| | |  |     |  |             |  `----.|  `--'  | |  |  |  | |  |  |  | |  |     |  |     |  `----.|  `----.|  | 
 \______| |__|     |__|              \______| \______/  |__|  |__| |__|  |__| |__|     |__|      \______||_______||__| 
                                                                                                                       
"""

# -- Setup --

def parse_args():

    parser = argparse.ArgumentParser(
        
        prog="gitcommit-cli", 
        description = "gitcommit-cli is a CLI tool that auto-generates git commit messages by analyzing staged diffs with ai.hackclub.com or, if provided, an OpenAI key with ChatGPT. Preview the generated message and, in one smooth command, run git commit. Standardized style reduces friction, keeping your workflow focused and history clean.", 
        formatter_class=argparse.RawTextHelpFormatter
        
    )



    return parser.parse_args()

# --- Main CLI Entry ---

def main():

    print(ASCII_BANNER)
    args = parse_args()

if __name__ == "__main__":
    main()