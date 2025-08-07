# Address Selection Modal Features

## Overview

Modal that appears when users try to pay without selecting a delivery address, ensuring complete order information.

## 🎯 **Functionality**

### **Modal Trigger**

- **Payment Button Click**: Modal appears when user clicks pay button without address
- **Address Validation**: Checks both saved addresses and form fields
- **Prevents Payment**: Stops payment process until address is selected

### **Address Validation Logic**

1. **Saved Address Check**: First checks if a saved address is selected
2. **Form Fields Check**: Validates if address form fields are filled
3. **Complete Address**: Requires street, building, flat, and city

## 🎨 **Modal Design**

### **Visual Elements**

- **Warning Icon**: ⚠️ Attention icon in header
- **Clear Message**: "Выберите пожалуйста адрес доставки чтобы мы смогли привезти ваши орешки"
- **Action Button**: "Понятно" button to close modal
- **Close Button**: × button in top-right corner

### **Styling Features**

- **Centered Modal**: Appears in center of screen
- **Overlay Background**: Semi-transparent dark overlay
- **Brand Colors**: Uses Samin's orange color scheme
- **Responsive Design**: Adapts to mobile screens

## 🔧 **Technical Implementation**

### **HTML Structure**

```html
<div id="address-modal" class="address-modal" style="display: none">
  <div class="address-modal__overlay"></div>
  <div class="address-modal__content">
    <div class="address-modal__header">
      <h3 class="address-modal__title">⚠️ Внимание</h3>
      <button class="address-modal__close" onclick="hideAddressModal()">
        ×
      </button>
    </div>
    <div class="address-modal__body">
      <p class="address-modal__message">
        Выберите пожалуйста адрес доставки чтобы мы смогли привезти ваши орешки
      </p>
    </div>
    <div class="address-modal__footer">
      <button class="address-modal__btn" onclick="hideAddressModal()">
        Понятно
      </button>
    </div>
  </div>
</div>
```

### **CSS Classes**

- **`.address-modal`**: Main modal container
- **`.address-modal__overlay`**: Background overlay
- **`.address-modal__content`**: Modal content box
- **`.address-modal__header`**: Header with title and close button
- **`.address-modal__body`**: Message content area
- **`.address-modal__footer`**: Button area
- **`.address-modal__btn`**: Action button styling

### **JavaScript Functions**

#### **`showAddressModal()`**

- Displays the modal
- Adds event listeners for closing
- Handles Escape key press

#### **`hideAddressModal()`**

- Hides the modal
- Removes event listeners

#### **`isAddressSelected()`**

- Checks for selected saved address
- Validates form field completion
- Returns boolean for address validity

## 🎯 **User Experience**

### **Modal Behavior**

- **Auto-close**: Click overlay or Escape key to close
- **Button Close**: "Понятно" button closes modal
- **Prevents Payment**: Payment process stops until address selected
- **Clear Guidance**: Clear message explains what user needs to do

### **Address Validation**

- **Saved Addresses**: Checks if user selected a saved address
- **Form Completion**: Validates all required address fields
- **Flexible Logic**: Works with both address selection methods

## 📱 **Responsive Design**

### **Mobile Optimizations**

- **Smaller Padding**: Reduced padding on mobile
- **Full Width**: Modal takes 95% width on mobile
- **Touch Friendly**: Large touch targets for buttons
- **Readable Text**: Proper font sizes for mobile

## 🔗 **Integration**

### **Payment Flow**

1. User clicks "Pay" button
2. System checks `isAddressSelected()`
3. If no address: shows modal, stops payment
4. If address selected: proceeds with payment

### **Address Systems**

- **Saved Addresses**: Works with existing saved address system
- **Form Addresses**: Validates manually entered addresses
- **Local Storage**: Integrates with existing address storage

## 🎨 **Design Features**

### **Color Scheme**

- **Primary Orange**: `#ff6b35` (Samin brand color)
- **Hover Orange**: `#e55a2b` (darker shade)
- **Text Colors**: Dark gray for readability
- **Background**: White modal with shadow

### **Typography**

- **Header**: 20px, bold weight
- **Message**: 16px, regular weight
- **Button**: 16px, medium weight
- **Proper Spacing**: Consistent padding and margins

## 🚀 **Benefits**

### **For Users**

- **Clear Guidance**: Knows exactly what to do
- **No Confusion**: Prevents incomplete orders
- **Easy Dismissal**: Multiple ways to close modal
- **Mobile Friendly**: Works on all devices

### **For Business**

- **Complete Orders**: Ensures delivery information
- **Reduced Errors**: Prevents incomplete address orders
- **Better UX**: Clear user guidance
- **Brand Consistency**: Matches Samin design

## 🔧 **Technical Details**

### **Event Handling**

- **Click Events**: Overlay and button clicks
- **Keyboard Events**: Escape key support
- **Form Validation**: Real-time address checking
- **Payment Integration**: Seamless payment flow

### **Storage Integration**

- **Local Storage**: Works with existing address storage
- **Address Selection**: Integrates with saved address system
- **Form Data**: Validates manually entered addresses
- **State Management**: Maintains modal state

The address selection modal ensures users provide complete delivery information before proceeding with payment, improving order completion rates and user experience.
