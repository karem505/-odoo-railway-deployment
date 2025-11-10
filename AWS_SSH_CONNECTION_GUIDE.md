# 🔐 AWS Odoo Server - SSH Connection Guide

**Last Updated**: November 4, 2025
**Status**: ⚠️ Connection Issue - Wrong SSH Key

---

## 📋 Quick Connection Summary

### Current PEM File Status

| PEM File | Location | MD5 Fingerprint | Status |
|----------|----------|-----------------|--------|
| **odooaws.pem** | `C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs\odooaws.pem` | `94:cc:94:82:14:eb:2a:d5:35:64:1f:f8:a7:03:17:a3` | ❌ **REJECTED** |
| **MyTestApp-KeyPair.pem** | `C:\Users\Al Saad Nasr City\Downloads\MyTestApp-KeyPair.pem` | Unknown | ✅ **Expected Key** |

### SSH Key Fingerprint (Provided)
```
Key: e8:94:09:2f:85:f2:1c:e0:d7:0d:1d:0f:a4:ca:17:63:34:57:43:f5
```

---

## 🔧 Connection Issue Diagnosis

### Problem
The `odooaws.pem` file does **not** match the SSH key configured on the AWS EC2 instance.

### Technical Details
- **Attempted Connection**: `ssh -i "odooaws.pem" ec2-user@56.228.2.47`
- **Result**: `Permission denied (publickey,gssapi-keyex,gssapi-with-mic)`
- **Root Cause**: The public key derived from `odooaws.pem` is not in the instance's `~/.ssh/authorized_keys`

### SSH Debug Output
```
debug1: Trying private key: odooaws.pem
debug2: we sent a publickey packet, wait for reply
debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic
debug2: we did not send a packet, disable method
debug1: No more authentication methods to try.
```

---

## ✅ Solutions

### Option 1: Use the Correct PEM File (Recommended)
The EC2 instance is configured to accept **MyTestApp-KeyPair.pem**.

1. **Locate the original key**:
   ```bash
   # Expected location
   C:\Users\Al Saad Nasr City\Downloads\MyTestApp-KeyPair.pem
   ```

2. **If found, use it to connect**:
   ```bash
   cd "C:\Users\Al Saad Nasr City\Desktop\odoo AWS logs"
   ssh -i "../Downloads/MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
   ```

3. **Copy it to current directory** (optional):
   ```bash
   cp "C:\Users\Al Saad Nasr City\Downloads\MyTestApp-KeyPair.pem" .
   chmod 400 MyTestApp-KeyPair.pem
   ssh -i "MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
   ```

### Option 2: Replace the Key on AWS Instance

⚠️ **WARNING**: This requires AWS Console access and may cause downtime.

#### Steps:

1. **Generate new key pair in AWS Console**:
   - Go to: https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#KeyPairs
   - Actions → Create key pair
   - Name: `odooaws` (to match your file)
   - Type: RSA
   - Format: .pem
   - Download the new key

2. **Stop the instance** (required):
   - Instance ID: `i-034ca3b1f4e02393a`
   - Actions → Instance State → Stop

3. **Detach old key and attach new**:
   - Actions → Security → Modify instance key pair
   - Select new key pair: `odooaws`

4. **Start the instance**:
   - Actions → Instance State → Start
   - ⚠️ Note: Public IP may change!

5. **Test connection**:
   ```bash
   ssh -i "odooaws.pem" ec2-user@<NEW_IP>
   ```

### Option 3: Add New Key Without Replacing (Advanced)

If you have alternative access (AWS Systems Manager Session Manager), you can add the new key to `authorized_keys`:

1. **Connect via AWS Session Manager**:
   - Go to EC2 Console → Instance → Connect → Session Manager

2. **Add new public key**:
   ```bash
   # Extract public key from odooaws.pem
   ssh-keygen -y -f odooaws.pem > odooaws.pub

   # On the instance (via Session Manager)
   echo "<paste_public_key_here>" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

3. **Test connection**:
   ```bash
   ssh -i "odooaws.pem" ec2-user@56.228.2.47
   ```

---

## 📝 Correct Connection Commands

### Once You Have the Right Key

#### Using DNS Name
```bash
ssh -i "MyTestApp-KeyPair.pem" ec2-user@ec2-56-228-2-47.eu-north-1.compute.amazonaws.com
```

#### Using IP Address
```bash
ssh -i "MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
```

#### With Proper Permissions (Linux/Mac/Git Bash)
```bash
chmod 400 MyTestApp-KeyPair.pem
ssh -i "MyTestApp-KeyPair.pem" ec2-user@56.228.2.47
```

---

## 🔍 Key File Information

### Current PEM File (odooaws.pem)
```
Size: 1674 bytes
Type: RSA Private Key
Fingerprints:
  - MD5: 94:cc:94:82:14:eb:2a:d5:35:64:1f:f8:a7:03:17:a3
  - SHA256: 9VbmrmUberUuPjjXvGh9juE5GODI+Ner150nSXT622A
Format: Valid OpenSSH RSA private key
Status: ❌ Not authorized on EC2 instance
```

### Expected Key Fingerprint
```
Key provided by user: e8:94:09:2f:85:f2:1c:e0:d7:0d:1d:0f:a4:ca:17:63:34:57:43:f5
```

---

## 🖥️ AWS EC2 Instance Details

| Property | Value |
|----------|-------|
| **Instance ID** | i-034ca3b1f4e02393a |
| **Region** | eu-north-1 (Stockholm) |
| **Public IP** | 56.228.2.47 |
| **Public DNS** | ec2-56-228-2-47.eu-north-1.compute.amazonaws.com |
| **Instance Type** | t3.micro |
| **OS** | Amazon Linux 2023 |
| **Username** | ec2-user |

### AWS Console Links
- **Instance**: https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#Instances:instanceId=i-034ca3b1f4e02393a
- **Key Pairs**: https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#KeyPairs
- **Security Groups**: https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#SecurityGroups

---

## 🔐 Security Best Practices

### PEM File Permissions
```bash
# Linux/Mac/Git Bash
chmod 400 MyTestApp-KeyPair.pem

# Windows (PowerShell - run as Administrator)
icacls MyTestApp-KeyPair.pem /inheritance:r
icacls MyTestApp-KeyPair.pem /grant:r "%username%:R"
```

### SSH Config (Optional)
Create `~/.ssh/config` for easier access:

```
Host odoo-aws
    HostName 56.228.2.47
    User ec2-user
    IdentityFile C:\Users\Al Saad Nasr City\Downloads\MyTestApp-KeyPair.pem
    StrictHostKeyChecking no
    ServerAliveInterval 60
```

Then connect with:
```bash
ssh odoo-aws
```

---

## 🔧 Troubleshooting

### Issue: Permission Denied
**Symptoms**: `Permission denied (publickey,gssapi-keyex,gssapi-with-mic)`

**Solutions**:
1. Verify you're using the correct PEM file
2. Check file permissions: `ls -la MyTestApp-KeyPair.pem`
3. Ensure username is `ec2-user` (not `ubuntu` or `root`)
4. Verify instance is running in AWS Console

### Issue: Connection Timeout
**Symptoms**: `Connection timed out` or `No route to host`

**Solutions**:
1. Check instance is running: AWS Console → EC2 → Instances
2. Verify Security Group allows SSH (port 22) from your IP
3. Check if public IP has changed (if instance was stopped/started)
4. Try using DNS name instead of IP

### Issue: Host Key Verification Failed
**Symptoms**: `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`

**Solution**:
```bash
ssh-keygen -R 56.228.2.47
ssh-keygen -R ec2-56-228-2-47.eu-north-1.compute.amazonaws.com
```

### Issue: PEM File Not Found
**Solution**:
```bash
# Find all PEM files
find ~ -name "*.pem" -type f 2>/dev/null | grep -i test
```

---

## 📦 After Successful Connection

### Verify Installation
```bash
# Check hostname
hostname

# Check user
whoami

# Check Python
python3.11 --version

# Check PostgreSQL
psql --version

# Check Odoo
ls -la ~/odoo18

# Check Odoo service
sudo systemctl status odoo
```

### Access Odoo Web Interface
- **URL**: http://56.228.2.47:8069
- **Alternative**: http://ec2-56-228-2-47.eu-north-1.compute.amazonaws.com:8069

---

## 📞 Need Help?

### AWS Support
- **Console**: https://eu-north-1.console.aws.amazon.com/ec2/
- **Documentation**: https://docs.aws.amazon.com/ec2/

### Key Management
- **Generate New Key**: EC2 Console → Network & Security → Key Pairs → Create key pair
- **Instance Connect**: EC2 Console → Instance → Connect → Session Manager

### Emergency Access
If completely locked out:
1. Use AWS Session Manager (if IAM role configured)
2. Create snapshot and launch new instance with new key
3. Contact AWS Support for account recovery

---

## ✅ Next Steps

1. **Immediate**: Locate and use `MyTestApp-KeyPair.pem` to connect
2. **If not found**: Use AWS Console to create new key pair (see Option 2)
3. **After connecting**: Update this document with successful connection details
4. **Optional**: Set up SSH config for easier access
5. **Backup**: Keep PEM file in multiple secure locations

---

**🔒 KEEP THIS DOCUMENT AND PEM FILES SECURE**
**Do not commit to Git or share publicly**

---

**Document Version**: 1.0
**Status**: Awaiting correct PEM file for successful connection
