import re 
from diff_reader import DiffReader
from commit_msg.hueristic import hueristic

def generate_commit_message(diff: str, llm_use: bool = False, openai_use: bool = False) -> str:

    llm_use = False
    openai_use = False

    if openai_use:

        pass

    elif llm_use:

        pass

    else:

        msgcli = hueristic()

        return msgcli.generate_commit_message(diff)




        
