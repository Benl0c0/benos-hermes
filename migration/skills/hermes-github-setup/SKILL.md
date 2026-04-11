---
name: hermes-github-setup
description: Set up GitHub access on Ben's WSL2/Ubuntu environment. Covers gh CLI install, token login, and the critical git push fix for WSL where credential helpers fail.
author: Hermes Agent
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [github, wsl, setup, git, push, auth]
    related_skills: [github-auth, benos-setup]
---

# GitHub Setup on WSL2

## Problem

On Ben's WSL2 environment, `gh auth login --with-token` succeeds, but `git push origin master` fails with:
```
fatal: could not read Username for 'https://github.com': No such device or address
```

This happens despite `gh auth status` showing "Logged in". The Git credential helper chain in WSL cannot access the token stored at `~/.config/gh/hosts.yml`.

## Solution

Store the Personal Access Token locally and use it directly in the push URL.

### Step 1: Install gh CLI
```bash
sudo apt-get install gh -y
```

### Step 2: Store the Token
Save the token to a file for reuse across sessions:
```bash
echo "ghp_YOUR_TOKEN_HERE" > ~/.hermes/github_token.txt
chmod 600 ~/.hermes/github_token.txt
```

### Step 3: Login to gh
```bash
cat ~/.hermes/github_token.txt | gh auth login --with-token
```
Verify with `gh auth status`.

### Step 4: Push via URL (Critical Fix)
**DO NOT** use `git push origin master`. Instead:
```bash
TOKEN=$(cat ~/.hermes/github_token.txt)
cd ~/benos
git push https://x-access-token:${TOKEN}@github.com/Benl0c0/benos-hermes.git HEAD:master
```

### Step 5: Create Remote Repo
```bash
gh repo create Benl0c0/benos-hermes --public --description "BEN//OS Hermes Agent System"
```

### Verification
```bash
gh repo view Benl0c0/benos-hermes
gh auth status
```

## Pitfalls
- `git remote set-url` with token in URL: Git will store the URL in `.git/config`. Reset to clean URL after push: `git remote set-url origin https://github.com/Benl0c0/benos-hermes.git`
- Token permissions: Fine-grained PAT needs `Contents: Read & Write` at minimum. Classic PAT needs `repo` scope.
- WSL credential store is unreliable – always use URL-based auth or set up `git config --global credential.helper store`.
