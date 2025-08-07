# 📧 Email Notification Setup Guide

## Overview

This system sends email notifications when customers place and pay for orders. It uses Yandex SMTP service for reliable delivery in Russia.

## 🔧 Setup Instructions

### 1. Create Yandex Email Account

1. Go to [Yandex Mail](https://mail.yandex.ru)
2. Create a new email account (e.g., `notifications@samin.ru`)
3. Enable SMTP access in settings

### 2. Generate App Password

1. Go to Yandex Account Settings
2. Navigate to "Security" → "App passwords"
3. Generate a new app password for SMTP
4. Save this password securely

### 3. Configure Environment Variables

Add these variables to your `.env` file:

```env
# Email Configuration
EMAIL_USER=your-email@yandex.ru
EMAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@samin.ru
```

### 4. Test Email Functionality

1. Start the Flask server
2. Visit `/test-email` to send a test email
3. Check if email is received at admin email address

## 📋 Email Features

### ✅ What's Included

- **Order Details**: Order ID, date, status
- **Customer Info**: Name, phone, address
- **Product List**: All items with quantities and prices
- **Total Calculation**: Subtotal, delivery, final total
- **Professional Design**: HTML email with Samin branding

### 🎨 Email Design

- **Header**: Gradient background with Samin colors
- **Order Info**: Clean section with order details
- **Customer Info**: Highlighted customer information
- **Product Table**: Organized product list
- **Total Section**: Clear price breakdown
- **Footer**: Professional branding

## 🔍 Troubleshooting

### Common Issues

1. **SMTP Authentication Failed**

   - Check email and password are correct
   - Ensure app password is used (not regular password)
   - Verify SMTP is enabled in Yandex settings

2. **Email Not Sending**

   - Check internet connection
   - Verify SMTP server settings
   - Check firewall settings

3. **Email Not Received**
   - Check spam folder
   - Verify admin email address
   - Check email service status

### Debug Steps

1. Check console logs for error messages
2. Test with `/test-email` route
3. Verify environment variables are loaded
4. Check Yandex account settings

## 📊 Email Content

### Order Information

- Order ID (shortened for readability)
- Date and time of order
- Payment status

### Customer Details

- Full name
- Phone number
- Delivery address

### Product Details

- Product name
- Quantity
- Unit price
- Total price per item

### Financial Summary

- Subtotal (products only)
- Delivery cost
- Final total

## 🚀 Production Deployment

### Security Considerations

1. Use environment variables for sensitive data
2. Enable SSL/TLS for email transmission
3. Regularly update app passwords
4. Monitor email delivery rates

### Performance Optimization

1. Email sending is asynchronous (non-blocking)
2. Failed emails are logged but don't affect order processing
3. Email service is fault-tolerant

## 📞 Support

If you encounter issues:

1. Check the console logs for error messages
2. Verify your Yandex account settings
3. Test with the `/test-email` route
4. Ensure all environment variables are set correctly

---

**Note**: This system is designed to work specifically with Russian email services for optimal delivery in Russia.
