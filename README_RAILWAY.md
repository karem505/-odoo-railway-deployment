# Odoo 18 + LiveKit Voice Agent - Railway Deployment

Complete Railway deployment package for Odoo 18 ERP with integrated LiveKit voice navigation agent.

## 🎯 Overview

This repository contains everything needed to deploy a fully functional Odoo 18 system with voice-controlled navigation to Railway. Users can navigate between Odoo modules using voice commands in Arabic or English.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RAILWAY SERVICES                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Odoo Web     │  │ LiveKit      │  │ PostgreSQL   │ │
│  │ (Port 8069)  │  │ Agent        │  │ Database     │ │
│  │              │  │ (Port 8080)  │  │              │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │          │
│         └──────────────────┴──────────────────┘          │
│                           │                              │
│                  ┌────────┴────────┐                    │
│                  │  Redis Cache    │                    │
│                  └─────────────────┘                    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  LiveKit Cloud         │
              │  wss://live-agent-... │
              └────────────────────────┘
```

## ✨ Features

- **Odoo 18 ERP**: Full-featured business management system
- **Voice Navigation**: Navigate between modules using voice commands
- **Bilingual Support**: Commands work in Arabic and English
- **Microservices Architecture**: Scalable and maintainable
- **Auto-deployment**: Push to GitHub → Railway auto-deploys
- **Redis Caching**: Session management and performance optimization
- **PostgreSQL**: Managed database with automatic backups
- **HTTPS**: Automatic SSL certificates via Railway

## 📋 Prerequisites

Before deployment, ensure you have:

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Account**: For repository and auto-deployment
3. **OpenAI API Key**: From [platform.openai.com](https://platform.openai.com)
4. **LiveKit Credentials**: Already configured in `.env.example`
5. **Git**: Installed locally for pushing code

## 🚀 Quick Start Deployment

### Step 1: Prepare Repository

```bash
# Clone or navigate to this directory
cd "D:\odoo docker\odoo AWS logs"

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Odoo 18 + LiveKit Voice Agent"

# Create GitHub repository and push
# Go to github.com → New Repository → "odoo-railway-deployment"
git remote add origin https://github.com/YOUR_USERNAME/odoo-railway-deployment.git
git branch -M main
git push -u origin main
```

### Step 2: Create Railway Project

1. Go to [railway.app/new](https://railway.app/new)
2. Click **"Deploy from GitHub repo"**
3. Select your repository: `odoo-railway-deployment`
4. Railway will detect the configuration automatically

### Step 3: Add Database Services

In Railway dashboard:

1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Click **"+ New"** → **"Database"** → **"Add Redis"**
3. Railway will automatically set `DATABASE_URL` and `REDIS_URL`

### Step 4: Configure Environment Variables

In Railway dashboard, go to **each service** → **Variables** and add:

**For Odoo Service:**
```
ODOO_MASTER_PASSWORD=your_secure_master_password
ODOO_ADMIN_PASSWORD=your_admin_password
SECRET_KEY=your_32_char_random_secret
LIVEKIT_URL=wss://live-agent-9pacbr1x.livekit.cloud
LIVEKIT_API_KEY=APIGXGkGsm32tQF
LIVEKIT_API_SECRET=RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA
WORKERS=2
```

**For LiveKit Agent Service:**
```
LIVEKIT_URL=wss://live-agent-9pacbr1x.livekit.cloud
LIVEKIT_API_KEY=APIGXGkGsm32tQF
LIVEKIT_API_SECRET=RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA
OPENAI_API_KEY=sk-your-openai-api-key
ODOO_FRONTEND_URL=https://your-odoo-service.railway.app
```

### Step 5: Deploy!

Railway will automatically:
1. Build Docker images
2. Deploy services
3. Connect services together
4. Provide you with a public URL

Access your Odoo at: `https://your-odoo-service.railway.app`

### Step 6: Initial Setup

1. **Access Odoo**: Open the Railway-provided URL
2. **Create Database**:
   - Database name: `production` (or your choice)
   - Admin password: Use `ODOO_ADMIN_PASSWORD` from env vars
   - Country: Select your country
   - Click "Create Database"

3. **Install Voice Agent Module**:
   - Go to **Apps** menu (top-right)
   - Click **"Update Apps List"**
   - Search for **"Voice Navigation"**
   - Click **"Install"**

4. **Test Voice Navigation**:
   - Look for microphone icon in top-right systray
   - Click it and allow microphone permissions
   - Say: **"Open sales"** or **"افتح المبيعات"**
   - Odoo should navigate automatically!

## 🧪 Local Testing (Before Railway)

Test everything locally using Docker Compose:

```bash
# 1. Create .env file with your OpenAI key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 2. Start all services
docker-compose up -d

# 3. Access Odoo
# Open: http://localhost:8069

# 4. View logs
docker-compose logs -f odoo
docker-compose logs -f livekit-agent

# 5. Stop services
docker-compose down

# 6. Stop and remove all data
docker-compose down -v
```

## 📁 Project Structure

```
odoo-railway-deployment/
├── Dockerfile.odoo              # Odoo container definition
├── Dockerfile.livekit           # LiveKit agent container
├── docker-compose.yml           # Local testing setup
├── railway.yaml                 # Railway service configuration
├── requirements.txt             # Odoo Python dependencies
├── livekit-requirements.txt     # Voice agent dependencies
├── odoo.conf.template           # Odoo configuration template
├── entrypoint-odoo.sh           # Odoo startup script
├── entrypoint-livekit.sh        # Agent startup script
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
│
├── custom_addons/
│   └── odoo_voice_agent/        # Voice navigation module
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── controllers/
│       │   ├── __init__.py
│       │   └── main.py          # LiveKit token generation
│       ├── models/
│       │   └── __init__.py
│       ├── static/src/
│       │   ├── js/
│       │   │   ├── voice_widget.js
│       │   │   └── navigation_handler.js
│       │   ├── css/
│       │   │   └── voice_widget.css
│       │   └── xml/
│       │       └── voice_widget_templates.xml
│       └── views/
│           └── webclient_templates.xml
│
├── livekit-agent/
│   ├── agent.py                 # Voice agent main file
│   └── prompts/
│       └── agent_instructions.txt
│
├── README_RAILWAY.md            # This file
├── MIGRATION.md                 # AWS → Railway migration guide
└── CLAUDE.md                    # Project context (for Claude Code)
```

## 🔧 Configuration

### Environment Variables

All configuration is done via environment variables. See `.env.example` for complete list.

**Critical Variables:**
- `DATABASE_URL`: Auto-provided by Railway PostgreSQL
- `REDIS_URL`: Auto-provided by Railway Redis
- `ODOO_MASTER_PASSWORD`: For database management (CHANGE THIS!)
- `OPENAI_API_KEY`: Required for voice agent
- `LIVEKIT_*`: LiveKit credentials

### Odoo Configuration

Odoo is configured via `odoo.conf.template` which supports:
- Database connection pooling
- Redis session storage
- Worker processes for scaling
- Proxy mode for Railway's HTTPS
- Custom addon paths

### Voice Agent Configuration

Agent behavior is defined in:
- `livekit-agent/agent.py`: Navigation functions
- `livekit-agent/prompts/agent_instructions.txt`: Agent personality

## 📊 Monitoring & Logs

### View Logs in Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# View logs
railway logs odoo
railway logs livekit-agent
```

### Health Checks

- **Odoo**: `https://your-app.railway.app/web/health`
- **LiveKit Agent**: Automatic health monitoring via Railway

## 🔄 Updates & Maintenance

### Deploy Updates

```bash
# Make changes to code
git add .
git commit -m "Your update message"
git push

# Railway auto-deploys new version
```

### Database Backup

```bash
# Via Railway CLI
railway run --service postgres pg_dump > backup.sql

# Or use Railway dashboard → PostgreSQL → Backups
```

### Scale Resources

In Railway dashboard:
1. Select service (Odoo or LiveKit)
2. Go to **Settings** → **Resources**
3. Adjust memory/CPU limits
4. Click **"Save"**

## 🐛 Troubleshooting

### Odoo won't start

1. Check logs: `railway logs odoo`
2. Verify `DATABASE_URL` is set
3. Check if PostgreSQL service is healthy
4. Ensure `ODOO_MASTER_PASSWORD` is set

### Voice agent not connecting

1. Check logs: `railway logs livekit-agent`
2. Verify `OPENAI_API_KEY` is valid
3. Check `LIVEKIT_URL` is correct
4. Ensure `ODOO_FRONTEND_URL` points to Odoo service

### Voice commands not working

1. Check browser console (F12) for JavaScript errors
2. Verify microphone permissions are granted
3. Check `odoo_voice_agent` module is installed
4. Test LiveKit connection in browser console

### Database connection issues

1. Verify PostgreSQL service is running
2. Check `DATABASE_URL` format is correct
3. Ensure database service is in same Railway project
4. Check firewall/network policies

## 🔒 Security Best Practices

1. **Change default passwords**: Use strong, unique passwords
2. **Secure master password**: Never commit to Git
3. **Rotate API keys**: Regularly update OpenAI and LiveKit keys
4. **Use HTTPS**: Railway provides automatic SSL
5. **Limit database access**: Only from Railway services
6. **Monitor logs**: Check for suspicious activity
7. **Regular backups**: Automated via Railway PostgreSQL

## 📈 Performance Optimization

### Odoo Workers

Adjust `WORKERS` based on traffic:
- Low traffic: `WORKERS=2`
- Medium traffic: `WORKERS=4`
- High traffic: `WORKERS=8`

Formula: `(2 * CPU_cores) + 1`

### Redis Caching

Sessions are automatically cached in Redis. Monitor hit rates in Railway dashboard.

### Database Connection Pooling

Configured in `odoo.conf.template`:
- `db_maxconn=64`: Maximum connections
- Adjust based on worker count

## 🌍 Custom Domain Setup

1. **In Railway**:
   - Go to Odoo service → **Settings** → **Domains**
   - Click **"Add Domain"**
   - Enter: `odoo.yourdomain.com`

2. **In DNS Provider** (e.g., Cloudflare, GoDaddy):
   - Add CNAME record:
     - Name: `odoo`
     - Value: `your-odoo-service.railway.app`

3. **Update Environment**:
   - Set `ODOO_FRONTEND_URL=https://odoo.yourdomain.com`
   - Update LiveKit agent's `ODOO_FRONTEND_URL`

4. **Wait for SSL**: Railway auto-provisions SSL (5-10 minutes)

## 🆘 Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Odoo Documentation**: https://www.odoo.com/documentation/18.0
- **LiveKit Docs**: https://docs.livekit.io
- **GitHub Issues**: Create issue in this repository

## 📝 License

This deployment configuration is provided as-is. Odoo is licensed under LGPL-3.

## 🙏 Credits

- **Odoo**: Open-source ERP platform
- **LiveKit**: Real-time communication platform
- **OpenAI**: Realtime API for voice processing
- **Railway**: Cloud deployment platform

---

**Need help?** Check `MIGRATION.md` for AWS → Railway migration guide or open an issue on GitHub.
