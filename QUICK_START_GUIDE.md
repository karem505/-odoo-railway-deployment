# 🚀 Odoo AWS - Quick Start Guide

**For New Developers** | **5-Minute Setup**

---

## ⚡ Connect to Server in 3 Steps

### Step 1: Get SSH Key
- Ask team lead for: `MyTestApp-KeyPair.pem`
- Save it somewhere safe (e.g., `C:\keys\MyTestApp-KeyPair.pem`)

### Step 2: Install VS Code Extension
1. Open **VS Code**
2. Press `Ctrl+Shift+X`
3. Search: **"Remote - SSH"**
4. Click **Install**

### Step 3: Connect
1. Press `F1` in VS Code
2. Type: `Remote-SSH: Connect`
3. Enter:
   ```
   ssh -i "C:\path\to\MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
   ```
4. Open folder: `/home/ec2-user/odoo18`

**✅ You're connected!**

---

## 🎯 Your First Commit (5 Minutes)

```bash
# 1. Open VS Code terminal (Ctrl+`)

# 2. Get latest code
cd /home/ec2-user/odoo18
git pull origin development

# 3. Create your branch
git checkout -b feature/my-first-feature

# 4. Make a small change
# Edit any file in VS Code (e.g., add a comment)

# 5. Test it works
sudo systemctl restart odoo

# 6. Commit and push
git add .
git commit -m "feat: my first commit"
git push origin feature/my-first-feature

# 7. Go to GitHub and create Pull Request
# https://github.com/karem505/API-for-odoo
```

**🎉 Congratulations! You just made your first contribution!**

---

## 📖 Daily Workflow Cheat Sheet

```bash
# Morning: Get latest code
git checkout development
git pull origin development

# Create feature branch
git checkout -b feature/description

# After changes: Test
sudo systemctl restart odoo
tail -f /home/ec2-user/.odoo/odoo-server.log  # Ctrl+C to exit

# Commit
git add .
git commit -m "feat: what you did"
git push origin feature/description

# Evening: Create PR on GitHub
```

---

## 🆘 Common Issues

### Can't connect to server?
```bash
# Test SSH from command prompt:
ssh -i "path\to\MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
```

### Odoo won't start?
```bash
# Check logs:
tail -n 50 /home/ec2-user/.odoo/odoo-server.log
```

### Git conflicts?
```bash
# Get latest and try again:
git checkout development
git pull origin development
git checkout -b feature/new-branch-name
```

---

## 📞 Need Help?

- **Full Documentation**: See `ODOO_GIT_WORKFLOW_DOCUMENTATION.md`
- **Server Access**: `http://56.228.2.47:8069`
- **GitHub Repo**: https://github.com/karem505/API-for-odoo (Private)
- **Team Lead**: @karem505

---

## ⚡ Must-Know Commands

| Task | Command |
|------|---------|
| Get latest code | `git pull origin development` |
| Create branch | `git checkout -b feature/name` |
| See status | `git status` |
| Commit | `git add . && git commit -m "message"` |
| Push | `git push origin branch-name` |
| Restart Odoo | `sudo systemctl restart odoo` |
| Check logs | `tail -f /home/ec2-user/.odoo/odoo-server.log` |

---

**Ready to code? Open VS Code and connect to the server!** 🚀
