# 🚀 Deploying Samin on Render

This guide will help you deploy your Samin application on Render with automatic environment variable detection.

## 📋 Prerequisites

- A Render account
- Your application code pushed to a Git repository
- All required API keys and credentials

## 🔧 Environment Variables Setup

### 1. Go to Your Render Dashboard

- Navigate to [render.com](https://render.com)
- Select your service
- Go to **Environment** → **Environment Variables**

### 2. Add Required Variables

#### OAuth Configuration

```
CLIENT_ID=your_yandex_oauth_client_id
CLIENT_SECRET=your_yandex_oauth_client_secret
REDIRECT_URI=https://your-app-name.onrender.com/callback
```

#### Yandex Payment Configuration

```
YANDEX_MERCHANT_ID=your_yandex_merchant_id
YANDEX_API_URL=https://yoomoney.ru/api/v4
```

#### Security

```
SECRET_KEY=your_secret_key_here
adminPassword=your_admin_password
```

#### API Keys

```
DADATA_API_TOKEN=your_dadata_api_token
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key
```

#### Email Configuration

```
EMAIL_USER=your_email@yandex.ru
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=admin@samin.ru
```

#### Server Configuration

```
DEBUG_MODE=False
HOST=0.0.0.0
PORT=10000
```

### 3. Optional Variables

#### File Paths (Render will use these automatically)

```
DATA_DIR=/opt/render/project/src/static/data
PRIVATE_DIR=/opt/render/project/src/private
UPLOADS_DIR=/opt/render/project/src/static/uploads
```

#### Email Service

```
SMTP_SERVER=smtp.yandex.ru
SMTP_PORT=587
```

#### File Upload

```
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp
```

#### Application Info

```
APP_NAME=Samin
APP_VERSION=1.0.0
```

## 🎯 Automatic Detection Features

The application automatically detects when running on Render and:

- ✅ **Loads environment variables** from Render's environment
- ✅ **Adjusts file paths** for Render's file system
- ✅ **Provides helpful error messages** if variables are missing
- ✅ **Logs environment information** for debugging
- ✅ **Validates required variables** on startup

## 🔍 Environment Detection

The app detects Render deployment by checking for:

- `RENDER` environment variable
- `RENDER_EXTERNAL_HOSTNAME`
- `RENDER_SERVICE_ID`
- `RENDER_SERVICE_NAME`
- `RENDER_INSTANCE_ID`
- Hostname patterns containing "render"

## 🚨 Error Handling

If required environment variables are missing:

### On Render:

```
❌ Configuration Error: Required environment variable CLIENT_ID not set on Render.
   Please configure it in your Render dashboard.
💡 Tip: Go to your service → Environment → Environment Variables
```

### Locally:

```
❌ Configuration Error: Required environment variable CLIENT_ID not set.
   Please check your .env file or environment configuration.
💡 Tip: Create a .env file in your project root with all required variables.
```

## 📁 File Structure on Render

```
/opt/render/project/src/
├── static/
│   ├── data/           # Data files
│   ├── uploads/        # User uploads
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   └── images/         # Images
├── private/             # Private files
├── templates/           # HTML templates
├── routes/              # Flask routes
├── services/            # Business logic
├── utils/               # Utilities
├── app.py               # Main application
├── config.py            # Configuration
└── requirements.txt     # Dependencies
```

## 🐳 Docker Support

If using Docker on Render, ensure your Dockerfile:

1. **Copies all files** to the correct location
2. **Sets working directory** to `/opt/render/project/src`
3. **Exposes port** 10000 (Render's default)
4. **Runs as non-root** user for security

## 🔐 Security Best Practices

- ✅ **Never commit** `.env` files to Git
- ✅ **Use strong passwords** for admin accounts
- ✅ **Rotate API keys** regularly
- ✅ **Enable HTTPS** (automatic on Render)
- ✅ **Set DEBUG_MODE=False** in production

## 🚀 Deployment Steps

1. **Push code** to your Git repository
2. **Create service** on Render
3. **Connect repository** to Render
4. **Set environment variables** (see above)
5. **Deploy** and wait for build to complete
6. **Test** your application
7. **Monitor** logs for any issues

## 📊 Monitoring & Debugging

### View Logs

- Go to your service on Render
- Click **Logs** tab
- Look for environment detection messages

### Environment Info

The app logs detailed environment information:

```
🌍 Environment Detection:
   Platform: Linux 5.4.0
   Python: 3.9.16
   Running on Render: ✅ YES
   Render Service: samin-app
   Render Instance: abc123
   Debug Mode: ❌ DISABLED
   Data Directory: /opt/render/project/src/static/data
   Host: 0.0.0.0:10000
```

## 🆘 Troubleshooting

### Common Issues

1. **Environment variables not loading**

   - Check Render dashboard → Environment
   - Ensure variable names match exactly
   - Restart service after adding variables

2. **File permission errors**

   - Render handles file permissions automatically
   - Check if paths are correct in environment variables

3. **API keys not working**

   - Verify keys are set correctly
   - Check for extra spaces or characters
   - Ensure keys have proper permissions

4. **Port binding issues**
   - Render uses port 10000 by default
   - Set `PORT=10000` in environment variables

### Getting Help

- Check Render's [documentation](https://render.com/docs)
- Review application logs for error messages
- Verify all environment variables are set
- Test locally with `.env` file first

## 🎉 Success!

Once deployed, your application will:

- ✅ Automatically detect Render environment
- ✅ Load all configuration from environment variables
- ✅ Provide helpful error messages if something is wrong
- ✅ Work seamlessly across local and production environments

Happy deploying! 🚀
