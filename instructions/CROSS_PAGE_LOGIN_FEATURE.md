# Cross-Page Login Information Feature

## Overview

This feature ensures that user login information appears consistently across both `index.html` and `cartSamin.html` pages. When a user logs in from either page, their login information is properly displayed on both pages, and users can navigate seamlessly between them.

## How It Works

### User Session Management

- **Consistent Session Handling**: Both pages now receive user session information from the backend
- **Login Success Messages**: Both pages display welcome messages when users log in
- **Real-time Updates**: User information updates immediately across both pages

### Navigation Between Pages

- **Index Page**: Added "Корзина" (Cart) link in navigation menu
- **Cart Page**: Added "Главная" (Main) link in navigation menu
- **Sidebar Navigation**: Both pages include links to each other in mobile sidebar
- **Visual Indicators**: Cart page highlights the current page in navigation

## Implementation Details

### Files Modified

1. **`routes/main.py`**

   - Updated `/cart` route to pass user session information
   - Added `just_logged_in` flag handling for success messages

2. **`templates/index.html`**

   - Added "Корзина" link to main navigation menu
   - Added "Корзина" link to mobile sidebar navigation
   - Added login success message display
   - Enhanced user experience with visual feedback

3. **`templates/cartSamin.html`**

   - Added "Главная" link to main navigation menu
   - Added "Корзина" link to mobile sidebar navigation
   - Added login success message display
   - Updated navigation to point to actual pages instead of sections

4. **`static/js/commonScript.js`**

   - Added responsive header functionality for mobile devices
   - Implemented sidebar toggle functionality
   - Added overlay and close button functionality
   - Ensures consistent behavior across both pages

5. **`static/css/responsiveCart.css`**
   - Added responsive header styles for small screens
   - Implemented mobile navigation sidebar styles
   - Added overlay and toggle button styles
   - Ensures consistent responsive design across both pages

### Key Features

#### Login Success Messages

- **Index Page**: Shows welcome message with user's name
- **Cart Page**: Shows welcome message with user's name and order context
- **Visual Design**: Green gradient background with checkmark icon
- **Auto-dismiss**: Messages appear only for the current session

#### Navigation Enhancements

- **Main Menu**: Direct links between index and cart pages
- **Mobile Sidebar**: Consistent navigation on mobile devices
- **Visual Feedback**: Current page highlighted in navigation
- **Intuitive Icons**: Home and cart icons for easy recognition
- **Responsive Design**: Full mobile support with hamburger menu
- **Touch-Friendly**: Optimized for mobile touch interactions

#### User Information Display

- **Avatar Display**: Shows user's Yandex avatar in header
- **User Name**: Displays real name, display name, or login
- **Profile Dropdown**: Access to reviews, orders, and logout
- **Consistent Layout**: Same header structure on both pages

## Usage Examples

### Scenario 1: User logs in from index page

1. User visits `/` (index page)
2. User clicks "Войти с Яндекс ID"
3. User completes Yandex OAuth
4. User sees success message on index page
5. User can navigate to cart page and see same login status

### Scenario 2: User logs in from cart page

1. User visits `/cart` (cart page)
2. User clicks "Войти с Яндекс ID"
3. User completes Yandex OAuth
4. User sees success message on cart page
5. User can navigate to index page and see same login status

### Scenario 3: Navigation between pages

1. User is logged in on either page
2. User clicks "Корзина" to go to cart page
3. User sees same login information and avatar
4. User clicks "Главная" to return to index page
5. User maintains login status throughout navigation

## Technical Notes

### Session Management

- Uses Flask session to store user information
- `just_logged_in` flag for temporary success messages
- Session data passed to both page templates

### Template Variables

- `user`: Contains user login, avatar, real_name, display_name
- `just_logged_in`: Boolean flag for success message display
- Conditional rendering based on login status

### Navigation Structure

- Main navigation menu with direct page links
- Mobile sidebar with consistent navigation
- Visual indicators for current page
- Responsive design for all screen sizes

### User Experience

- Immediate feedback on successful login
- Consistent interface across pages
- Easy navigation between main sections
- Professional visual design with gradients and icons

## Benefits

- **Seamless Experience**: Users can navigate freely between pages
- **Consistent Interface**: Same login information on all pages
- **Visual Feedback**: Clear indication of login status
- **Mobile Friendly**: Responsive navigation on all devices
- **Professional Design**: Modern UI with success messages
