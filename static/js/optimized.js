/* ===== OPTIMIZED JAVASCRIPT - CONSOLIDATED FUNCTIONS ===== */

// ===== GLOBAL VARIABLES =====
let notifications = [];
let notificationPanelVisible = false;

// ===== UTILITY FUNCTIONS =====
function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;

  // Add styles
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    z-index: 10000;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    max-width: 300px;
    word-wrap: break-word;
  `;

  // Set background color based on type
  const colors = {
    success: "#4caf50",
    error: "#f44336",
    warning: "#ff9800",
    info: "#2196f3",
  };
  notification.style.backgroundColor = colors[type] || colors.info;

  document.body.appendChild(notification);

  // Animate in
  setTimeout(() => {
    notification.style.transform = "translateX(0)";
  }, 100);

  // Remove after 5 seconds
  setTimeout(() => {
    notification.style.transform = "translateX(100%)";
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 5000);
}

// ===== NOTIFICATION SYSTEM =====
function toggleNotificationPanel() {
  const panel = document.getElementById("notification-panel");
  if (!panel) return;

  notificationPanelVisible = !notificationPanelVisible;

  if (notificationPanelVisible) {
    panel.classList.add("show");
    loadNotifications();
  } else {
    panel.classList.remove("show");
  }
}

function loadNotifications() {
  fetch("/api/get-notifications")
    .then((response) => response.json())
    .then((data) => {
      notifications = data.notifications || [];
      updateNotificationBadge();
      displayNotifications();
    })
    .catch((error) => {
      console.error("Error loading notifications:", error);
    });
}

function updateNotificationBadge() {
  const badge = document.querySelector(".notification-badge");
  if (!badge) return;

  const unreadCount = notifications.filter((n) => !n.read).length;

  if (unreadCount > 0) {
    badge.textContent = unreadCount > 99 ? "99+" : unreadCount;
    badge.style.display = "block";
  } else {
    badge.style.display = "none";
  }
}

function displayNotifications() {
  const list = document.getElementById("notification-list");
  if (!list) return;

  if (notifications.length === 0) {
    showEmptyNotifications();
    return;
  }

  list.innerHTML = notifications
    .map(
      (notification) => `
      <div class="notification-item ${notification.read ? "read" : "unread"}" 
           onclick="markNotificationRead('${notification.id}')">
        <div class="notification-title">${notification.title}</div>
        <div class="notification-message">${notification.message}</div>
        <div class="notification-time">${formatNotificationTime(
          notification.timestamp
        )}</div>
      </div>
    `
    )
    .join("");
}

function showEmptyNotifications() {
  const list = document.getElementById("notification-list");
  if (!list) return;

  list.innerHTML = `
    <div class="notification-empty">
      <svg viewBox="0 0 24 24">
        <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
      </svg>
      <p>Нет новых уведомлений</p>
    </div>
  `;
}

function markNotificationRead(notificationId) {
  fetch("/api/mark-notification-read", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      notification_id: notificationId,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        notifications = notifications.map((n) =>
          n.id === notificationId ? { ...n, read: true } : n
        );
        updateNotificationBadge();
        displayNotifications();
      }
    })
    .catch((error) => {
      console.error("Error marking notification as read:", error);
    });
}

function formatNotificationTime(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;

  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "Только что";
  if (minutes < 60) return `${minutes} мин назад`;
  if (hours < 24) return `${hours} ч назад`;
  if (days < 7) return `${days} дн назад`;

  return date.toLocaleDateString("ru-RU");
}

// ===== RESPONSIVE HEADER =====
function initializeResponsiveHeader() {
  const toggleBtn = document.getElementById("toggleBtn");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");
  const closeBtn = document.getElementById("closeBtn");

  if (!toggleBtn || !sidebar || !overlay || !closeBtn) return;

  function openSidebar() {
    sidebar.classList.add("active");
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeSidebar() {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  toggleBtn.addEventListener("click", openSidebar);
  closeBtn.addEventListener("click", closeSidebar);
  overlay.addEventListener("click", closeSidebar);

  // Close on escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeSidebar();
    }
  });
}

// ===== SCROLL ANIMATIONS =====
function initializeScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate-fade-in");
      }
    });
  }, observerOptions);

  // Observe all sections
  document.querySelectorAll(".section").forEach((section) => {
    observer.observe(section);
  });
}

// ===== CART FUNCTIONS =====
function updateCartCounter(count) {
  const counter = document.querySelector(".floating__cart-counter");
  if (!counter) return;

  counter.textContent = count;
  counter.classList.add("bump");

  setTimeout(() => {
    counter.classList.remove("bump");
  }, 300);
}

// ===== FORM VALIDATION =====
function validateForm(form) {
  const inputs = form.querySelectorAll(
    "input[required], select[required], textarea[required]"
  );
  let isValid = true;

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.classList.add("error");
      isValid = false;
    } else {
      input.classList.remove("error");
    }
  });

  return isValid;
}

// ===== MODAL FUNCTIONS =====
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (!modal) return;

  modal.style.display = "flex";
  document.body.style.overflow = "hidden";

  // Animate in
  setTimeout(() => {
    modal.classList.add("active");
  }, 10);
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (!modal) return;

  modal.classList.remove("active");

  setTimeout(() => {
    modal.style.display = "none";
    document.body.style.overflow = "";
  }, 300);
}

// ===== UTILITY FUNCTIONS =====
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function throttle(func, limit) {
  let inThrottle;
  return function () {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", function () {
  // Initialize responsive header
  initializeResponsiveHeader();

  // Initialize scroll animations
  initializeScrollAnimations();

  // Initialize notifications
  loadNotifications();

  // Check for new notifications every 30 seconds
  setInterval(loadNotifications, 30000);

  // Close notification panel when clicking outside
  document.addEventListener("click", function (event) {
    const panel = document.getElementById("notification-panel");
    const notificationIcon = document.querySelector(".floating-notifications");

    if (
      panel &&
      notificationIcon &&
      !panel.contains(event.target) &&
      !notificationIcon.contains(event.target)
    ) {
      panel.classList.remove("show");
      notificationPanelVisible = false;
    }
  });

  // Initialize form validation
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!validateForm(this)) {
        e.preventDefault();
        showNotification(
          "Пожалуйста, заполните все обязательные поля",
          "error"
        );
      }
    });
  });

  // Initialize modal close buttons
  document.querySelectorAll("[data-modal-close]").forEach((button) => {
    button.addEventListener("click", function () {
      const modalId = this.getAttribute("data-modal-close");
      closeModal(modalId);
    });
  });
});

// ===== EXPORT FOR MODULE USE =====
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    showNotification,
    toggleNotificationPanel,
    loadNotifications,
    updateNotificationBadge,
    displayNotifications,
    markNotificationRead,
    formatNotificationTime,
    initializeResponsiveHeader,
    initializeScrollAnimations,
    updateCartCounter,
    validateForm,
    openModal,
    closeModal,
    debounce,
    throttle,
  };
}
