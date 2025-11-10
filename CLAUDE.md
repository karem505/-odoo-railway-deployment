# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

This is an **Odoo 18 ERP system** running on AWS EC2 with a **LiveKit voice agent integration** currently in progress. The voice agent enables bilingual (Arabic/English) voice navigation between Odoo modules.

**Current Status**: Voice agent code complete and documented in `voice_agent_complete_code.md` - **deployment pending**.

---

## AWS Server Connection

### Active Server Details
- **Host**: `ec2-51-20-91-45.eu-north-1.compute.amazonaws.com` (51.20.91.45)
- **Region**: eu-north-1 (Stockholm)
- **SSH Key**: `odoo2.pem` (located in this directory)
- **User**: ec2-user

### Connection Command
```bash
ssh -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com
```

### File Transfer (SCP)
```bash
# Upload single file
scp -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" local_file ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:/remote/path/

# Upload directory
scp -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" -r local_dir/ ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:/remote/path/

# Download from server
scp -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:/remote/path/file ./
```

---

## Odoo Installation Details

### Key Paths
- **Odoo Location**: `/opt/odoo/odoo18/`
- **Config File**: `/etc/odoo/odoo.conf`
- **Log File**: `/var/log/odoo/odoo.log`
- **Custom Addons**: `/opt/odoo/custom_addons/`
- **Systemd Service**: `/etc/systemd/system/odoo.service`

### Odoo Commands
```bash
# Restart Odoo
sudo systemctl restart odoo

# Check status
sudo systemctl status odoo

# View logs (real-time)
sudo tail -f /var/log/odoo/odoo.log

# View logs (last 100 lines)
sudo tail -n 100 /var/log/odoo/odoo.log
```

### Configuration
- **Version**: Odoo 18.0
- **Python**: 3.11 (`/usr/bin/python3.11`)
- **Port**: 8069
- **Database**: PostgreSQL 15
- **DB Name**: postgres (default)
- **DB User**: odoo
- **DB Password**: `Odoo2024!SecurePass` (in config file)

### Web Access
- **URL**: http://51.20.91.45:8069

---

## LiveKit Voice Agent Integration

### Overview
Voice-controlled navigation for Odoo using LiveKit + OpenAI Realtime API. Users can say commands like "افتح المبيعات" (Open Sales) or "Open sales" to navigate between modules.

### Architecture
```
┌─────────────────┐
│  Odoo Frontend  │  (JavaScript OWL Component - Floating Widget)
│  Port 8069      │
└────────┬────────┘
         │ LiveKit WebSocket + Data Channels
         ▼
┌─────────────────┐
│ LiveKit Cloud   │  wss://live-agent-9pacbr1x.livekit.cloud
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Voice Agent     │  Python Agent on EC2 (/opt/livekit-agent/)
│ OpenAI Realtime │  Handles voice → navigation commands
└─────────────────┘
```

### Current Status: DEPLOYED & OPERATIONAL (Currently Stopped)
1. ✅ Upload LiveKit agent files to `/opt/livekit-agent/`
2. ✅ Create `.env` file with credentials
3. ✅ Python dependencies installation completed
4. ✅ Agent.py updated and functional
5. ✅ Systemd service created and tested
6. ⚠️ **Agent Status**: Stopped and disabled (auto-start disabled on 2025-11-08)
7. ⏳ Odoo module `odoo_voice_agent` not yet created in `/opt/odoo/custom_addons/`
8. ⏳ LiveKit SDK not yet installed in Odoo Python environment

### Service Control
```bash
# Start agent (manual)
sudo systemctl start livekit-agent

# Stop agent
sudo systemctl stop livekit-agent

# Enable auto-start on reboot
sudo systemctl enable livekit-agent

# Disable auto-start
sudo systemctl disable livekit-agent

# Check status
sudo systemctl status livekit-agent
```

### Complete Implementation Code
**Location**: `voice_agent_complete_code.md` (in this directory)

Contains all 12 files needed:
- Odoo module structure (manifest, controllers, models)
- JavaScript widget (OWL component)
- CSS styling
- XML templates
- Updated agent.py navigation functions
- Systemd service configuration

### Key Files on Server

**LiveKit Agent** (on EC2):
- `/opt/livekit-agent/agent.py` - Main agent file (needs navigation functions update)
- `/opt/livekit-agent/.env` - Credentials (already created)
- `/opt/livekit-agent/prompts/agent_instructions.txt` - Agent personality (already updated)
- `/opt/livekit-agent/venv/` - Python virtual environment

**Odoo Module** (to be created):
- `/opt/odoo/custom_addons/odoo_voice_agent/` - Module directory (doesn't exist yet)

### Next Steps (To Complete Integration)

**Backend agent is deployed and tested. Remaining work: Frontend integration**

1. **Create Odoo module `odoo_voice_agent`**:
   - Create directory structure in `/opt/odoo/custom_addons/odoo_voice_agent`
   - Copy all frontend files from `voice_agent_complete_code.md`
   - Set ownership: `sudo chown -R odoo:odoo /opt/odoo/custom_addons/odoo_voice_agent`

2. **Install LiveKit SDK in Odoo environment**:
   ```bash
   sudo /usr/bin/python3.11 -m pip install livekit livekit-api
   ```

3. **Restart Odoo and install module**:
   ```bash
   sudo systemctl restart odoo
   # Then: Go to http://51.20.91.45:8069 → Apps → Update Apps List → Search "Voice" → Install
   ```

4. **Start the agent**:
   ```bash
   sudo systemctl enable --now livekit-agent
   ```

### Credentials (in .env file)
- **LiveKit URL**: `wss://live-agent-9pacbr1x.livekit.cloud`
- **LiveKit API Key**: `APIGXGkGsm32tQF`
- **LiveKit API Secret**: `RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA`
- **OpenAI API Key**: In `.env` file on server
- **Frontend URL**: `http://51.20.91.45:8069`

---

## Existing Custom Modules

### app_launcher_home (Oravex)
**Location**: `/opt/odoo/custom_addons/app_launcher_home/`

Custom home page for Odoo with Oravex branding.

**Local Copy**: This directory contains template files and icons for reference.

**Access**: http://51.20.91.45:8069/web/app_launcher

---

## Database Access

### PostgreSQL Commands
```bash
# Connect to database
sudo -u postgres psql

# Connect as odoo user
sudo -u odoo psql

# List databases
sudo -u postgres psql -c "\l"

# Backup database
sudo -u postgres pg_dump DATABASE_NAME > backup.sql

# Restore database
sudo -u postgres psql DATABASE_NAME < backup.sql
```

### Connection from Odoo
- **Host**: localhost
- **Port**: 5432
- **User**: odoo
- **Password**: `Odoo2024!SecurePass`
- **Authentication**: trust (for local odoo user)

---

## Common Development Tasks

### Deploy Code Changes to Server
```bash
# 1. SSH to server
ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com

# 2. Navigate to Odoo
cd /opt/odoo/odoo18/

# 3. Pull latest changes (if using Git)
sudo -u odoo git pull origin 18.0

# 4. Restart Odoo
sudo systemctl restart odoo

# 5. Check logs for errors
sudo tail -f /var/log/odoo/odoo.log
```

### Upload Custom Module
```bash
# From local machine
scp -i "odoo2.pem" -r module_name/ ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:/tmp/

# On server
ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com
sudo mv /tmp/module_name /opt/odoo/custom_addons/
sudo chown -R odoo:odoo /opt/odoo/custom_addons/module_name
sudo systemctl restart odoo
```

### Install Python Package for Odoo
```bash
# Install in system Python 3.11 (used by Odoo)
sudo /usr/bin/python3.11 -m pip install package_name

# Verify installation
/usr/bin/python3.11 -c "import package_name; print('OK')"

# Restart Odoo after installing packages
sudo systemctl restart odoo
```

### Debugging

**Check if service is running**:
```bash
sudo systemctl status odoo
sudo systemctl status livekit-agent  # When agent is deployed
sudo systemctl status postgresql
```

**View logs**:
```bash
# Odoo logs
sudo tail -f /var/log/odoo/odoo.log

# LiveKit agent logs (when deployed)
sudo journalctl -u livekit-agent -f

# PostgreSQL logs
sudo tail -f /var/lib/pgsql/data/log/postgresql-*.log

# System logs
sudo journalctl -xe
```

**Check ports**:
```bash
# Check what's listening on port 8069
sudo netstat -tulpn | grep 8069

# Check all Odoo processes
ps aux | grep odoo
```

**Restart everything**:
```bash
sudo systemctl restart postgresql
sudo systemctl restart odoo
sudo systemctl restart livekit-agent  # When deployed
```

---

## Architecture Notes

### Odoo 18 Structure
- **Web Client**: OWL (Odoo Web Library) JavaScript framework
- **Backend**: Python 3.11 with Werkzeug
- **Database ORM**: Odoo ORM (wraps psycopg2)
- **Views**: XML templates with QWeb
- **Assets**: Bundled via `__manifest__.py` 'assets' key

### Module Structure
```
odoo_voice_agent/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py           # HTTP routes for token generation
├── models/
│   └── __init__.py
├── static/src/
│   ├── js/
│   │   ├── voice_widget.js       # OWL component
│   │   └── navigation_handler.js # Event handler
│   ├── css/
│   │   └── voice_widget.css
│   └── xml/
│       └── voice_widget_templates.xml
└── views/
    └── webclient_templates.xml
```

### LiveKit Agent Communication
1. **Frontend** gets JWT token from Odoo backend (`/voice_agent/get_token`)
2. **Frontend** connects to LiveKit cloud with token
3. **Agent** (Python) connects to same LiveKit room
4. **Voice input** → OpenAI Realtime API → Agent decides action
5. **Agent** sends navigation command via **data channel** to frontend
6. **Frontend** receives command and updates Odoo URL hash

---

## Security Notes

### Credentials Security
- ⚠️ **odoo2.pem**: SSH private key - keep secure, never commit to Git
- ⚠️ **Database password** in `/etc/odoo/odoo.conf`
- ⚠️ **LiveKit credentials** hardcoded in `controllers/main.py` (should move to system parameters for production)
- ⚠️ **Old GitHub token** in `.env` should be revoked

### Access Control
- SSH: Only accessible with correct PEM file
- Odoo: User authentication required
- Database: Trust auth for local odoo user only
- LiveKit: Token-based authentication (JWT)

---

## Important Files in This Directory

| File | Purpose |
|------|---------|
| `odoo2.pem` | **SSH private key** - Required for server access |
| `voice_agent_complete_code.md` | **Complete voice agent code** - All 12 files needed for deployment |
| `SERVER_CREDENTIALS.md` | Server credentials and access details |
| `README.md` | Project overview and documentation index |
| `AWS_SSH_CONNECTION_GUIDE.md` | Detailed SSH troubleshooting |

---

## Testing Voice Agent (After Deployment)

1. **Start agent**: `sudo systemctl status livekit-agent` (should show "active (running)")
2. **Access Odoo**: http://51.20.91.45:8069
3. **Login** to Odoo
4. **Look for microphone icon** in top-right systray
5. **Click microphone** → Allow permissions
6. **Say test command**:
   - "افتح المبيعات" (Arabic - Open Sales)
   - "Open sales" (English)
   - "go to CRM"
   - "show me inventory"
7. **Verify navigation** occurs automatically

### Troubleshooting Voice Agent
```bash
# Check agent is running
sudo systemctl status livekit-agent

# View agent logs
sudo journalctl -u livekit-agent -n 50

# Check Odoo logs for module errors
sudo tail -f /var/log/odoo/odoo.log | grep voice_agent

# Check browser console (F12) for JavaScript errors

# Test LiveKit connection manually
curl -I wss://live-agent-9pacbr1x.livekit.cloud
```

---

## Known Issues

1. **Security**: LiveKit credentials are hardcoded in controller code (should move to system parameters for production)
2. **Old GitHub token**: Exists in .env, should be revoked for security
3. **Frontend integration**: Odoo module not yet created (backend agent is functional)

---

## Quick Start for New Session

```bash
# 1. Connect to server
ssh -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com

# 2. Check current state
sudo systemctl status odoo
sudo systemctl status livekit-agent  # Will fail if not yet deployed
ls -la /opt/livekit-agent/
ls -la /opt/odoo/custom_addons/

# 3. Continue voice agent deployment (if needed)
# See "Deployment Steps (When Continuing)" section above

# 4. View logs
sudo tail -f /var/log/odoo/odoo.log
```

---

**Last Updated**: 2025-11-08
**Project**: Odoo 18 + LiveKit Voice Agent Integration
**Status**: Backend agent deployed and functional (stopped). Frontend Odoo module pending.
