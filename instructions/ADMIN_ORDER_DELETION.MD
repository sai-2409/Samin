# Admin Order Deletion System

## Overview

This system allows administrators to securely delete orders from the admin dashboard with password verification and automatic user notification.

## Features

### 🔐 Secure Password Verification

- Admin must enter their password to delete any order
- Password is verified against the `adminPassword` environment variable
- Prevents unauthorized order deletions

### 🗑️ Order Deletion Process

1. **Admin clicks delete button** (🗑️) next to any order in the admin dashboard
2. **Password verification modal** appears with order details
3. **Admin enters password** and confirms deletion
4. **Order is permanently removed** from `orders.json`
5. **User receives notification** about the cancelled order

### 📢 User Notification System

- **Automatic notification** sent to order owner when their order is deleted
- **Real-time notification badge** appears for users with unread notifications
- **Notification panel** shows all user notifications
- **Mark as read** functionality to dismiss notifications

## API Endpoints

### DELETE Order

```
POST /api/delete-order
```

**Request Body:**

```json
{
  "order_id": "order_uuid_here",
  "admin_password": "admin_password_here"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Order abc12345 deleted successfully",
  "customer_name": "John Doe"
}
```

### Get Notifications

```
GET /api/get-notifications
```

**Response:**

```json
{
  "notifications": [
    {
      "id": "del_20250807_004316",
      "user_id": "user_login",
      "type": "order_deleted",
      "title": "Заказ отменен",
      "message": "Ваш заказ #abc12345 был отменен администратором...",
      "timestamp": "2025-08-07T00:43:16.123456",
      "read": false
    }
  ]
}
```

### Mark Notification Read

```
POST /api/mark-notification-read
```

**Request Body:**

```json
{
  "notification_id": "del_20250807_004316"
}
```

## Files Modified

### Backend (`routes/main.py`)

- Added `/api/delete-order` endpoint with password verification
- Added `/api/get-notifications` endpoint for user notifications
- Added `/api/mark-notification-read` endpoint for marking notifications as read
- Integrated notification creation when orders are deleted

### Frontend (`templates/admin.html`)

- Added delete button (🗑️) to each order row
- Added password verification modal
- Added JavaScript functions for delete functionality
- Enhanced with loading states and error handling

### User Interface (`static/js/commonScript.js`)

- Added notification system for users
- Real-time notification badge
- Notification panel with read/unread functionality
- Automatic notification checking every 30 seconds

### Templates

- Added `data-user-login` attribute to body tags for notification system
- Updated `.gitignore` to exclude `notifications.json`

## Security Features

### ✅ Password Protection

- Admin password required for all deletions
- Password verified against environment variable
- No hardcoded passwords in code

### ✅ User Notification

- Order owner automatically notified of deletion
- Notification includes order ID and contact information
- Users can mark notifications as read

### ✅ Audit Trail

- All deletions logged with timestamp
- User notifications stored with unique IDs
- Order details preserved in notification message

## Usage Instructions

### For Administrators:

1. Log into admin dashboard at `/admin`
2. Find the order you want to delete
3. Click the 🗑️ button next to the order
4. Enter your admin password in the modal
5. Click "Удалить заказ" to confirm
6. Order will be deleted and user will be notified

### For Users:

1. Notifications appear as red badge in top-right corner
2. Click badge to view notification panel
3. Click on notification to mark as read
4. Notifications automatically check for updates every 30 seconds

## Environment Variables Required

Make sure your `.env` file contains:

```
adminPassword=your_secure_admin_password
```

## File Structure

```
static/data/
├── orders.json          # Order data (ignored by git)
└── notifications.json   # User notifications (ignored by git)
```

## Error Handling

- **Invalid password**: Returns 401 error with message
- **Order not found**: Returns 404 error
- **Missing data**: Returns 400 error
- **Server errors**: Returns 500 error with logging

## Testing

1. **Admin login**: Visit `/admin-login` and enter admin password
2. **Delete order**: Use delete button in admin dashboard
3. **User notification**: Check notification badge appears for affected user
4. **Password verification**: Try deleting with wrong password
