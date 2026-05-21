---
description: Create a pull request with title, description, and branch management
---

# Create Pull Request

This command helps you create a pull request with proper formatting and branch management.

## What it does

1. Checks git status and current branch
2. Ensures you're not on main/master branch
3. Pushes current branch to remote
4. Creates PR using GitHub CLI
5. Opens PR in browser

## Execution

!git status
!git rev-parse --abbrev-ref HEAD
!gh pr create --web

## Usage

1. Make sure you have commits on a feature branch
2. Run `/pr-creation`
3. Follow the GitHub CLI prompts for:
   - PR title
   - PR description
   - Base branch
4. The PR will be created and opened in your browser

## Requirements

- GitHub CLI (`gh`) must be installed and authenticated
- You must be on a branch other than main/master
- Remote repository must be configured

## Example Workflow

```bash
# Make changes and commit
git checkout -b feature/new-feature
git add .
git commit -m "feat: add new feature"

# Create PR
/pr-creation
```

## Tips

- Write clear, descriptive PR titles
- Include context in PR description
- Reference related issues with #issue-number
- Request reviewers if needed
