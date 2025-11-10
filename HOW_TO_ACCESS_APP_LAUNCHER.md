# 🚀 How to Access Your New Oravex App Launcher

## ✅ Module Installation Complete!

The `app_launcher_home` module is now **installed and running** on your Odoo AWS instance.

---

## 📍 How to Access the App Launcher

### Method 1: Direct URL (Recommended)

Simply visit this URL in your browser:

```
http://56.228.2.47:8069/web/app_launcher
```

**Important**:
- Make sure you're logged into Odoo first
- If you're not logged in, log in at: http://56.228.2.47:8069

### Method 2: From Odoo Home

1. Go to http://56.228.2.47:8069
2. Log in with your credentials
3. Navigate to: http://56.228.2.47:8069/web/app_launcher

---

## 🎨 What You Should See

When you access the app launcher, you should see:

✅ **ORAVEX** logo and branding in the header
✅ Animated teal/blue gradient background
✅ Custom icons for Sales, Inventory, Accounting, HR, CRM, Purchase
✅ Smooth hover animations on app cards
✅ "ORAVEX" title instead of "Welcome to Odoo"
✅ "Enterprise Resource Planning" subtitle

---

## 🔧 Troubleshooting

### If you still see "Welcome to Odoo":

**Clear your browser cache**:

1. **Chrome/Edge**: Press `Ctrl + Shift + Delete`
   - Select "Cached images and files"
   - Time range: "All time"
   - Click "Clear data"
   - Refresh the page with `Ctrl + F5`

2. **Firefox**: Press `Ctrl + Shift + Delete`
   - Check "Cache"
   - Time range: "Everything"
   - Click "Clear Now"
   - Refresh with `Ctrl + F5`

3. **Hard Refresh**: Press `Ctrl + Shift + R` or `Ctrl + F5`

### If icons still look the same:

This is normal for modules that don't have custom icons mapped. The controller generates beautiful SVG icons with Oravex colors for all modules automatically.

**To add a custom icon for a specific module**:

1. Create an SVG icon file
2. Upload it to: `/home/ec2-user/odoo18/addons/app_launcher_home/static/src/img/icons/`
3. Edit `/home/ec2-user/odoo18/addons/app_launcher_home/controllers/main.py`
4. Add the mapping in the `icon_mapping` dictionary
5. Restart Odoo: `sudo systemctl restart odoo`

### If the background is still plain:

1. Clear browser cache completely
2. Try accessing in **Incognito/Private mode**
3. Hard refresh with `Ctrl + Shift + R`
4. Try a different browser

---

## 🖼️ Current Icon Mappings

These modules will show custom icons:

- **Sales** → Shopping cart icon
- **CRM** → Heart/house icon
- **Invoicing** → Dollar sign icon
- **Accounting** → Dollar sign icon
- **Account** → Dollar sign icon
- **Inventory** → Grid boxes icon
- **Purchase** → Shopping bag icon
- **HR** → Person silhouette icon
- **Employees** → Person silhouette icon
- **Expenses** → Dollar sign icon (shares with accounting)
- **Point of Sale / POS** → Shopping cart icon (shares with sales)

All other modules get automatically generated SVG icons with Oravex colors!

---

## 🎯 Quick Access Bookmark

**Bookmark this URL for quick access**:
```
http://56.228.2.47:8069/web/app_launcher
```

---

## 📞 Still Having Issues?

If you're still seeing the old interface:

1. **Completely close** your browser (all windows)
2. **Reopen** the browser
3. Go to: http://56.228.2.47:8069/web/app_launcher
4. If still not working, try in **Incognito/Private mode**

If it works in Incognito mode, your browser cache needs to be cleared.

---

## 🔍 Verify Module is Installed

To verify the module is installed in Odoo:

1. Log into Odoo: http://56.228.2.47:8069
2. Go to **Apps** menu
3. Remove any filters (click the X on filter chips)
4. Search for "app_launcher_home"
5. You should see it marked as **Installed**

---

## ✨ What's Next?

1. **Access the app launcher** using the URL above
2. **Clear your browser cache** if you see the old design
3. **Enjoy** the new Oravex-branded interface!
4. **Customize** by adding more custom icons if needed

---

**Module Status**: ✅ Installed and Running
**Last Updated**: October 25, 2025
**Odoo Service**: Active and Running
