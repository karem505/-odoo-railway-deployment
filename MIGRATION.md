# AWS EC2 to Railway Migration Guide

Complete guide for migrating your existing Odoo 18 + LiveKit Voice Agent installation from AWS EC2 to Railway.

## 📋 Table of Contents

1. [Pre-Migration Checklist](#pre-migration-checklist)
2. [Data Backup](#data-backup)
3. [Railway Setup](#railway-setup)
4. [Database Migration](#database-migration)
5. [Custom Modules Migration](#custom-modules-migration)
6. [Testing & Validation](#testing--validation)
7. [Cutover Strategy](#cutover-strategy)
8. [Post-Migration](#post-migration)
9. [Rollback Plan](#rollback-plan)

---

## Pre-Migration Checklist

### ✅ Things to Verify Before Starting

- [ ] Railway account created and verified
- [ ] GitHub repository set up
- [ ] OpenAI API key available
- [ ] LiveKit credentials accessible
- [ ] AWS SSH key (`odoo2.pem`) accessible
- [ ] At least 4-6 hours for complete migration
- [ ] Backup storage for database export (1-5 GB recommended)
- [ ] List of all custom modules documented
- [ ] Current Odoo version confirmed (18.0)

### ⏰ Recommended Migration Window

- **Duration**: 2-4 hours (plus testing)
- **Best time**: Off-peak hours (evening/weekend)
- **Users**: Inform users of downtime

---

## Data Backup

### Step 1: Backup PostgreSQL Database

```bash
# SSH to AWS server
ssh -i "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com

# Create backup directory
mkdir -p ~/odoo_backups
cd ~/odoo_backups

# Backup database (choose one method)

# Method 1: Full database dump (recommended)
sudo -u postgres pg_dump postgres > odoo_full_backup_$(date +%Y%m%d_%H%M%S).sql

# Method 2: Custom format (compressed)
sudo -u postgres pg_dump -Fc postgres > odoo_backup_$(date +%Y%m%d_%H%M%S).dump

# Verify backup size
ls -lh odoo_*.sql
# Should be 100MB-5GB depending on your data

# Compress if needed
gzip odoo_full_backup_*.sql
```

### Step 2: Backup Filestore (User Uploads)

```bash
# Backup filestore (attachments, images, etc.)
sudo tar -czf filestore_backup_$(date +%Y%m%d).tar.gz /var/lib/odoo/.local/share/Odoo/filestore/

# Check size
ls -lh filestore_backup_*.tar.gz
```

### Step 3: Backup Custom Modules

```bash
# Backup custom addons
sudo tar -czf custom_addons_backup_$(date +%Y%m%d).tar.gz /opt/odoo/custom_addons/

# List what's included
tar -tzf custom_addons_backup_*.tar.gz | head -20
```

### Step 4: Download Backups to Local Machine

```bash
# On your Windows machine (PowerShell or CMD)
cd "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\backups"

# Download database
scp -i "..\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:~/odoo_backups/odoo_full_backup_*.sql.gz .

# Download filestore
scp -i "..\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:~/odoo_backups/filestore_backup_*.tar.gz .

# Download custom addons
scp -i "..\odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:~/odoo_backups/custom_addons_backup_*.tar.gz .
```

### Step 5: Export Configuration

```bash
# Save Odoo configuration
ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com 'sudo cat /etc/odoo/odoo.conf' > odoo_aws_config.conf

# Save LiveKit agent .env
ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com 'cat /opt/livekit-agent/.env' > livekit_aws_env.txt
```

---

## Railway Setup

### Step 1: Deploy to Railway

Follow the steps in `README_RAILWAY.md`:

1. Push code to GitHub
2. Create Railway project
3. Add PostgreSQL and Redis services
4. Configure environment variables
5. Wait for initial deployment

### Step 2: Verify Services Are Running

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Check service status
railway status
```

All services should show "Active" status.

---

## Database Migration

### Step 1: Prepare Database Backup

```bash
# Decompress if needed
gunzip odoo_full_backup_*.sql.gz
```

### Step 2: Upload to Railway PostgreSQL

```bash
# Option A: Via Railway CLI (recommended for large databases)
railway run --service postgres psql < odoo_full_backup_20241108.sql

# Option B: Via psql directly (if you have psql installed locally)
# Get DATABASE_URL from Railway dashboard
railway variables --service postgres

# Then:
psql "postgresql://postgres:password@host:port/railway" < odoo_full_backup_20241108.sql
```

**Expected output:**
```
SET
SET
CREATE TABLE
CREATE TABLE
...
(thousands of lines)
...
COPY 1234
COPY 5678
ALTER TABLE
CREATE INDEX
```

### Step 3: Verify Database Import

```bash
# Connect to Railway database
railway run --service postgres psql

# Check tables
\dt

# Check record counts
SELECT COUNT(*) FROM res_users;
SELECT COUNT(*) FROM res_partner;
SELECT COUNT(*) FROM sale_order;

# Exit
\q
```

### Step 4: Migrate Filestore (if needed)

**Note**: Filestore contains uploaded files (images, documents, etc.)

```bash
# Extract filestore backup
mkdir -p filestore_temp
cd filestore_temp
tar -xzf ../filestore_backup_20241108.tar.gz

# Upload to Railway (requires Railway storage or external S3/CDN)
# For now, Railway doesn't support persistent volumes easily
# Recommended: Use S3 or similar for file storage (separate guide)

# Alternative: Small filestores can be bundled in Docker image
# See "Advanced: Filestore Migration" section below
```

---

## Custom Modules Migration

### Step 1: Extract app_launcher_home from AWS

If you don't already have it locally:

```bash
# Download from AWS
scp -i "odoo2.pem" -r ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com:/opt/odoo/custom_addons/app_launcher_home ./custom_addons/

# Or extract from backup
tar -xzf custom_addons_backup_20241108.tar.gz
```

### Step 2: Add to Repository

```bash
# Copy to deployment directory
cp -r app_launcher_home "D:\odoo docker\odoo AWS logs\custom_addons\"

# Add to git
cd "D:\odoo docker\odoo AWS logs"
git add custom_addons/app_launcher_home
git commit -m "Add app_launcher_home custom module"
git push
```

Railway will automatically redeploy with the new module.

### Step 3: Install Modules in Railway Odoo

1. Access Railway Odoo URL
2. Login with admin credentials
3. Go to **Apps** → **Update Apps List**
4. Search for:
   - "Voice Navigation" (`odoo_voice_agent`)
   - "App Launcher Home" (`app_launcher_home`)
5. Click **Install** on each

---

## Testing & Validation

### Step 1: Functional Testing

```markdown
## Test Checklist

- [ ] Login works with existing users
- [ ] Company information displays correctly
- [ ] Sales module accessible
- [ ] CRM data visible
- [ ] Inventory records present
- [ ] Accounting data accessible
- [ ] Custom reports work
- [ ] User permissions correct
- [ ] Email notifications working (if configured)
```

### Step 2: Voice Agent Testing

```markdown
## Voice Agent Tests

- [ ] Microphone icon appears in systray
- [ ] Click microphone → connects to LiveKit
- [ ] Say "Open sales" → navigates to Sales
- [ ] Say "افتح المبيعات" → navigates to Sales (Arabic)
- [ ] Try other modules (CRM, Inventory, etc.)
- [ ] Agent responds with confirmations
- [ ] No JavaScript errors in console (F12)
```

### Step 3: Performance Testing

```bash
# Test database connection
railway run --service odoo python -c "import psycopg2; print('DB OK')"

# Test Redis connection
railway run --service redis redis-cli ping

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s https://your-odoo.railway.app/web

# Monitor logs
railway logs odoo -f
```

### Step 4: Data Integrity Checks

Login to Railway Odoo and verify:

```sql
-- Run in Railway PostgreSQL (railway run --service postgres psql)

-- Check user count
SELECT COUNT(*) FROM res_users;

-- Check partner count
SELECT COUNT(*) FROM res_partner;

-- Check sales orders
SELECT COUNT(*) FROM sale_order;

-- Check products
SELECT COUNT(*) FROM product_template;

-- Check latest records
SELECT id, name, create_date FROM sale_order ORDER BY create_date DESC LIMIT 5;
```

Compare counts with AWS database.

---

## Cutover Strategy

### Option A: Immediate Cutover (Simple)

**Best for**: Small teams, low transaction volume

1. **Maintenance Mode (AWS)**:
   ```bash
   ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com
   sudo systemctl stop odoo
   sudo systemctl stop livekit-agent
   ```

2. **Announce to Users**:
   - Send email/Slack message
   - "System migrating to new infrastructure"
   - "Downtime: 2-4 hours"
   - "New URL: https://your-odoo.railway.app"

3. **Complete Migration** (follow steps above)

4. **Update DNS** (if using custom domain):
   - Point `odoo.yourdomain.com` → Railway URL
   - Wait for DNS propagation (5-30 minutes)

5. **Go Live**:
   - Test thoroughly
   - Announce new URL to users
   - Monitor for issues

### Option B: Parallel Running (Safe)

**Best for**: Large teams, critical operations

1. **Keep AWS Running**
2. **Deploy to Railway** (complete setup)
3. **Sync Data Nightly**:
   ```bash
   # Schedule daily backup & restore
   # Run on AWS at 2 AM
   0 2 * * * /home/ec2-user/backup_and_sync.sh
   ```

4. **Test Railway for 1-2 weeks**:
   - Internal team uses Railway
   - Production users stay on AWS
   - Fix any issues found

5. **Final Cutover**:
   - Stop AWS Odoo
   - Do final data sync
   - Switch DNS
   - Announce to all users

---

## Post-Migration

### Step 1: Monitor for 48 Hours

```bash
# Watch logs continuously
railway logs odoo -f

# Check error rates
railway logs odoo | grep ERROR

# Monitor resource usage
# (Check Railway dashboard → Metrics)
```

### Step 2: Optimize Performance

```bash
# Adjust workers if needed
railway variables set WORKERS=4 --service odoo

# Monitor database connections
railway run --service postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
```

### Step 3: Setup Automated Backups

Railway PostgreSQL includes automatic backups, but verify:

1. Go to Railway dashboard → PostgreSQL service
2. Check **Backups** tab
3. Verify backup schedule (daily recommended)
4. Test restore procedure:
   ```bash
   railway run --service postgres pg_dump > test_backup.sql
   ```

### Step 4: Update Documentation

- Update internal wiki with new URLs
- Update API integrations (if any)
- Update bookmarks/shortcuts
- Train users on new URL

### Step 5: Decommission AWS (After 2-4 Weeks)

**Only after confirming Railway is stable:**

```bash
# 1. Stop AWS services
ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com
sudo systemctl stop odoo
sudo systemctl stop livekit-agent
sudo systemctl disable odoo
sudo systemctl disable livekit-agent

# 2. Keep one final backup
sudo -u postgres pg_dump postgres > final_aws_backup.sql

# 3. Download final backup
scp -i "odoo2.pem" ec2-user@...:/path/to/final_aws_backup.sql ./

# 4. Terminate EC2 instance (via AWS Console)
# IMPORTANT: This is irreversible!
```

---

## Rollback Plan

If migration fails, rollback to AWS:

### Emergency Rollback (< 1 hour after cutover)

```bash
# 1. SSH to AWS
ssh -i "odoo2.pem" ec2-user@ec2-51-20-91-45.eu-north-1.compute.amazonaws.com

# 2. Start services
sudo systemctl start odoo
sudo systemctl start livekit-agent

# 3. Verify services
sudo systemctl status odoo
sudo systemctl status livekit-agent

# 4. Check logs
sudo tail -f /var/log/odoo/odoo.log

# 5. Announce to users: back to old URL
```

### Planned Rollback (Data Loss Concerns)

If you discover data issues after hours/days:

1. **Stop Railway services** (to prevent further changes)
2. **Restore AWS database** from pre-migration backup:
   ```bash
   sudo systemctl stop odoo
   sudo -u postgres psql -c "DROP DATABASE postgres;"
   sudo -u postgres psql -c "CREATE DATABASE postgres;"
   sudo -u postgres psql postgres < final_aws_backup.sql
   sudo systemctl start odoo
   ```
3. **Update DNS** back to AWS (if changed)
4. **Investigate** what went wrong on Railway
5. **Plan re-migration** after fixes

---

## Troubleshooting

### Issue: Database import fails

**Error**: `ERROR: relation already exists`

**Solution**:
```bash
# Drop and recreate database
railway run --service postgres psql -c "DROP DATABASE railway;"
railway run --service postgres psql -c "CREATE DATABASE railway;"
railway run --service postgres psql railway < odoo_backup.sql
```

### Issue: Voice agent won't connect

**Error**: `Failed to connect to LiveKit`

**Solution**:
1. Check `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
2. Verify `OPENAI_API_KEY` is valid
3. Check LiveKit agent logs: `railway logs livekit-agent`

### Issue: Missing files/images

**Problem**: Uploaded files don't appear

**Solution**: Files are in filestore, need to migrate separately (see "Advanced: Filestore Migration")

### Issue: Performance is slow

**Problem**: Odoo responds slowly

**Solution**:
1. Increase workers: `WORKERS=4`
2. Check Redis connection is working
3. Upgrade Railway plan (more CPU/memory)
4. Check database indexes: `railway run --service postgres psql -c "\di"`

---

## Advanced: Filestore Migration

If you have many uploaded files (images, documents), you'll need to migrate the filestore:

### Option A: S3/External Storage (Recommended for Production)

1. **Install S3 addon** in Odoo
2. **Configure S3** bucket
3. **Upload filestore** to S3:
   ```bash
   aws s3 sync ./filestore/ s3://your-bucket/odoo-filestore/
   ```
4. **Configure Odoo** to use S3 (see Odoo docs)

### Option B: Bundle in Docker Image (Small filestores only)

```dockerfile
# In Dockerfile.odoo, add:
COPY ./filestore /var/lib/odoo/.local/share/Odoo/filestore/
RUN chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo/filestore/
```

**Warning**: This makes Docker image large and slow to build.

---

## Migration Checklist Summary

```markdown
## Pre-Migration
- [ ] Backups completed (database, filestore, custom modules)
- [ ] Railway project created
- [ ] Services deployed and running
- [ ] Environment variables configured

## During Migration
- [ ] AWS Odoo stopped (maintenance mode)
- [ ] Database imported to Railway
- [ ] Custom modules deployed
- [ ] Modules installed in Railway Odoo
- [ ] Testing completed (functional, voice agent, performance)

## Post-Migration
- [ ] Users notified of new URL
- [ ] DNS updated (if applicable)
- [ ] Monitoring active (48 hours)
- [ ] Backups verified
- [ ] AWS kept as backup (2-4 weeks)

## Decommission (After 2-4 weeks)
- [ ] Railway confirmed stable
- [ ] Final AWS backup downloaded
- [ ] AWS EC2 instance terminated
- [ ] Documentation updated
```

---

## Need Help?

- **Railway Support**: https://railway.app/support
- **Odoo Community**: https://www.odoo.com/forum
- **GitHub Issues**: Open issue in this repository

---

**Estimated Total Time**: 4-8 hours (including testing)

**Recommended Team**: 2 people (1 DevOps, 1 Odoo admin)

**Risk Level**: Medium (with proper backups and testing)
