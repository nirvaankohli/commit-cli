import argparse
import sys
from gitcommit_cli.hackclubai import llm
from gitcommit_cli.diff_reader import DiffReader
import subprocess
import time

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

# --- Formatting ---

def display_commit_message(message_lines):

    formatted = """
    
    The following is the commit message our CLI generated:

"""

    for line in message_lines.split('\n'):

        formatted += (f" | {line} \n")

    return formatted


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

        help="Generate and apply commit directly with user confirmation."

    )

    commit_parser.add_argument(

        "--skip-confirmation",

        action="store_true",

        help="Do not show commit message preview before committing."
    
    )


    commit_msg_parser = subparsers.add_parser(

        "commit_msg",

        help="Generate commit message without committing."

    )

    return parser.parse_args()

def commit(skip_confirmation:bool = False ):

    print("Analyzing staged changes...")

    ai_client = llm()

    commit_msg = ai_client.generate_commit_message(
        
        diff=DiffReader.get_staged_diff(),

        max_tokens=350
        
        )
    
    print(display_commit_message(commit_msg))

    if not skip_confirmation:

        approve = input("Continue with the commit: (y/n) ")

        if approve.lower() == "y":

            print("\n Continuing with the commit...")

            subprocess.run(


                ["git", "commit", "-m", commit_msg]

            )

            print("\n Commit Completed!")
                  
        else:
        
            print("\n Canceling..")



    else:

        time.sleep(1.25)

        print("\n Continuing with the commit...")

        subprocess.run(


            ["git", "commit", "-m", commit_msg]

        )

        print("\n Commit Completed!") 

def commit_message():

    print("Analyzing staged changes...")

    ai_client = llm()

    commit_msg = ai_client.generate_commit_message(
        
        diff=DiffReader.get_staged_diff(),

        max_tokens=350
        
        )

    print(f"""

\n

The following is the commit message our CLI generated: (Copy Pastable)
          
{commit_msg}
          
          """)


        

# --- Main CLI Entry ---

def main():

    print(ASCII_BANNER)

    args = parse_args()

    if args.command == "commit":

        if args.skip_confirmation:

            commit
        
        else:

            commit()


    elif args.command == "commit_msg":

        commit_message()


if __name__ == "__main__":
    main()
