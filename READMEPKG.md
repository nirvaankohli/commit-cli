# gitcommit-cli

Auto-generate meaningful git commit messages using AI-powered analysis of your staged changes.

## Features

* ✨ **AI-Powered**: Automatically generates commit messages- *no API key required* -via [Hackclub’s](https://hackclub.com/) free [AI API](https://ai.hackclub.com/) (exclusive to members).
* 📝 **Conventional Commits**: Follows the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/)
* 🔎 **Preview Mode**: *You stay in control*: preview every AI-generated commit message before it touches your repo.
* 🎨 **Beautiful CLI**: *Clean* ASCII art and *formatted* output(I like this part a lot)

## Installation

You can install **gitcommit-cli** with *pip* by running the following command:

```bash
pip install gitcommit-cli
```
## Quick Start

1. **Stage your changes** as usual:

    ```bash
    git add .
    ```
2. **Generate and commit** with AI:

    ```bash
    gitcommit-cli commit
    ```
3. **Review the generated message** and either commit or cancel

## Usage 

### Generate & Commit

```bash

# Interactive Mode - preview & confirm before commiting or canceling

gitcommit-cli commit

# Skip confirmation and commit directly

gitcommit-cli commit --skip-confirmation
```

### Generate Message Only 

```bash
# Just generate the message without committing

gitcommit-cli commit_msg
```

## Example Output

```bash

Analyzing staged changes...

The following is the commit message our CLI generated:

 | feat(cli): add AI-powered commit message generation
 | 
 | - Implemented automatic commit message generation using Hack Club AI
 | - Added support for conventional commits format
 | - Includes preview mode for user confirmation

Continue with the commit: (y/n)
```

## How it works

1. **Analyzes** your staged diff
2. **Sends** the diff to Hackclub AI for analysis
3. **Generates** a commit message message following best practices:
    * Conventional Commits format(`feat:`, `fix:`, etc.)
    * *Clear*, *concise* subject line (≤80 characters)
    * Descriptive body explaining what and why
4. **Formats** the output beautifully in your terminal

## Requirements

* Python 3.8+
* Git repository
* Internet connection (for AI analysis)
* `curl` command available in *PATH*

## Configuration

The tool works out of the box with no configuration needed. It uses:

* *AI Model*: `meta-llama/llama-4-maverick-17b-128e-instruct` via Hack Club AI
* **Commit Format**: Conventional Commits specification
* **Temperature**: 0.0 (deterministic output)

You can customize the AI model by setting the `HACKCLUB_MODEL` environment variable:

```bash

export HACKCLUB_MODEL="your-preferred-model"
gitcommit-cli commit
```
## Examples

### Feature Addition
```bash
$ git add new_feature.py
$ gitcommit-cli commit
```
Output: `feat(parser): add array support for configuration files`

### Bug Fix
```bash
$ git add bug_fix.py
$ gitcommit-cli commit
```
Output: `fix(auth): resolve token validation edge case`

### Documentation
```bash
$ git add README.md
$ gitcommit-cli commit
```
Output: `docs: update installation instructions and examples`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Use `gitcommit-cli` to generate your commit message! 😉 (see what I did)
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Credits

- Built with ❤️ by [Nirvaan](mailto:nirvaan@gmail.com)
- Powered by [Hackclub AI](https://ai.hackclub.com)
- Follows [Conventional Commits](https://www.conventionalcommits.org/) specification

---

*Make your commit messages meaningful without the mental overhead!*