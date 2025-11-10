# 📚 Odoo AWS Documentation

**Complete documentation for Odoo 18 development on AWS EC2**

---

## 📖 Documentation Index

This folder contains all documentation needed for developing and deploying Odoo on AWS.

### 🚀 Quick Start
Start here if you're new to the project:
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Get up and running in 5 minutes

### 📘 Main Documentation
Complete workflow and reference:
- **[ODOO_GIT_WORKFLOW_DOCUMENTATION.md](ODOO_GIT_WORKFLOW_DOCUMENTATION.md)** - Full Git workflow, commands, and best practices

### 🔐 Access & Credentials
Sensitive information (keep secure):
- **[SERVER_CREDENTIALS.md](SERVER_CREDENTIALS.md)** - Server access, passwords, and credentials

### ✅ Operations
Day-to-day operations:
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment guide

---

## 🎯 Quick Links

### Server Access
- **Web Interface**: http://56.228.2.47:8069
- **SSH**: `ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47`
- **GitHub**: https://github.com/karem505/API-for-odoo (Private)

### Common Tasks
```bash
# Connect to server
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47

# Deploy latest code
cd /home/ec2-user/odoo18
git pull origin development
sudo systemctl restart odoo

# Check logs
tail -f /home/ec2-user/.odoo/odoo-server.log
```

---

## 📂 Project Structure

```
Odoo AWS Logs/
├── README.md                              ← You are here
├── INDEX.md                               ← Complete documentation index
├── QUICK_START_GUIDE.md                   ← New developer onboarding
├── ODOO_GIT_WORKFLOW_DOCUMENTATION.md     ← Complete reference guide
├── SERVER_CREDENTIALS.md                  ← Access credentials (confidential)
├── DEPLOYMENT_CHECKLIST.md                ← Deployment procedures
├── DEPLOYMENT_LOG.md                      ← Deployment history
├── TROUBLESHOOTING_GUIDE.md               ← Problem solutions
└── REPOSITORY_MIGRATION_SUMMARY.md        ← Private repo migration details
```

---

## 🎓 Learning Path

### For New Developers
1. Read **QUICK_START_GUIDE.md**
2. Connect to server via VS Code
3. Make your first commit (guided in Quick Start)
4. Read **ODOO_GIT_WORKFLOW_DOCUMENTATION.md** sections:
   - Repository Structure
   - Daily Development Workflow
   - Git Commands Reference

### For Team Leads
1. Review **SERVER_CREDENTIALS.md** - Understand access control
2. Study **ODOO_GIT_WORKFLOW_DOCUMENTATION.md** - Team Workflow section
3. Use **DEPLOYMENT_CHECKLIST.md** for every deployment
4. Set up branch protection on GitHub

### For DevOps
1. **SERVER_CREDENTIALS.md** - Infrastructure details
2. **ODOO_GIT_WORKFLOW_DOCUMENTATION.md** - Deployment section
3. **DEPLOYMENT_CHECKLIST.md** - Deployment procedures

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              GitHub Repository (Private)                 │
│        https://github.com/karem505/API-for-odoo         │
│                                                          │
│  Branches:                                               │
│  ├── 18.0 (production/stable)                          │
│  └── development (active development)                   │
└─────────────────────────────────────────────────────────┘
                          │
                          │ git pull
                          ▼
┌─────────────────────────────────────────────────────────┐
│               AWS EC2 Instance (eu-north-1)             │
│         ec2-56-228-2-47.eu-north-1.compute...          │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Odoo 18 (/home/ec2-user/odoo18)              │    │
│  │  ├── Python 3.11                                │    │
│  │  ├── Port 8069                                  │    │
│  │  └── Service: odoo.service                      │    │
│  └────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  PostgreSQL 15 (localhost:5432)                │    │
│  │  └── Database: odoo18                           │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTP
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Users/Browsers                         │
│              http://56.228.2.47:8069                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Odoo | 18.0 |
| **Language** | Python | 3.11.13 |
| **Database** | PostgreSQL | 15.14 |
| **Web Server** | Werkzeug (built-in) | 2.2.2 |
| **OS** | Amazon Linux | 2023 |
| **Cloud** | AWS EC2 | t3.micro |
| **Version Control** | Git | 2.50.1 |
| **Repository** | GitHub | - |

---

## 👥 Team Workflow Overview

```
Developer Local Machine
        │
        │ (1) Code & Test
        ▼
Feature Branch (GitHub)
        │
        │ (2) Pull Request
        ▼
Development Branch (GitHub)
        │ Code Review
        │ Approve & Merge
        ▼
AWS Production Server
        │ (3) Deploy
        │ git pull + restart
        ▼
Live Odoo Instance
  http://56.228.2.47:8069
```

---

## 📊 Key Metrics & Goals

### Performance Targets
- **Page Load**: < 2 seconds
- **API Response**: < 500ms
- **Uptime**: > 99.5%

### Development Targets
- **Deployment Time**: < 5 minutes
- **Code Review Time**: < 24 hours
- **Bug Fix Time**: < 48 hours

### Quality Targets
- **Test Coverage**: > 80%
- **Zero Critical Bugs**: In production
- **Documentation**: Up to date

---

## 🔐 Security Guidelines

### Access Control
- ✅ SSH key required for server access
- ✅ GitHub 2FA enabled for all team members
- ✅ Master password protected
- ✅ Regular credential rotation

### Best Practices
- ❌ Never commit credentials to Git
- ❌ Never share SSH keys publicly
- ❌ Never expose database directly to internet
- ✅ Always use HTTPS in production (TODO)
- ✅ Regular security updates
- ✅ Monitor access logs

---

## 📅 Maintenance Schedule

### Daily
- Monitor logs for errors
- Check disk space
- Review user issues

### Weekly
- Deploy approved features
- Database backup verification
- Security group review

### Monthly
- Update from upstream Odoo
- Clean up old branches
- Performance optimization review

### Quarterly
- Rotate credentials
- AWS cost review
- Infrastructure optimization

---

## 🆘 Emergency Procedures

### Server Down
```bash
# Check status
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47
sudo systemctl status odoo

# Restart if needed
sudo systemctl restart odoo

# Check logs
tail -n 100 /home/ec2-user/.odoo/odoo-server.log
```

### Database Issues
```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Restart if needed
sudo systemctl restart postgresql

# Check connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity WHERE datname='odoo18';"
```

### Rollback Code
See **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Rollback section

---

## 📞 Support & Resources

### Internal Resources
- **Team Lead**: @karem505
- **Repository**: https://github.com/karem505/API-for-odoo (Private)
- **Server Logs**: `/home/ec2-user/.odoo/odoo-server.log`

### External Resources
- **Odoo Documentation**: https://www.odoo.com/documentation/18.0/
- **Odoo Community**: https://www.odoo.com/forum
- **GitHub Docs**: https://docs.github.com
- **AWS EC2 Docs**: https://docs.aws.amazon.com/ec2/

### Getting Help
1. Check relevant documentation file
2. Search error in Odoo logs
3. Search Odoo community forum
4. Contact team lead
5. Create GitHub issue

---

## 📝 Contributing to Documentation

This documentation is maintained by the team. To update:

1. Edit markdown files locally
2. Test formatting (use VS Code with Markdown preview)
3. Commit changes:
   ```bash
   git add "odoo AWS logs/*.md"
   git commit -m "docs: update documentation"
   git push
   ```

### Documentation Standards
- Use clear, simple language
- Include code examples
- Keep formatting consistent
- Update last modified date
- Test all commands before documenting

---

## 🎯 Project Goals

### Short Term (1-3 months)
- [ ] Set up SSL/HTTPS
- [ ] Implement automated backups
- [ ] Add monitoring/alerting
- [ ] Create custom modules

### Medium Term (3-6 months)
- [ ] CI/CD pipeline
- [ ] Staging environment
- [ ] Load balancing
- [ ] Performance optimization

### Long Term (6-12 months)
- [ ] Multi-region deployment
- [ ] Disaster recovery plan
- [ ] Advanced analytics
- [ ] Mobile app integration

---

## 📋 Document Maintenance

| Document | Last Updated | Next Review |
|----------|--------------|-------------|
| README.md | 2025-10-23 | 2025-11-23 |
| QUICK_START_GUIDE.md | 2025-10-23 | 2025-11-23 |
| ODOO_GIT_WORKFLOW_DOCUMENTATION.md | 2025-10-23 | 2025-11-23 |
| SERVER_CREDENTIALS.md | 2025-10-23 | 2025-11-23 |
| DEPLOYMENT_CHECKLIST.md | 2025-10-22 | 2025-11-22 |

**Review schedule**: Monthly or as needed

---

## ✅ Quick Health Check

Run these commands to verify everything is working:

```bash
# SSH works?
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47 "echo 'SSH OK'"

# Odoo running?
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47 "sudo systemctl status odoo"

# Git configured?
ssh -i MyTestApp-KeyPair.pem ec2-user@56.228.2.47 "cd /home/ec2-user/odoo18 && git status"

# Web accessible?
curl -I http://56.228.2.47:8069
```

All OK? ✅ You're good to go!

---

## 📜 Version History

### Version 1.1 (2025-10-23)
- Migrated to private repository (API-for-odoo)
- Updated all documentation references
- Added repository migration summary
- Updated Git workflow configuration

### Version 1.0 (2025-10-22)
- Initial documentation setup
- Complete Git workflow documented
- Deployment procedures established
- Quick start guide created

---

**Need help? Start with the [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)!**

**Questions? Contact @karem505 or check the relevant documentation file above.**

---

*This documentation is maintained by the Odoo development team.*
*Last updated: October 23, 2025*
