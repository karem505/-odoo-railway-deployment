# 🚀 Docker Quick Start - Odoo 18 + LiveKit Voice Agent

Get Odoo 18 with AI voice navigation running in **3 minutes**!

## Prerequisites

- Docker 20.10+ ([Install](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+ ([Install](https://docs.docker.com/compose/install/))
- OpenAI API Key ([Get one](https://platform.openai.com/api-keys))

## 🎯 Quick Start

### Option 1: Using Make (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/karem505/-odoo-railway-deployment.git
cd -odoo-railway-deployment

# 2. Create .env file
make env-template

# 3. Add your OpenAI API key
nano .env
# Set: OPENAI_API_KEY=sk-your-key-here

# 4. Start Odoo
make dev-up

# 5. Open browser
# http://localhost:8069
```

### Option 2: Using Docker Compose Directly

```bash
# 1. Clone repository
git clone https://github.com/karem505/-odoo-railway-deployment.git
cd -odoo-railway-deployment

# 2. Create .env file
cp .env.example .env

# 3. Add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# 4. Start services
docker-compose up -d

# 5. Open browser
# http://localhost:8069
```

## 🎤 Testing Voice Agent

1. **Login to Odoo**: http://localhost:8069
   - First time: Complete setup wizard
   - Username: `admin`
   - Password: `admin`

2. **Install Voice Agent Module**:
   - Go to **Apps** menu
   - Click **Update Apps List**
   - Search for "Voice"
   - Install **Odoo Voice Agent**

3. **Test Voice Navigation**:
   - Click **microphone icon** in top-right
   - Allow browser permissions
   - Say: **"Open sales"** or **"افتح المبيعات"**
   - Odoo navigates automatically!

## 📦 What's Running?

| Service | Port | Description |
|---------|------|-------------|
| Odoo | 8069 | Main ERP application |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache & sessions |
| LiveKit Agent | 8080 | Voice AI agent |

## 🛠️ Common Commands

### Using Make

```bash
make dev-up          # Start development
make dev-down        # Stop development
make dev-logs        # View logs
make dev-restart     # Restart services
make status          # Check status
make backup          # Backup database
```

### Using Docker Compose

```bash
docker-compose up -d              # Start
docker-compose down               # Stop
docker-compose logs -f            # View logs
docker-compose restart            # Restart
docker-compose ps                 # Check status
```

## 🔧 Troubleshooting

### Port 8069 already in use

```bash
# Check what's using the port
sudo lsof -i :8069

# Or change port in docker-compose.yml
ports:
  - "8070:8069"
```

### Can't connect to Odoo

```bash
# Check services
docker-compose ps

# Check logs
docker-compose logs odoo

# Restart
docker-compose restart odoo
```

### Voice agent not working

```bash
# Check agent logs
docker-compose logs livekit-agent

# Verify API key is set
docker-compose exec livekit-agent env | grep OPENAI
```

### Database errors

```bash
# Restart database
docker-compose restart postgres

# Check database logs
docker-compose logs postgres

# Reset everything (WARNING: deletes data!)
docker-compose down -v
docker-compose up -d
```

## 🌐 Accessing Services

- **Odoo**: http://localhost:8069
- **Odoo Debug Mode**: http://localhost:8069/web?debug=1
- **Database Shell**: `docker exec -it odoo-postgres psql -U odoo postgres`
- **Odoo Shell**: `docker exec -it odoo-web bash`

## 📊 Resource Usage

Check resource usage:
```bash
docker stats
```

Expected usage (idle):
- **Odoo**: ~200-500 MB RAM
- **PostgreSQL**: ~50-100 MB RAM
- **Redis**: ~10-20 MB RAM
- **LiveKit Agent**: ~100-200 MB RAM

## 🔒 Security Notes

**For development**:
- Default passwords are weak (okay for local dev)
- Database exposed on localhost

**For production**:
- Use `docker-compose.prod.yml`
- Set strong passwords in `.env`
- Don't expose database ports
- Use SSL/TLS certificates
- See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md) for full production guide

## 📚 Next Steps

1. **Customize Odoo**: Install apps from Apps menu
2. **Add modules**: Place in `custom_addons/` directory
3. **Configure**: Edit `.env` file
4. **Deploy to production**: See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)

## 🆘 Need Help?

- **Full documentation**: [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)
- **Odoo docs**: https://www.odoo.com/documentation/18.0/
- **Docker docs**: https://docs.docker.com/
- **Issues**: Open issue on GitHub

## ⚡ Pro Tips

```bash
# View logs for specific service
docker-compose logs -f odoo

# Execute commands in Odoo container
docker exec -it odoo-web odoo shell

# Backup database
make backup
# Or: docker exec odoo-postgres pg_dump -U odoo postgres > backup.sql

# Clean Docker resources
make clean

# Check Makefile for all commands
make help
```

## 🎉 Success!

You now have a fully functional Odoo 18 system with AI voice navigation!

Try saying:
- 🇬🇧 "Open sales"
- 🇬🇧 "Show me CRM"
- 🇸🇦 "افتح المبيعات"
- 🇸🇦 "اعرض المخزون"

---

**Deployment time**: ~3 minutes | **System requirements**: 4GB RAM, 2 CPU cores
