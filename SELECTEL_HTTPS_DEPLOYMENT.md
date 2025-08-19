# 🚀 Selectel HTTPS Deployment Guide for Samin

## 🔐 Critical OAuth HTTPS Issues & Solutions

### **🚨 Why OAuth Fails on HTTPS:**

1. **Missing ProxyFix**: Flask doesn't know it's behind nginx/apache
2. **Session Cookie Issues**: HTTPS requires secure cookies
3. **Redirect URI Mismatch**: Yandex OAuth expects exact HTTPS URL
4. **Missing CSRF Protection**: OAuth flows need CSRF tokens
5. **Session Configuration**: HTTPS deployment needs specific session settings

---

## 🛠️ **Step 1: Environment Variables Setup**

### **Required Environment Variables on Selectel:**

```bash
# OAuth Configuration (CRITICAL for HTTPS)
CLIENT_ID=your_yandex_client_id
CLIENT_SECRET=your_yandex_client_secret
REDIRECT_URI=https://yourdomain.com/callback

# Security (CRITICAL for HTTPS)
SECRET_KEY=your_very_long_random_secret_key
DEBUG_MODE=False

# Other Required Variables
YANDEX_MERCHANT_ID=your_merchant_id
YANDEX_API_URL=https://api.yandex.ru
DADATA_API_TOKEN=your_dadata_token
YANDEX_MAPS_API_KEY=your_maps_api_key
adminPassword=your_admin_password
```

### **⚠️ CRITICAL: REDIRECT_URI Must Match Exactly**

- **Local Development**: `http://localhost:5000/callback`
- **Selectel HTTPS**: `https://yourdomain.com/callback`
- **No trailing slashes**
- **Exact case matching**

---

## 🔧 **Step 2: Yandex OAuth App Configuration**

### **In Yandex OAuth Console:**

1. **Callback URLs**: Add `https://yourdomain.com/callback`
2. **Remove old HTTP URLs** if they exist
3. **Save changes** and wait 5-10 minutes for propagation

### **OAuth App Settings:**

```
App Name: Samin
Platform: Web
Callback URLs: https://yourdomain.com/callback
```

---

## 🌐 **Step 3: Selectel Server Configuration**

### **Nginx Configuration (if using nginx):**

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # Security headers
    add_header X-Forwarded-Proto $scheme;
    add_header X-Forwarded-Host $host;
    add_header X-Forwarded-For $proxy_add_x_forwarded_for;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
    }
}
```

### **Apache Configuration (if using apache):**

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-Host "yourdomain.com"
</VirtualHost>
```

---

## 🐍 **Step 4: Python Application Setup**

### **Install Dependencies:**

```bash
pip install -r requirements.txt
```

### **Create Systemd Service (for auto-start):**

```bash
sudo nano /etc/systemd/system/samin.service
```

**Service Content:**

```ini
[Unit]
Description=Samin Flask Application
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/your/samin/app
Environment="PATH=/path/to/your/venv/bin"
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
ExecStart=/path/to/your/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable Service:**

```bash
sudo systemctl enable samin
sudo systemctl start samin
sudo systemctl status samin
```

---

## 🔍 **Step 5: Testing & Debugging**

### **Test OAuth Configuration:**

1. **Visit**: `https://yourdomain.com/debug/oauth` (if DEBUG_MODE=True)
2. **Check logs**: `sudo journalctl -u samin -f`
3. **Test login flow**: Try logging in with Yandex ID

### **Common Error Messages & Solutions:**

| Error                         | Cause                              | Solution                     |
| ----------------------------- | ---------------------------------- | ---------------------------- |
| `redirect_uri does not match` | URI mismatch in Yandex console     | Update callback URL exactly  |
| `unauthorized`                | Missing ProxyFix or session issues | Check nginx/apache headers   |
| `invalid_client`              | Wrong CLIENT_ID/SECRET             | Verify environment variables |
| `session expired`             | Cookie configuration issues        | Check HTTPS session settings |

---

## 🚀 **Step 6: Production Deployment**

### **Using Gunicorn (Recommended):**

```bash
pip install gunicorn
```

**Gunicorn Command:**

```bash
gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 app:app
```

**With Environment Variables:**

```bash
gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 --env FLASK_ENV=production app:app
```

### **Environment File:**

```bash
# /etc/environment or ~/.bashrc
export FLASK_ENV=production
export DEBUG_MODE=False
export CLIENT_ID=your_client_id
export CLIENT_SECRET=your_client_secret
export REDIRECT_URI=https://yourdomain.com/callback
export SECRET_KEY=your_secret_key
```

---

## 🔒 **Step 7: Security Checklist**

### **✅ HTTPS Configuration:**

- [ ] SSL certificate installed and working
- [ ] HTTP to HTTPS redirect configured
- [ ] HSTS headers enabled (optional)

### **✅ OAuth Security:**

- [ ] CSRF protection enabled
- [ ] Secure session cookies
- [ ] HTTPS-only cookies
- [ ] Proper redirect URI validation

### **✅ Server Security:**

- [ ] Firewall configured
- [ ] SSH key authentication
- [ ] Regular security updates
- [ ] Monitoring and logging enabled

---

## 🐛 **Troubleshooting**

### **Check Application Logs:**

```bash
sudo journalctl -u samin -f
tail -f /var/log/nginx/error.log
tail -f /var/log/apache2/error.log
```

### **Test OAuth Flow Manually:**

1. **Check callback URL**: Visit `/callback` directly
2. **Verify headers**: Check X-Forwarded-\* headers
3. **Session debugging**: Check browser cookies and network tab

### **Common Issues:**

1. **"redirect_uri does not match"**

   - Double-check Yandex OAuth console
   - Ensure exact URL match (no trailing slash)
   - Wait 5-10 minutes after changes

2. **"unauthorized" error**

   - Check ProxyFix configuration
   - Verify nginx/apache headers
   - Check session cookie settings

3. **Session not persisting**
   - Verify SECRET_KEY is set
   - Check HTTPS cookie configuration
   - Ensure proper domain settings

---

## 📞 **Support & Debugging**

### **Enable Debug Mode Temporarily:**

```bash
export DEBUG_MODE=True
export FLASK_ENV=development
```

### **Debug Endpoints:**

- `/debug/oauth` - OAuth configuration info
- Check browser console for JavaScript errors
- Check network tab for failed requests

### **Contact Information:**

- **Yandex OAuth Support**: Check Yandex developer documentation
- **Selectel Support**: Contact Selectel technical support
- **Application Logs**: Check system logs for detailed error information

---

## 🎯 **Success Indicators**

### **✅ OAuth Working Correctly:**

- User can click "Войти с Яндекс ID"
- Redirects to Yandex OAuth page
- Successfully returns to your site
- User session is created and maintained
- No "unauthorized" errors in logs

### **✅ HTTPS Working Correctly:**

- Site loads over HTTPS
- No mixed content warnings
- Secure cookies are set
- Proper redirects from HTTP to HTTPS

---

**🚀 Your Samin application should now work correctly with Yandex OAuth on Selectel with HTTPS!**
