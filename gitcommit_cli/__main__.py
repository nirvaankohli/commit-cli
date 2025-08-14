import argparse
import sys

# --- The Terminal Art ---

ASCII_BANNER = r"""
  _______  __  .___________.  ______   ______   .___  ___. .___  ___.  __  .___________.
 /  _____||  | |           | /      | /  __  \  |   \/   | |   \/   | |  | |           |
|  |  __  |  | `---|  |----`|  ,----'|  |  |  | |  \  /  | |  \  /  | |  | `---|  |----`
|  | |_ | |  |     |  |     |  |     |  |  |  | |  |\/|  | |  |\/|  | |  |     |  |     
|  |__| | |  |     |  |     |  `----.|  `--'  | |  |  |  | |  |  |  | |  |     |  |     
 \______| |__|     |__|      \______| \______/  |__|  |__| |__|  |__| |__|     |__|     
                                                                                        
          ______  __       __                                                           
         /      ||  |     |  |                                                          
 ______ |  ,----'|  |     |  |                                                          
|______||  |     |  |     |  |                                                          
        |  `----.|  `----.|  |                                                          
         \______||_______||__|                                                          
                                                                                        

"""

# --- Setup ---

def parse_args():
    
    parser = argparse.ArgumentParser(
        prog="gitcommit-cli",
        description=(
            "gitcommit-cli auto-generates git commit messages "
            "by analyzing staged diffs with ai.hackclub.com or an OpenAI key.\n"
            "Preview the generated message and commit in one smooth command."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True)


    commit_parser = subparsers.add_parser(

        "commit",
        help="Generate and apply commit directly with user conformation."

    )

    commit_parser.add_argument(
        "--skip-preview",
        action="store_true",
        help="Do not show commit message preview before committing."
    )


    commit_msg_parser = subparsers.add_parser(
        "commit_msg",
        help="Generate commit message without committing."
    )

    return parser.parse_args()

# --- Main CLI Entry ---

def main():

    print(ASCII_BANNER)

    args = parse_args()

    if args.command == "commit":

        if args.skip_preview:

            print("[Commit] Skipping confirmation, committing now")
        
        else:
            
            print("[Commit] Showing preview, awaiting confirmation")


    elif args.command == "commit_msg":

        print("[Commit Message] Generating commit message preview")


if __name__ == "__main__":
    main()
