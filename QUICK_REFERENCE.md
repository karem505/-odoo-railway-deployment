# 🚀 Oravex App Launcher - Quick Reference

## Access the App Launcher

**URL**: http://56.228.2.47:8069/web/app_launcher

---

## File Locations

| File | Path |
|------|------|
| **Template** | `/home/ec2-user/odoo18/addons/app_launcher_home/views/app_launcher_templates.xml` |
| **Controller** | `/home/ec2-user/odoo18/addons/app_launcher_home/controllers/main.py` |
| **Logo** | `/home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/branding/oravex-logo.png` |
| **Icons** | `/home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/icons/` |

---

## Update Logo

To replace the logo with your actual Oravex logo:

```bash
# SSH into server
ssh -i "MyTestApp-KeyPair.pem" ec2-user@56.228.2.47

# Upload new logo (from your local machine)
scp -i "MyTestApp-KeyPair.pem" /path/to/your/oravex-logo.png ec2-user@56.228.2.47:/home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/branding/oravex-logo.png

# Restart Odoo
sudo systemctl restart odoo
```

---

## Customize Colors

Edit the template file and change the gradient colors:

```bash
nano /home/ec2-user/odoo18/addons/app_launcher_home/views/app_launcher_templates.xml
```

Look for these lines:
```css
background: linear-gradient(135deg, #0ea5b5 0%, #0d7c88 25%, #1a4d6d 75%, #0c3952 100%);
```

After changes, restart Odoo:
```bash
sudo systemctl restart odoo
```

---

## Add More Custom Icons

1. Create SVG icon file (e.g., `icon_manufacturing.svg`)
2. Upload to server:
```bash
scp -i "MyTestApp-KeyPair.pem" icon_manufacturing.svg ec2-user@56.228.2.47:/home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/icons/
```

3. Update controller mapping in `main.py`:
```python
icon_mapping = {
    'manufacturing': '/app_launcher_home/static/src/img/icons/icon_manufacturing.svg',
    # ... other mappings
}
```

4. Restart Odoo

---

## Troubleshooting

### Logo not showing?
```bash
# Check file exists
ls -lh /home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/branding/

# Check Odoo logs
tail -50 /home/ec2-user/.odoo/odoo-server.log
```

### Icons not showing?
```bash
# Verify icons directory
ls -lh /home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/icons/

# Clear browser cache and refresh
```

### Changes not appearing?
```bash
# Restart Odoo
sudo systemctl restart odoo

# Check service status
sudo systemctl status odoo

# Clear browser cache (Ctrl+Shift+Delete)
```

---

## Useful Commands

```bash
# Restart Odoo
sudo systemctl restart odoo

# View Odoo logs
tail -f /home/ec2-user/.odoo/odoo-server.log

# Check Odoo status
sudo systemctl status odoo

# Navigate to module
cd /home/ec2-user/odoo18/addons/app_launcher_home

# List all files
find . -type f
```

---

## Color Palette Reference

```
Primary:   #0ea5b5 (Bright Teal)
Secondary: #0d7c88 (Dark Teal)
Accent:    #1a4d6d (Navy)
Dark:      #0c3952 (Deep Blue)
Light:     #e0f7f8 (Light Teal)
```

---

## Support

- **Docs**: See `ORAVEX_APP_LAUNCHER_IMPLEMENTATION.md`
- **Server**: AWS EC2 (eu-north-1)
- **IP**: 56.228.2.47
- **Odoo Version**: 18.0
