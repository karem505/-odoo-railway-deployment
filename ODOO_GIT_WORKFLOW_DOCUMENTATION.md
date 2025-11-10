# 🚀 Odoo AWS Git Workflow Documentation

**Project**: Odoo 18 Development
**Repository**: https://github.com/karem505/API-for-odoo (Private)
**Server**: AWS EC2 (eu-north-1)
**Last Updated**: October 23, 2025

---

## 📋 Table of Contents

1. [Server Information](#server-information)
2. [Repository Structure](#repository-structure)
3. [Git Configuration](#git-configuration)
4. [Team Workflow](#team-workflow)
5. [Developer Setup](#developer-setup)
6. [Daily Development Workflow](#daily-development-workflow)
7. [Deployment Process](#deployment-process)
8. [Git Commands Reference](#git-commands-reference)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## 🖥️ Server Information

### AWS EC2 Instance Details

| Property | Value |
|----------|-------|
| **Instance ID** | `i-034ca3b1f4e02393a` |
| **Public IP** | `56.228.2.47` |
| **Public DNS** | `ec2-56-228-2-47.eu-north-1.compute.amazonaws.com` |
| **Region** | `eu-north-1` (Stockholm) |
| **OS** | Amazon Linux 2023 |
| **Python Version** | 3.11.13 |
| **PostgreSQL Version** | 15.14 |

### SSH Access

```bash
ssh -i "MyTestApp-KeyPair.pem" ec2-user@ec2-56-228-2-47.eu-north-1.compute.amazonaws.com
```

**Key File Location**: `C:\Users\Al Saad Nasr City\Downloads\MyTestApp-KeyPair.pem`

### Odoo Configuration

| Property | Value |
|----------|-------|
| **Odoo Version** | 18.0 (Latest) |
| **Installation Path** | `/home/ec2-user/odoo18` |
| **Config File** | `/home/ec2-user/.odoo/odoo.conf` |
| **Log File** | `/home/ec2-user/.odoo/odoo-server.log` |
| **Database Name** | `odoo18` |
| **Web Access** | `http://56.228.2.47:8069` |
| **Master Password** | `admin123` |
| **Service Name** | `odoo.service` |

### Useful Server Commands

```bash
# Check Odoo status
sudo systemctl status odoo

# Restart Odoo
sudo systemctl restart odoo

# Stop Odoo
sudo systemctl stop odoo

# Start Odoo
sudo systemctl start odoo

# View logs in real-time
tail -f /home/ec2-user/.odoo/odoo-server.log

# View last 100 lines of logs
tail -n 100 /home/ec2-user/.odoo/odoo-server.log
```

---

## 📂 Repository Structure

### GitHub Repository

**Main Repository**: https://github.com/karem505/API-for-odoo (Private)
**Upstream**: https://github.com/odoo/odoo (Official Odoo)

### Branch Strategy

```
karem505/API-for-odoo (Private Repository)
├── 18.0 (production/stable)
│   └── Base Odoo 18.0 installation
│
└── development (active development)
    ├── feature/module-name
    ├── feature/custom-reports
    ├── fix/bug-description
    └── update/improvement-name
```

### Remote Repositories

```bash
origin   → https://github.com/karem505/API-for-odoo.git (Private team repository)
upstream → https://github.com/odoo/odoo.git (Official Odoo)
```

**Purpose**:
- **origin**: Your team's private repository where you push changes
- **upstream**: Official Odoo repository for getting updates

---

## ⚙️ Git Configuration

### Current Git Setup on Server

```bash
# Location
cd /home/ec2-user/odoo18

# Git user configuration
user.name=karem505
user.email=karem505@users.noreply.github.com

# Remote configuration
origin: https://ghp_TOKEN@github.com/karem505/API-for-odoo.git
upstream: https://github.com/odoo/odoo.git

# Current branch
development
```

### Authentication

- **Method**: GitHub Personal Access Token (PAT)
- **Token Format**: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Token Expiration**: Check GitHub settings
- **Scopes**: `repo`, `workflow`

**To regenerate token**:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy token and update on server:
   ```bash
   cd /home/ec2-user/odoo18
   git remote set-url origin https://NEW_TOKEN@github.com/karem505/API-for-odoo.git
   ```

---

## 👥 Team Workflow

### Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         DEVELOPMENT CYCLE                        │
└─────────────────────────────────────────────────────────────────┘

1. Developer pulls latest 'development' branch
         ↓
2. Creates feature branch (feature/name)
         ↓
3. Writes code & tests locally
         ↓
4. Commits changes with descriptive message
         ↓
5. Pushes feature branch to GitHub
         ↓
6. Creates Pull Request on GitHub
         ↓
7. Code review by team
         ↓
8. Merge into 'development' branch
         ↓
9. Deploy to AWS server
         ↓
10. Test on production URL
```

### Branch Naming Conventions

| Type | Format | Example | Purpose |
|------|--------|---------|---------|
| Feature | `feature/description` | `feature/customer-portal` | New functionality |
| Bug Fix | `fix/description` | `fix/invoice-calculation` | Bug fixes |
| Update | `update/description` | `update/performance-optimization` | Improvements |
| Documentation | `docs/description` | `docs/api-documentation` | Documentation only |
| Hotfix | `hotfix/description` | `hotfix/critical-security-patch` | Urgent fixes |

### Commit Message Format

Use clear, descriptive commit messages with prefixes:

```bash
feat: add customer portal with authentication
fix: resolve invoice calculation rounding error
update: improve product search query performance
docs: add API documentation for custom endpoints
config: update database connection pool settings
refactor: reorganize sales module structure
test: add unit tests for payment processing
```

**Format**: `<type>: <description>`

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `update` - Update existing feature
- `docs` - Documentation
- `config` - Configuration changes
- `refactor` - Code refactoring
- `test` - Adding tests
- `chore` - Maintenance tasks

---

## 🛠️ Developer Setup

### Prerequisites

1. **VS Code** installed
2. **Remote - SSH** extension installed
3. **SSH Key file** (MyTestApp-KeyPair.pem)
4. **Git** basic knowledge

### Step 1: Install VS Code Extensions

1. Open **VS Code**
2. Press `Ctrl+Shift+X` (Extensions)
3. Install:
   - **Remote - SSH** (by Microsoft)
   - **Python** (by Microsoft)
   - **GitLens** (optional, for Git visualization)

### Step 2: Configure SSH Connection

#### Method A: VS Code GUI

1. Press `F1` or `Ctrl+Shift+P`
2. Type: `Remote-SSH: Connect to Host...`
3. Click `+ Add New SSH Host...`
4. Enter:
   ```
   ssh -i "path/to/MyTestApp-KeyPair.pem" ec2-user@ec2-56-228-2-47.eu-north-1.compute.amazonaws.com
   ```
5. Select SSH config file to update
6. Click **"Connect"**

#### Method B: Manual SSH Config

**Windows**: `C:\Users\USERNAME\.ssh\config`
**Linux/Mac**: `~/.ssh/config`

Add this configuration:

```ssh-config
Host odoo-aws
    HostName ec2-56-228-2-47.eu-north-1.compute.amazonaws.com
    User ec2-user
    IdentityFile C:\path\to\MyTestApp-KeyPair.pem
    StrictHostKeyChecking no
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Then connect**:
1. Press `F1` → `Remote-SSH: Connect to Host...`
2. Select `odoo-aws`

### Step 3: Open Odoo Project

1. Once connected, click **"Open Folder"**
2. Navigate to: `/home/ec2-user/odoo18`
3. Click **OK**
4. VS Code will reload with the Odoo project

### Step 4: Test Connection

Open terminal in VS Code (`Ctrl+~`) and run:

```bash
pwd
# Should output: /home/ec2-user/odoo18

git status
# Should output: On branch development

python3.11 --version
# Should output: Python 3.11.13
```

---

## 💻 Daily Development Workflow

### Scenario 1: Starting New Feature

```bash
# 1. Navigate to project
cd /home/ec2-user/odoo18

# 2. Make sure you're on development branch
git checkout development

# 3. Get latest changes from GitHub
git pull origin development

# 4. Create feature branch
git checkout -b feature/add-inventory-module

# 5. Verify you're on the new branch
git branch
# Output should show: * feature/add-inventory-module

# 6. Start coding in VS Code...
```

### Scenario 2: Making Changes and Testing

```bash
# After editing files in VS Code...

# 1. Check what files changed
git status

# 2. View specific changes
git diff filename.py

# 3. Restart Odoo to test changes
sudo systemctl restart odoo

# 4. Monitor logs for errors
tail -f /home/ec2-user/.odoo/odoo-server.log
# Press Ctrl+C to stop watching

# 5. Test in browser
# Open: http://56.228.2.47:8069
```

### Scenario 3: Committing Changes

```bash
# 1. Stage all changes
git add .

# Or stage specific files
git add addons/custom_module/models/product.py
git add addons/custom_module/__manifest__.py

# 2. Check what will be committed
git status

# 3. Commit with descriptive message
git commit -m "feat: add inventory tracking module with barcode scanning"

# 4. Push to GitHub
git push origin feature/add-inventory-module

# If first time pushing this branch, Git will suggest:
git push --set-upstream origin feature/add-inventory-module
```

### Scenario 4: Creating Pull Request

1. **Go to GitHub**: https://github.com/karem505/odoo
2. **GitHub will show**: "Compare & pull request" button - click it
3. **Fill in PR details**:
   - **Title**: `Add inventory tracking module`
   - **Description**:
     ```markdown
     ## Changes
     - Added inventory tracking module
     - Implemented barcode scanning functionality
     - Added product location management

     ## Testing
     - Tested barcode scanning with 10+ products
     - Verified location updates in database
     - Checked inventory reports

     ## Screenshots
     [Add screenshots if helpful]
     ```
4. **Request reviewers**: Select team members
5. **Click**: "Create pull request"

### Scenario 5: After PR is Approved

```bash
# 1. Switch back to development branch
git checkout development

# 2. Pull the merged changes
git pull origin development

# 3. Restart Odoo with new changes
sudo systemctl restart odoo

# 4. Verify no errors
tail -n 50 /home/ec2-user/.odoo/odoo-server.log

# 5. Test in browser
# http://56.228.2.47:8069

# 6. Delete local feature branch (cleanup)
git branch -d feature/add-inventory-module
```

### Scenario 6: Multiple Developers Working

**Developer A** working on inventory:
```bash
git checkout -b feature/inventory-tracking
# ... make changes ...
git push origin feature/inventory-tracking
```

**Developer B** working on reports:
```bash
git checkout -b feature/custom-reports
# ... make changes ...
git push origin feature/custom-reports
```

**Both can work simultaneously!** Merge PRs one at a time.

---

## 🚀 Deployment Process

### Standard Deployment (After PR Merge)

```bash
# 1. SSH to server
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47

# 2. Navigate to project
cd /home/ec2-user/odoo18

# 3. Check current branch
git branch
# Should show: * development

# 4. Pull latest changes
git pull origin development

# 5. Check what changed
git log --oneline -5

# 6. Restart Odoo service
sudo systemctl restart odoo

# 7. Check service status
sudo systemctl status odoo
# Should show: active (running)

# 8. Monitor logs for errors
tail -f /home/ec2-user/.odoo/odoo-server.log
# Watch for any ERROR or CRITICAL messages
# Press Ctrl+C when satisfied

# 9. Test in browser
# http://56.228.2.47:8069

# 10. Verify database migrations (if any)
# Check Odoo UI → Settings → Technical → Database Structure
```

### Emergency Rollback

If deployment causes issues:

```bash
# 1. Check recent commits
git log --oneline -10

# 2. Find the last working commit (e.g., abc1234)
# 3. Revert to that commit
git reset --hard abc1234

# 4. Restart Odoo
sudo systemctl restart odoo

# 5. Verify it works
tail -f /home/ec2-user/.odoo/odoo-server.log

# 6. Force push to GitHub (CAREFUL!)
git push origin development --force

# Note: Inform team before force pushing!
```

### Database Backup Before Deployment

```bash
# Backup database before major deployment
sudo -u postgres pg_dump odoo18 > /tmp/odoo18_backup_$(date +%Y%m%d_%H%M%S).sql

# List backups
ls -lh /tmp/odoo18_backup_*

# Restore if needed
sudo -u postgres psql odoo18 < /tmp/odoo18_backup_YYYYMMDD_HHMMSS.sql
```

---

## 📖 Git Commands Reference

### Basic Commands

```bash
# Check repository status
git status

# View commit history
git log
git log --oneline -10          # Last 10 commits, compact
git log --graph --all          # Visual branch graph

# View changes
git diff                       # Uncommitted changes
git diff filename              # Changes in specific file
git diff HEAD~1                # Compare with previous commit

# View remote repositories
git remote -v

# View branches
git branch                     # Local branches
git branch -a                  # All branches (local + remote)
git branch -r                  # Remote branches only
```

### Branch Operations

```bash
# Create new branch
git branch feature/new-feature

# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout development
git checkout 18.0

# Delete branch (local)
git branch -d feature/old-feature      # Safe delete (only if merged)
git branch -D feature/old-feature      # Force delete

# Delete remote branch
git push origin --delete feature/old-feature

# Rename current branch
git branch -m new-branch-name
```

### Staging and Committing

```bash
# Stage files
git add filename                # Stage specific file
git add .                       # Stage all changes
git add *.py                    # Stage all Python files
git add addons/custom_module/   # Stage entire directory

# Unstage files
git reset filename              # Unstage specific file
git reset                       # Unstage all

# Commit changes
git commit -m "commit message"
git commit -m "feat: add feature" -m "Additional description here"

# Amend last commit (change message or add files)
git add forgotten_file.py
git commit --amend
```

### Pushing and Pulling

```bash
# Push to remote
git push origin branch-name
git push origin development
git push -u origin feature/new    # Push and set upstream

# Pull from remote
git pull origin development
git pull                          # Pull from tracked branch

# Fetch without merging
git fetch origin
git fetch upstream                # Fetch from official Odoo
```

### Synchronizing with Upstream (Official Odoo)

```bash
# Fetch latest from official Odoo
git fetch upstream

# View what's new
git log HEAD..upstream/18.0 --oneline

# Merge official updates into your development
git checkout development
git merge upstream/18.0

# Resolve conflicts if any
# Edit conflicting files in VS Code
git add .
git commit -m "merge: sync with official Odoo 18.0"

# Push to your fork
git push origin development
```

### Viewing and Comparing

```bash
# View file at specific commit
git show commit-hash:path/to/file

# Compare branches
git diff development..feature/new
git diff origin/development..HEAD

# Show changes in last commit
git show HEAD
git show HEAD~1                 # Previous commit
git show HEAD~2                 # Two commits ago

# Search commit history
git log --grep="invoice"        # Find commits mentioning "invoice"
git log --author="developer"    # Commits by specific author
git log --since="2025-10-01"   # Commits since date
```

### Stashing (Temporary Save)

```bash
# Save work temporarily without committing
git stash
git stash save "work in progress on feature X"

# List stashes
git stash list

# Apply stashed changes
git stash pop                   # Apply and remove from stash
git stash apply                 # Apply but keep in stash

# Remove stash
git stash drop
git stash clear                 # Remove all stashes
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- filename        # Discard changes to file
git checkout -- .               # Discard all changes

# Unstage file (but keep changes)
git reset filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert commit-hash

# Reset to specific commit (DANGEROUS!)
git reset --hard commit-hash
```

### Resolving Conflicts

```bash
# When merge conflicts occur:

# 1. Pull latest changes
git pull origin development
# Git will show: CONFLICT in filename

# 2. Open conflicting files in VS Code
# Look for markers:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch

# 3. Resolve conflicts manually
# Remove markers and keep desired code

# 4. Mark as resolved
git add filename

# 5. Complete merge
git commit -m "fix: resolve merge conflicts"

# 6. Push
git push origin branch-name
```

### Advanced Git

```bash
# Cherry-pick specific commit
git cherry-pick commit-hash

# Interactive rebase (clean up history)
git rebase -i HEAD~3            # Edit last 3 commits

# View who changed each line
git blame filename

# Find when bug was introduced
git bisect start
git bisect bad                  # Current version is bad
git bisect good commit-hash     # Known good version
# Git will check out middle commit, test it
git bisect good/bad             # Mark current commit
# Repeat until bug found

# Create tag for release
git tag v1.0.0
git push origin v1.0.0
```

---

## 🔧 Troubleshooting

### Problem: "Permission denied (publickey)"

**Cause**: SSH key not found or incorrect permissions

**Solution**:
```bash
# Windows - Check file exists
dir "C:\path\to\MyTestApp-KeyPair.pem"

# Windows - Fix permissions
# Right-click file → Properties → Security → Advanced
# Remove all users except your account with Full Control

# Test SSH connection
ssh -i "MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
```

### Problem: "fatal: Authentication failed"

**Cause**: GitHub token expired or incorrect

**Solution**:
```bash
# 1. Generate new token at https://github.com/settings/tokens

# 2. Update remote URL on server
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47
cd /home/ec2-user/odoo18
git remote set-url origin https://NEW_TOKEN@github.com/karem505/odoo.git

# 3. Test
git pull origin development
```

### Problem: "Your branch is behind 'origin/development'"

**Cause**: Remote has changes you don't have locally

**Solution**:
```bash
# Pull latest changes
git pull origin development

# If you have local commits
git pull --rebase origin development
```

### Problem: Merge Conflicts

**Cause**: Same file edited by multiple people

**Solution**:
```bash
# 1. Pull latest
git pull origin development
# CONFLICT message appears

# 2. Open conflicting files in VS Code
# VS Code shows conflict markers and resolution options

# 3. Choose resolution:
# - Accept Current Change (your changes)
# - Accept Incoming Change (their changes)
# - Accept Both Changes
# - Edit manually

# 4. After resolving all conflicts
git add .
git commit -m "fix: resolve merge conflicts"
git push origin branch-name
```

### Problem: Odoo Won't Start After Git Pull

**Cause**: Code error or missing dependencies

**Solution**:
```bash
# 1. Check logs
tail -n 100 /home/ec2-user/.odoo/odoo-server.log

# 2. Look for Python errors
# Common issues:
# - SyntaxError: Fix Python syntax
# - ImportError: Install missing package
# - ModuleNotFoundError: Check module dependencies

# 3. Install missing Python packages if needed
sudo pip3.11 install package-name
sudo systemctl restart odoo

# 4. If still broken, rollback
git log --oneline -5
git reset --hard PREVIOUS_WORKING_COMMIT
sudo systemctl restart odoo
```

### Problem: "detached HEAD state"

**Cause**: Checked out specific commit instead of branch

**Solution**:
```bash
# Return to development branch
git checkout development
```

### Problem: Accidentally Committed to Wrong Branch

**Cause**: Forgot to create feature branch

**Solution**:
```bash
# If not yet pushed
# 1. Create correct branch
git branch feature/correct-branch

# 2. Reset current branch
git reset --hard HEAD~1

# 3. Switch to correct branch
git checkout feature/correct-branch

# Your commit is now on correct branch!
```

### Problem: Need to Delete Committed Sensitive Data

**Cause**: Accidentally committed password, token, or key

**Solution**:
```bash
# WARNING: This rewrites history!

# 1. Remove file from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive_file" \
  --prune-empty --tag-name-filter cat -- --all

# 2. Force push
git push origin --force --all

# 3. Rotate compromised credentials immediately!
# Change passwords, regenerate tokens, etc.
```

### Problem: VS Code Can't Connect to Server

**Cause**: Network, SSH, or permissions issue

**Solution**:
```bash
# 1. Test SSH from terminal first
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47

# 2. If SSH works, reload VS Code
# Press Ctrl+Shift+P → "Developer: Reload Window"

# 3. Check VS Code SSH config
# Press Ctrl+Shift+P → "Remote-SSH: Open SSH Configuration File"
# Verify settings are correct

# 4. Check AWS Security Group allows SSH (port 22) from your IP
```

---

## ✅ Best Practices

### Code Quality

1. **✅ Test Before Committing**
   ```bash
   # Always test changes locally
   sudo systemctl restart odoo
   tail -f /home/ec2-user/.odoo/odoo-server.log
   # Visit http://56.228.2.47:8069 and test features
   ```

2. **✅ Write Clear Commit Messages**
   ```bash
   # Good
   git commit -m "feat: add customer portal with OAuth authentication"

   # Bad
   git commit -m "updates"
   git commit -m "fix"
   ```

3. **✅ Keep Commits Focused**
   - One feature/fix per commit
   - Don't mix unrelated changes

4. **✅ Review Your Changes Before Committing**
   ```bash
   git diff                    # Review all changes
   git diff filename          # Review specific file
   ```

### Collaboration

1. **✅ Pull Before Starting Work**
   ```bash
   git checkout development
   git pull origin development
   ```

2. **✅ Use Feature Branches**
   - Never commit directly to `development` or `18.0`
   - Always create feature branches

3. **✅ Keep Branches Small and Short-lived**
   - Merge within 1-3 days
   - Don't let branches diverge too much

4. **✅ Communicate with Team**
   - Inform team before force pushing
   - Discuss major changes before implementing
   - Use Pull Request descriptions to explain changes

### Security

1. **❌ Never Commit Sensitive Data**
   - No passwords
   - No API keys or tokens
   - No private keys
   - No `.env` files with secrets

2. **✅ Use .gitignore**
   ```bash
   # Already configured, but verify:
   cat .gitignore | grep -E "\.conf|\.env|\.pem"
   ```

3. **✅ Rotate Tokens Regularly**
   - GitHub PAT every 90 days
   - Update server after rotation

4. **✅ Protect Master/Main Branches**
   - Set up branch protection on GitHub
   - Require pull request reviews
   - Require status checks to pass

### Maintenance

1. **✅ Regular Updates from Upstream**
   ```bash
   # Monthly: Sync with official Odoo
   git fetch upstream
   git checkout development
   git merge upstream/18.0
   git push origin development
   ```

2. **✅ Clean Up Old Branches**
   ```bash
   # List merged branches
   git branch --merged development

   # Delete merged branches
   git branch -d feature/old-feature
   git push origin --delete feature/old-feature
   ```

3. **✅ Regular Backups**
   ```bash
   # Weekly: Backup database
   sudo -u postgres pg_dump odoo18 > /tmp/odoo18_backup_$(date +%Y%m%d).sql
   ```

4. **✅ Monitor Logs**
   ```bash
   # Check for errors regularly
   grep -i error /home/ec2-user/.odoo/odoo-server.log | tail -20
   ```

### Performance

1. **✅ Keep Repository Size Manageable**
   - Don't commit large binary files
   - Don't commit generated files (.pyc, __pycache__)
   - Use Git LFS for large assets if needed

2. **✅ Use Shallow Clones for Large Repos**
   ```bash
   git clone --depth 1 --branch 18.0 https://github.com/karem505/odoo.git
   ```

3. **✅ Fetch Only What You Need**
   ```bash
   git fetch origin development
   # Instead of: git fetch --all
   ```

---

## 📚 Additional Resources

### Official Documentation

- **Git Official**: https://git-scm.com/doc
- **GitHub Docs**: https://docs.github.com
- **Odoo Developer**: https://www.odoo.com/documentation/18.0/developer.html
- **VS Code Remote SSH**: https://code.visualstudio.com/docs/remote/ssh

### Useful Git Tools

- **GitLens (VS Code)**: Enhanced Git visualization
- **Git Graph (VS Code)**: Visual branch graph
- **GitHub Desktop**: GUI for Git (Windows/Mac)
- **Sourcetree**: Advanced Git GUI

### Git Cheat Sheets

- https://education.github.com/git-cheat-sheet-education.pdf
- https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet

### Learning Resources

- **GitHub Learning Lab**: https://lab.github.com/
- **Atlassian Git Tutorials**: https://www.atlassian.com/git/tutorials
- **Git Branching Game**: https://learngitbranching.js.org/

---

## 📞 Support & Contacts

### Repository Owner

- **GitHub**: [@karem505](https://github.com/karem505)
- **Repository**: https://github.com/karem505/odoo

### Quick Help

**For Git Issues**:
1. Check [Troubleshooting](#troubleshooting) section
2. Search GitHub issues
3. Contact repository owner

**For Odoo Issues**:
1. Check server logs: `tail -f /home/ec2-user/.odoo/odoo-server.log`
2. Odoo documentation: https://www.odoo.com/documentation/18.0/
3. Odoo Community Forum: https://www.odoo.com/forum

**For AWS Issues**:
1. Check AWS Console: https://console.aws.amazon.com
2. Verify Security Groups
3. Check instance status

---

## 📝 Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-10-22 | Initial setup: Forked repo, configured remotes, created development branch | karem505 |
| 2025-10-22 | Updated .gitignore for team development | karem505 |

---

## ⚖️ License

This documentation is for internal team use. The Odoo source code is licensed under LGPL v3.

**Odoo License**: https://github.com/odoo/odoo/blob/18.0/LICENSE

---

## 🎯 Quick Reference Card

### Most Used Commands

```bash
# Daily workflow
git checkout development           # Switch to dev branch
git pull origin development        # Get latest
git checkout -b feature/name       # Create feature branch
# ... make changes ...
git add .                          # Stage changes
git commit -m "feat: description"  # Commit
git push origin feature/name       # Push to GitHub

# Deployment
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47
cd /home/ec2-user/odoo18
git pull origin development
sudo systemctl restart odoo
tail -f /home/ec2-user/.odoo/odoo-server.log

# Troubleshooting
git status                         # Check status
git log --oneline -5               # Recent commits
git diff                           # View changes
git reset --hard origin/development  # Reset to remote
```

### Emergency Contacts

| Issue | Action |
|-------|--------|
| **Server Down** | `sudo systemctl restart odoo` |
| **Git Conflicts** | See [Troubleshooting](#problem-merge-conflicts) |
| **Can't Connect** | Check AWS Security Groups, verify SSH key |
| **Odoo Errors** | Check logs: `tail -f /home/ec2-user/.odoo/odoo-server.log` |

---

**Document Version**: 1.0
**Last Updated**: October 22, 2025
**Maintained By**: karem505

---

*This documentation is a living document. Please update it as the workflow evolves.*
