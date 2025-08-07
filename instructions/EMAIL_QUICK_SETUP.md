# 🚀 Quick Email Setup Guide

## ❌ Current Issue

You're getting this error:

```
Error sending email notification: (535, b'5.7.8 Error: authentication failed: Invalid user or password!)
```

## ✅ Quick Fix

### Step 1: Create `.env` File

Create a file named `.env` in your project root (same folder as `app.py`):

```env
# Email Configuration
EMAIL_USER=your-yandex-email@yandex.ru
EMAIL_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@gmail.com
```

### Step 2: Get Yandex Credentials

#### Option A: Use Your Existing Yandex Account

1. Go to [Yandex Account Settings](https://passport.yandex.ru/profile)
2. Click "Security" → "App passwords"
3. Generate new password for "SMTP"
4. Use your Yandex email + this password

#### Option B: Create New Yandex Account

1. Go to [Yandex Mail](https://mail.yandex.ru)
2. Create account like `notifications@samin.ru`
3. Enable SMTP in settings
4. Generate app password

### Step 3: Update `.env` File

Replace with your actual credentials:

```env
EMAIL_USER=your-actual-yandex@yandex.ru
EMAIL_PASSWORD=your-actual-app-password
ADMIN_EMAIL=where-you-want-emails@gmail.com
```

### Step 4: Restart Server

```bash
# Stop current server (Ctrl+C)
# Then restart:
python3 app.py
```

### Step 5: Test

Visit: `http://127.0.0.1:5001/test-email`

## 🔧 Alternative: File-Based Testing

If you don't want to set up email right now, the system will save email content to files:

1. Place an order and pay
2. Check `static/data/` folder
3. Look for files like `email_notification_12345678.html`
4. Open these files in browser to see email content

## 📧 Email Features

✅ **Professional HTML Design**
✅ **Complete Order Details**
✅ **Customer Information**
✅ **Product Breakdown**
✅ **Financial Summary**
✅ **Samin Branding**

## 🆘 Need Help?

1. **Check console logs** for specific error messages
2. **Verify Yandex settings** - SMTP must be enabled
3. **Use app password** - not your regular password
4. **Test with `/test-email`** route

---

**Note**: The email system is designed to work with Russian email services for optimal delivery in Russia.
