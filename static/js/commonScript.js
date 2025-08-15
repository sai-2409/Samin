function getTotalCartQuantity() {
  const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
  return cartItems.reduce((sum, item) => sum + item.quantity, 0);

  console.log("Total cart quantity:", totalQuantity);
}
getTotalCartQuantity();

// Updating the floating cart counter
function updateFloatingCartCounter() {
  const counter = document.querySelector(".floating__cart-counter");
  if (counter) {
    counter.textContent = getTotalCartQuantity();
  }
}

// Dropdown functionality for the company info in the footer
function toggleCompanyInfo() {
  const info = document.getElementById("company-info");
  info.classList.toggle("open");
}

// Notification system for users
function loadNotifications() {
  const user = document.querySelector("[data-user-login]");
  if (!user) return; // Only for logged-in users

  fetch("/api/get-notifications")
    .then((response) => response.json())
    .then((data) => {
      if (data.notifications && data.notifications.length > 0) {
        showNotificationBadge(data.notifications.length);
        displayNotifications(data.notifications);
      }
    })
    .catch((error) => {
      console.error("Error loading notifications:", error);
    });
}

function showNotificationBadge(count) {
  // Create or update notification badge
  let badge = document.getElementById("notification-badge");
  if (!badge) {
    badge = document.createElement("div");
    badge.id = "notification-badge";
    badge.className =
      "fixed top-4 right-4 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold z-50 cursor-pointer";
    badge.onclick = showNotificationPanel;
    document.body.appendChild(badge);
  }
  badge.textContent = count;
  badge.style.display = "flex";
}

function displayNotifications(notifications) {
  // Store notifications globally for the panel
  window.userNotifications = notifications;
}

function showNotificationPanel() {
  if (!window.userNotifications || window.userNotifications.length === 0)
    return;

  // Create notification panel
  const panel = document.createElement("div");
  panel.id = "notification-panel";
  panel.className =
    "fixed top-16 right-4 bg-white rounded-lg shadow-xl border max-w-sm w-full";
  panel.style.zIndex = "99999";

  let panelHTML = `
    <div class="p-4 border-b">
      <h3 class="font-semibold text-gray-900">Уведомления</h3>
    </div>
    <div class="max-h-64 overflow-y-auto">
  `;

  window.userNotifications.forEach((notif) => {
    const time = new Date(notif.timestamp).toLocaleString("ru-RU");
    panelHTML += `
      <div class="p-3 border-b hover:bg-gray-50 cursor-pointer" onclick="markNotificationRead('${notif.id}')">
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h4 class="font-medium text-gray-900">${notif.title}</h4>
            <p class="text-sm text-gray-600 mt-1">${notif.message}</p>
            <p class="text-xs text-gray-400 mt-2">${time}</p>
          </div>
          <button onclick="markNotificationRead('${notif.id}')" class="text-gray-400 hover:text-gray-600 ml-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    `;
  });

  panelHTML += `
    </div>
    <div class="p-3 border-t">
      <button onclick="hideNotificationPanel()" class="text-sm text-gray-500 hover:text-gray-700">
        Закрыть
      </button>
    </div>
  `;

  panel.innerHTML = panelHTML;
  document.body.appendChild(panel);

  // Hide badge when panel is open
  const badge = document.getElementById("notification-badge");
  if (badge) badge.style.display = "none";
}

function hideNotificationPanel() {
  const panel = document.getElementById("notification-panel");
  if (panel) panel.remove();

  // Show badge again if there are still notifications
  if (window.userNotifications && window.userNotifications.length > 0) {
    const badge = document.getElementById("notification-badge");
    if (badge) badge.style.display = "flex";
  }
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
        // Remove notification from global array
        window.userNotifications = window.userNotifications.filter(
          (n) => n.id !== notificationId
        );

        // Update badge count
        if (window.userNotifications.length === 0) {
          const badge = document.getElementById("notification-badge");
          if (badge) badge.style.display = "none";
          hideNotificationPanel();
        } else {
          showNotificationBadge(window.userNotifications.length);
        }
      }
    })
    .catch((error) => {
      console.error("Error marking notification as read:", error);
    });
}

// Responsive header functionality
function initializeResponsiveHeader() {
  const toggleBtn = document.getElementById("toggleBtn");
  const closeBtn = document.getElementById("closeBtn");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");

  if (!toggleBtn || !closeBtn || !sidebar || !overlay) {
    return; // Elements don't exist on this page
  }

  // Close sidebar when a link is clicked
  sidebar.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      sidebar.classList.remove("open");
      overlay.classList.remove("show");
    });
  });

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.add("open");
    overlay.classList.add("show");
  });

  closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
  });

  overlay.addEventListener("click", () => {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
  });
}

// Change Yandex ID button text for small screens
function updateYandexButtonText() {
  const yandexButton = document.querySelector(
    ".header__button-yandexID-small-screens"
  );
  if (yandexButton) {
    if (window.innerWidth <= 900) {
      // Small screens - show "Войти"
      yandexButton.innerHTML =
        '<img src="/static/images/logos/yandex-market-svg-logo-white.svg" width="30px" height="30px" alt="Yandex ID">Войти';
    } else {
      // Large screens - show original content
      yandexButton.innerHTML =
        '<img src="/static/images/logos/yandex-market-svg-logo-white.svg" width="30px" height="30px" alt="Yandex ID">Войти c Яндекс ID';
    }
  }
}

// Load notifications when page loads
document.addEventListener("DOMContentLoaded", function () {
  loadNotifications();
  initializeResponsiveHeader();

  // Update Yandex button text on page load
  updateYandexButtonText();

  // Check for new notifications every 30 seconds
  setInterval(loadNotifications, 30000);
});

// Update button text on window resize
window.addEventListener("resize", updateYandexButtonText);
