from __future__ import annotations

import os
import sys
import re
import json
import shutil
import subprocess
from textwrap import dedent
from typing import Optional

# I made the prompt myself, put it into a custom GPT that specializes with prompt engineering, and then edited myself.

SYSPROMPT = dedent(

    """\
    
    Follow these guidelines to generate a high-quality commit message:

        * **Subject (summary):** imperative present, LESS THAN 80 chars, capitalize first word, no period. They should not be cut off.
        
        * **Body (optional):** blank line after subject; wrap ~200 chars; explain **what** + **why** (not how); add key context/side effects.
        
        * **Types (optional):** use Conventional Commits (`feat:`, `fix:`, etc.) with optional scope, e.g., `feat(parser): add array support`. Make sure to use the correct type for the commit message THESE ARE IMPORTANT.
        
        * **Atomic commits:** one purpose per commit; reference issue IDs, but don’t rely on them to explain intent.
        
        * **Think future:** messages should help teammates trace **why** a change happened and ease reviews/debugging.
        
        * **Footers:** issues, reviewers, breaking changes, etc.

        **Conventional Commits spec:** https://www.conventionalcommits.org/en/v1.0.0/

        * **Purpose:** generate a concise, clear commit message based on the provided git diff. People should be able to tell what code was changed without opening the code and instead reading the commit message.

    **Template**

    ```

    ## <type>(<scope>): <Short imperative summary – less or equal to 80 chars>

    <Optional body ~200 chars>
    
    - Explain why this change is needed
    
    - Note side effects/context

    Issues: #123 (if applicable)
    Reviewed-by: Alice (if applicable)

    Example:

    ## feat(parser): add array support

    * Added support for parsing arrays in the configuration file.

    * This change allows users to define arrays in their config files, improving flexibility.

    * This is a breaking change as it changes the way arrays are handled in the parser.


    ```

    """

).strip()


class llm:

    """

        A class to create commit messages using the Hack Club AI chat completions
        endpoint (no API key required). Local model usage has been removed.
    
    """

    def __init__(self):

        self._have_curl = shutil.which("curl") is not None

    def build_prompt(
            
            self, 
            
            diff: str, 
            
            project_context: Optional[str] = None
                    
            ):
        
        ctx = f"\n\nProject context:\n{project_context}" if project_context else ""
        
        return dedent(

            f"""\

            {ctx}

            The Git Diff you must summarize: SUMMARIZE THE FOLLOWING DIFF AND GENERATE A COMMIT MESSAGE BASED ON IT. DO NOT EXPLAIN YOURSELF OR ADD ANYTHING ELSE. DO NOT USE CODE FENCES OR MARKDOWN. DO NOT ADD ANYTHING ELSE OUTSIDE OF THE COMMIT MESSAGE. DO NOT ADD ANYTHING ELSE OUTSIDE OF THE COMMIT MESSAGE. DO NOT ADD ANYTHING ELSE OUTSIDE OF THE COMMIT MESSAGE.

            ---

            {diff.strip()}

            ---
                
            You must return ONLY the commit message, nothing else.
            Enclose your entire output strictly between these markers:

            <<<COMMIT>>>

            <commit message only>

            <<<END>>>

            It must follow the Conventional Commits spec.
            
            """
        
        ).strip()

    def _trim_diff(
            
            self, 
            
            diff: str, 
            
            max_chars: int = 3000
            
            ) -> str:
        
        """
        
        Fast guardrail for very large diffs. Kept smaller for speed.
        
        """
        
        d = diff.strip()
        
        if len(d) <= max_chars:
        
            return d
        
        head = d[: max_chars // 2]
        tail = d[-(max_chars // 2) :]
        
        return head + "\n...\n[diff truncated]\n...\n" + tail

    def _extract_commit(self, text: str) -> str:
        
        """
        
        Sanitize/normalize LLM output to ensure ONLY a commit message is returned.
        
        """
        t = text.strip()


        if "<<<COMMIT>>>" in t and "<<<END>>>" in t:
            t = t.split("<<<COMMIT>>>", 1)[1].split("<<<END>>>", 1)[0].strip()


        t = t.replace("```", "").strip()
        lines = []
        for ln in t.splitlines():

            s = ln.strip()

            if not s:

                lines.append("")

                continue

            if s.startswith(("---", "diff --git", "index ")):

                continue

            if s.lower().startswith(("here's a high-quality", "here is a high-quality", "here’s a high-quality")):

                continue

            if s.lower().startswith(("<<<COMMIT>>>", "<<<END>>>")) or "<<<COMMIT>>>" in s or "<<<END>>>" in s:

                continue
            
            lines.append(ln)

        t = "\n".join(lines).strip()


        cc_re = re.compile(r"^(feat|fix|chore|refactor|docs|test|perf|style|build|ci|revert)(\([^)]+\))?:\s.+", re.IGNORECASE)
        first_valid = None

        for ln in t.splitlines():
            if cc_re.match(ln.strip()):
                first_valid = ln.strip()
                break

        if first_valid is None:

            parts = [p for p in t.splitlines() if p.strip()]
            subject = parts[0].strip() if parts else "chore: update"
            body = "\n".join(p.rstrip() for p in parts[1:]).strip()
        else:

            before, _, after = t.partition(first_valid)
            subject = first_valid
            body = after.split("\n", 1)[1].strip() if "\n" in after else ""


        subject = subject.strip()
        body = "\n".join(line.rstrip() for line in body.splitlines()).strip()

        return f"{subject}\n\n{body}" if body else subject

    def _generate_remote(
            
            self,
            
            prompt: str,
            
            max_tokens: int,
            
            temperature: float
    
    ) -> str:
        
        """
        
        Use Hack Club AI (no key required) via curl for fast generation. 
        
        """

        if not self._have_curl:

            return "chore: update (curl not available)"

        model_name = os.getenv(
            "HACKCLUB_MODEL",
            "meta-llama/llama-4-maverick-17b-128e-instruct"
        )

        payload = {
            "messages": [
                {"role": "system", "content": SYSPROMPT},
                {"role": "user", "content": prompt},
            ],
            "model": model_name,
            "max_tokens": max(48, min(max_tokens, 96)),
            "temperature": max(0.0, float(temperature)),
            "stop": ["<<<END>>>"],
        }

        try:

            cmd = [
                "curl",
                "-sS",
                "-X", "POST",
                "https://ai.hackclub.com/chat/completions",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(payload),
            ]

            out = subprocess.run(cmd, check=True, capture_output=True, text=True)
            data = json.loads(out.stdout)
            msg = data["choices"][0]["message"]["content"]

            return self._extract_commit(msg)
        
        except Exception:
            return "chore: update (remote generation failed)"

    def generate_commit_message(
            
        self,
        
        diff,
        
        max_tokens: int = 120,
        
        temperature: float = 0.0,
        
        project_context: Optional[str] = None,
    
    ) -> str:
        
        """
        
        Generate a commit message based on the provided diff using the
        Hack Club AI endpoint only.
        
        """

        if not diff:

            return("chore: update (no staged changes)")
        
        diff = str(diff)

        fast_diff = self._trim_diff(diff) 
        prompt = self.build_prompt(fast_diff, project_context)

        return self._generate_remote(prompt, max_tokens, temperature)


def get_staged_diff() -> str:

    """

    Reads staged changes with minimal context for speed and smaller prompts.
    
    """

    out = subprocess.check_output(

        ["git", "diff", "--staged", "--no-color", "-U0", "--diff-algorithm=patience"]
    
    )

    return out.decode("utf-8", errors="replace").strip()


if __name__ == "__main__":

    diff = get_staged_diff()

    if not diff:

        print("chore: update (no staged changes)")
    
    else:

        model = llm()
        commit_message = model.generate_commit_message(diff)
        print(commit_message)
