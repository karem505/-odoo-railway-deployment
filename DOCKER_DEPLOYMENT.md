# Docker Deployment Guide - Odoo 18 with LiveKit Voice Agent

Complete guide for deploying Odoo 18 ERP with LiveKit voice agent integration using Docker.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Configuration](#configuration)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)

---

## Overview

This repository contains a fully Dockerized Odoo 18 deployment with:

- **Odoo 18**: Latest ERP system with custom modules
- **PostgreSQL 15**: Database backend
- **Redis 7**: Session and cache storage
- **LiveKit Voice Agent**: AI-powered voice navigation (Arabic/English)
- **Multi-stage builds**: Optimized Docker images
- **Production-ready**: Health checks, logging, resource limits

### Key Features

✅ **Easy deployment** with docker-compose
✅ **Multi-stage builds** for smaller images
✅ **Health checks** for all services
✅ **Automated database setup** and migrations
✅ **Environment-based configuration**
✅ **Makefile** for common operations
✅ **Production and development** configurations
✅ **LiveKit voice agent** integration

---

## Prerequisites

### Required Software

- **Docker**: 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Git**: For cloning repository
- **Make**: For using Makefile commands (optional but recommended)

### Required Credentials

You'll need:

1. **OpenAI API Key** - For voice agent ([Get API Key](https://platform.openai.com/api-keys))
2. **LiveKit Credentials** - Already configured in `.env.example`
3. **Strong passwords** - For production database and Odoo master password

### System Requirements

**Minimum** (Development):
- 4 GB RAM
- 2 CPU cores
- 20 GB disk space

**Recommended** (Production):
- 8 GB RAM
- 4 CPU cores
- 50 GB SSD disk space

---

## Quick Start

Get Odoo running in 3 minutes:

```bash
# 1. Clone repository
git clone https://github.com/karem505/-odoo-railway-deployment.git
cd -odoo-railway-deployment

# 2. Create environment file
cp .env.example .env

# 3. Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
# Set: OPENAI_API_KEY=sk-your-key-here

# 4. Start services
make dev-up
# Or without make: docker-compose up -d

# 5. Access Odoo
# Open browser: http://localhost:8069
# Default credentials: admin / admin (first setup)
```

That's it! Odoo is now running with the voice agent.

---

## Development Setup

### Step-by-Step Development Setup

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/karem505/-odoo-railway-deployment.git
   cd -odoo-railway-deployment
   ```

2. **Configure Environment**
   ```bash
   # Create .env file
   cp .env.example .env

   # Edit .env
   nano .env
   ```

   Minimal `.env` for development:
   ```env
   # Required
   OPENAI_API_KEY=sk-your-openai-api-key-here

   # Optional (defaults work for local dev)
   # ODOO_MASTER_PASSWORD=admin123
   # WORKERS=2
   ```

3. **Start Services**
   ```bash
   # Using Makefile (recommended)
   make dev-up

   # Or using docker-compose directly
   docker-compose up -d
   ```

4. **Check Status**
   ```bash
   make status
   # Or: docker-compose ps
   ```

5. **View Logs**
   ```bash
   make dev-logs
   # Or: docker-compose logs -f
   ```

6. **Access Odoo**
   - Open browser: http://localhost:8069
   - Complete setup wizard
   - Default credentials: `admin` / `admin`

7. **Install Voice Agent Module**
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Voice"
   - Install "Odoo Voice Agent"

### Development Commands

```bash
# Start development environment
make dev-up

# Stop development environment
make dev-down

# Restart Odoo service
make dev-restart-odoo

# View logs
make dev-logs
make dev-logs-odoo      # Odoo only
make dev-logs-agent     # LiveKit agent only

# Open shell
make shell-odoo         # Odoo container
make shell-db           # PostgreSQL container

# Clean everything (WARNING: deletes data!)
make dev-clean
```

### Development with Custom Addons

The `custom_addons/` directory is mounted as a volume, so changes are reflected immediately:

```bash
# Edit your module
nano custom_addons/odoo_voice_agent/models/your_model.py

# Restart Odoo to reload
make dev-restart-odoo

# Or use Odoo's debug mode for auto-reload
# In browser: http://localhost:8069/web?debug=1
```

---

## Production Deployment

### Production Setup Steps

1. **Prepare Environment**
   ```bash
   # Create production .env
   cp .env.example .env
   ```

2. **Configure Production .env**

   **IMPORTANT**: Use strong, unique passwords!

   ```bash
   # Generate secure passwords
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

   Minimal production `.env`:
   ```env
   # ============================================
   # REQUIRED PRODUCTION SETTINGS
   # ============================================

   # Database
   POSTGRES_PASSWORD=YOUR_STRONG_DB_PASSWORD_HERE
   REDIS_PASSWORD=YOUR_STRONG_REDIS_PASSWORD_HERE

   # Odoo
   ODOO_MASTER_PASSWORD=YOUR_STRONG_MASTER_PASSWORD_HERE
   SECRET_KEY=YOUR_RANDOM_SECRET_KEY_MIN_32_CHARS
   WORKERS=4

   # OpenAI
   OPENAI_API_KEY=sk-your-openai-api-key

   # LiveKit (already configured)
   LIVEKIT_URL=wss://live-agent-9pacbr1x.livekit.cloud
   LIVEKIT_API_KEY=APIGXGkGsm32tQF
   LIVEKIT_API_SECRET=RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA

   # Frontend URL (set to your actual domain)
   ODOO_FRONTEND_URL=https://your-domain.com

   # ============================================
   # OPTIONAL: Email Configuration
   # ============================================
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_SSL=true
   ```

3. **Verify Configuration**
   ```bash
   make check-env
   ```

4. **Build Production Images**
   ```bash
   make build-prod
   ```

5. **Start Production**
   ```bash
   make prod-up
   ```

6. **Verify Services**
   ```bash
   make prod-status
   make prod-logs
   ```

### Production Commands

```bash
# Start production
make prod-up

# Stop production
make prod-down

# View logs
make prod-logs

# Restart services
make prod-restart

# Check status
make prod-status

# Create database backup
make backup

# Restore database
make restore FILE=./backups/odoo_backup_20240101.sql
```

### Production Deployment on Cloud Platforms

#### Railway

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Create new project
railway init

# 4. Add PostgreSQL
railway add --plugin postgresql

# 5. Add Redis
railway add --plugin redis

# 6. Set environment variables
railway variables set OPENAI_API_KEY=sk-your-key
railway variables set ODOO_MASTER_PASSWORD=your-password
# ... set all required variables

# 7. Deploy
railway up
```

Railway will automatically:
- Use `Dockerfile.odoo` for the main service
- Provide `DATABASE_URL` and `REDIS_URL`
- Handle SSL/TLS termination

#### Docker Swarm

```bash
# 1. Initialize swarm
docker swarm init

# 2. Create secrets
echo "your-db-password" | docker secret create postgres_password -
echo "your-openai-key" | docker secret create openai_api_key -

# 3. Deploy stack
docker stack deploy -c docker-compose.prod.yml odoo

# 4. Check services
docker stack services odoo
docker stack ps odoo
```

#### Kubernetes (via Kompose)

```bash
# 1. Install Kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv kompose /usr/local/bin/

# 2. Convert docker-compose to Kubernetes manifests
kompose convert -f docker-compose.prod.yml

# 3. Create namespace
kubectl create namespace odoo

# 4. Create secrets
kubectl create secret generic odoo-secrets \
  --from-literal=postgres-password=your-password \
  --from-literal=openai-api-key=sk-your-key \
  -n odoo

# 5. Apply manifests
kubectl apply -f . -n odoo

# 6. Check deployment
kubectl get all -n odoo
```

---

## Configuration

### Environment Variables

All configuration is done via environment variables in `.env` file.

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for voice agent | `sk-proj-...` |
| `ODOO_MASTER_PASSWORD` | Master password for database management | `SecurePass123!` |
| `SECRET_KEY` | Session encryption key (min 32 chars) | `random_string_32_chars` |
| `POSTGRES_PASSWORD` | PostgreSQL database password | `DbPass123!` |
| `REDIS_PASSWORD` | Redis cache password | `RedisPass123!` |

#### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKERS` | `2` | Number of Odoo worker processes |
| `ODOO_FRONTEND_URL` | `http://localhost:8069` | Public URL for Odoo |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `SMTP_SERVER` | - | SMTP server for emails |
| `SMTP_PORT` | `587` | SMTP port |
| `INIT_DATABASE` | `false` | Initialize database on startup |
| `INSTALL_MODULES` | - | Comma-separated modules to install |

### Odoo Configuration

The `odoo.conf.template` is automatically populated from environment variables. Key settings:

- **Workers**: Auto-configured based on `WORKERS` env var
- **Database**: Auto-configured from `DATABASE_URL`
- **Redis**: Session storage via Redis
- **Proxy mode**: Enabled for reverse proxy support
- **Logging**: Configured for Docker (stdout/stderr)

### LiveKit Voice Agent Configuration

LiveKit credentials are set in `.env`:

```env
LIVEKIT_URL=wss://live-agent-9pacbr1x.livekit.cloud
LIVEKIT_API_KEY=APIGXGkGsm32tQF
LIVEKIT_API_SECRET=RfZNRb5sugVMuTFR47jC87Ts2LfxDT9HVioZVned8YVA
```

Agent behavior is configured in:
- `livekit-agent/prompts/agent_instructions.txt` - Agent personality
- `livekit-agent/agent.py` - Navigation logic

---

## Maintenance

### Database Backups

**Automated Backup (Recommended)**:

```bash
# Add to crontab
0 2 * * * cd /path/to/odoo && make backup
```

**Manual Backup**:

```bash
# Create backup
make backup
# Output: ./backups/odoo_backup_20240101_120000.sql

# Restore backup
make restore FILE=./backups/odoo_backup_20240101_120000.sql
```

**Backup to S3 (AWS)**:

```bash
# Backup and upload to S3
make backup
aws s3 cp ./backups/odoo_backup_$(date +%Y%m%d).sql s3://your-bucket/odoo-backups/
```

### Updates and Upgrades

**Update Docker Images**:

```bash
# Pull latest official Odoo image
docker pull odoo:18.0

# Rebuild your images
make build-prod

# Restart with new images
make prod-down
make prod-up
```

**Update Custom Modules**:

```bash
# Update module code
git pull origin main

# Restart Odoo
make prod-restart

# Or upgrade specific module via Odoo UI
# Apps → Search module → Upgrade
```

**Database Migration**:

```bash
# Set environment variable
export UPGRADE_MODULES=odoo_voice_agent,app_launcher_home

# Restart (will auto-upgrade)
make prod-restart
```

### Monitoring

**Check Service Health**:

```bash
make test
# Checks Odoo, PostgreSQL, and Redis health
```

**View Resource Usage**:

```bash
docker stats
```

**Export Logs**:

```bash
make logs-export
# Output: ./logs/odoo_logs_20240101_120000.log
```

### Scaling

**Increase Odoo Workers**:

```bash
# Edit .env
WORKERS=8

# Restart
make prod-restart
```

**Resource Limits** (edit `docker-compose.prod.yml`):

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 4G
    reservations:
      cpus: '2'
      memory: 2G
```

---

## Troubleshooting

### Common Issues

#### 1. **Odoo won't start**

```bash
# Check logs
make dev-logs-odoo

# Common causes:
# - Database connection failed
# - Port 8069 already in use
# - Missing environment variables

# Check database connectivity
make db-shell
```

#### 2. **Database connection errors**

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Verify credentials in .env
make check-env
```

#### 3. **LiveKit agent fails**

```bash
# Check agent logs
make dev-logs-agent

# Common causes:
# - Missing OPENAI_API_KEY
# - Invalid LiveKit credentials
# - Network connectivity issues

# Verify environment variables
docker exec odoo-livekit-agent env | grep -E 'LIVEKIT|OPENAI'
```

#### 4. **Out of disk space**

```bash
# Check Docker disk usage
docker system df

# Clean unused images and containers
make clean

# Remove all unused Docker resources
make clean-all  # WARNING: removes all images
```

#### 5. **Port conflicts**

```bash
# Check what's using port 8069
sudo lsof -i :8069

# Change Odoo port in docker-compose.yml
ports:
  - "8070:8069"  # Changed from 8069
```

### Debug Mode

**Enable Odoo Debug Mode**:

1. Access: `http://localhost:8069/web?debug=1`
2. Or use browser extension: "Odoo Debug"

**Enable verbose logging**:

```bash
# Edit docker-compose.yml
environment:
  LOG_LEVEL: DEBUG

# Restart
make dev-restart
```

**Access Container Shell**:

```bash
# Odoo container
make shell-odoo
# Or: docker exec -it odoo-web bash

# PostgreSQL
make shell-db
# Or: docker exec -it odoo-postgres bash
```

### Health Checks

All services have health checks:

```bash
# Check health status
docker-compose ps

# Manual health check
curl http://localhost:8069/web/health
```

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet / Users                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                ┌────────────▼────────────┐
                │  Nginx (Optional)       │
                │  Reverse Proxy + SSL    │
                └────────────┬────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│  Odoo Web      │  │  LiveKit Cloud  │  │  PostgreSQL    │
│  Port: 8069    │  │  (External)     │  │  Port: 5432    │
│                │  │                 │  │                │
│  - Web UI      │  │  - WebSocket    │  │  - Database    │
│  - API         │  │  - Voice Agent  │  │  - Persistence │
│  - OWL Widget  │  │    Connection   │  │                │
└───────┬────────┘  └────────┬────────┘  └───────┬────────┘
        │                    │                    │
        │           ┌────────▼────────┐           │
        │           │  LiveKit Agent  │           │
        │           │  Port: 8080     │           │
        │           │                 │           │
        │           │  - Python 3.11  │           │
        │           │  - OpenAI API   │           │
        └───────────┤  - Navigation   │───────────┘
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Redis Cache    │
                    │  Port: 6379     │
                    │                 │
                    │  - Sessions     │
                    │  - Cache        │
                    └─────────────────┘
```

### Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Docker Network                        │
│                        (odoo-network)                        │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  odoo-web-prod  │  │ livekit-agent   │                  │
│  │                 │  │                 │                  │
│  │  Image: Custom  │  │  Image: Custom  │                  │
│  │  Base: odoo:18  │  │  Base: py3.11   │                  │
│  │  Volumes:       │  │  Volumes: None  │                  │
│  │  - filestore    │  │  User: livekit  │                  │
│  │  User: odoo     │  │  Health: ✓      │                  │
│  │  Health: ✓      │  └─────────────────┘                  │
│  └─────────────────┘                                        │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ odoo-postgres   │  │  odoo-redis     │                  │
│  │                 │  │                 │                  │
│  │  Image: pg:15   │  │  Image: redis:7 │                  │
│  │  Volumes:       │  │  Volumes:       │                  │
│  │  - postgres_data│  │  - redis_data   │                  │
│  │  User: postgres │  │  Persistence: ✓ │                  │
│  │  Health: ✓      │  │  Health: ✓      │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Voice Input** → Browser (OWL Widget)
2. **Browser** → LiveKit Cloud (WebSocket + WebRTC)
3. **LiveKit Cloud** → LiveKit Agent (Python)
4. **Agent** → OpenAI Realtime API (Voice → Text → Intent)
5. **Agent** → Browser (Data Channel - Navigation Command)
6. **Browser** → Odoo Backend (HTTP - Module Navigation)
7. **Odoo** → PostgreSQL (Data Persistence)
8. **Odoo** → Redis (Session Storage)

### Volume Persistence

```
Host Machine                Docker Volumes
─────────────              ───────────────
./custom_addons/    →     (mounted, dev only)
./backups/          ←     (backup target)

Docker Volumes              Purpose
──────────────              ───────
postgres_data               Database files (persistent)
redis_data                  Redis persistence (AOF)
odoo_filestore              User uploads, attachments
```

---

## Additional Resources

### Documentation

- [Odoo 18 Documentation](https://www.odoo.com/documentation/18.0/)
- [LiveKit Documentation](https://docs.livekit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

### Files in This Repository

| File | Purpose |
|------|---------|
| `Dockerfile.odoo` | Odoo container build |
| `Dockerfile.livekit` | LiveKit agent build |
| `docker-compose.yml` | Development setup |
| `docker-compose.prod.yml` | Production setup |
| `Makefile` | Common commands |
| `.env.example` | Environment template |
| `odoo.conf.template` | Odoo configuration |
| `entrypoint-odoo.sh` | Odoo startup script |
| `entrypoint-livekit.sh` | Agent startup script |

### Custom Modules

- **odoo_voice_agent**: LiveKit voice navigation module
- **app_launcher_home**: Oravex custom home page

### Support

For issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review logs: `make dev-logs`
3. Open issue on GitHub

---

## Security Checklist

Before deploying to production:

- [ ] Strong `ODOO_MASTER_PASSWORD` set (min 20 chars)
- [ ] Strong `POSTGRES_PASSWORD` set
- [ ] Strong `REDIS_PASSWORD` set
- [ ] `SECRET_KEY` is random (min 32 chars)
- [ ] `.env` file is NOT committed to Git
- [ ] Database ports NOT exposed externally
- [ ] SSL/TLS configured (via nginx or reverse proxy)
- [ ] Firewall rules configured
- [ ] Automated backups configured
- [ ] Log rotation configured
- [ ] Resource limits set in docker-compose.prod.yml
- [ ] Health checks enabled

---

## License

This deployment configuration is provided as-is. Odoo is licensed under LGPL v3.

---

**Last Updated**: 2024-01-16
**Odoo Version**: 18.0
**Maintainer**: Odoo Voice Agent Team
