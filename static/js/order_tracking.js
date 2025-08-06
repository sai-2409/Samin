// Order Tracking JavaScript

class OrderTracker {
  constructor() {
    this.currentStep = 2; // Start at "Paid" step
    this.steps = [
      { id: 1, name: "Заказ оформлен", status: "completed" },
      { id: 2, name: "Оплачен", status: "completed" },
      { id: 3, name: "Упаковка", status: "current" },
      { id: 4, name: "Отправлен", status: "pending" },
      { id: 5, name: "Доставлен", status: "pending" },
    ];
    this.init();
  }

  init() {
    this.updateProgressLine();
    this.setupRefreshButton();
    this.animateSteps();
    // this.simulateProgress(); // Disabled - will be controlled by admin dashboard later
  }

  updateProgressLine() {
    const progressLine = document.querySelector(".progress-tracker::after");
    if (progressLine) {
      const progressPercentage = (this.currentStep / this.steps.length) * 100;
      document.documentElement.style.setProperty(
        "--progress-width",
        `${progressPercentage}%`
      );
    }
  }

  updateStepStatus(stepId, status) {
    const step = document.querySelector(`[data-step="${stepId}"]`);
    if (step) {
      // Remove all status classes
      step.classList.remove("completed", "current", "pending");
      // Add new status class
      step.classList.add(status);

      // Update icon based on status
      const icon = step.querySelector(".step-icon");
      if (icon) {
        icon.innerHTML = this.getIconForStatus(status);
      }
    }
  }

  getIconForStatus(status) {
    switch (status) {
      case "completed":
        return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 12l2 2 4-4"/>
                </svg>`;
      case "current":
        return `<div class="loading-spinner"></div>`;
      case "pending":
        return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                </svg>`;
      default:
        return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                </svg>`;
    }
  }

  animateSteps() {
    const steps = document.querySelectorAll(".step");
    steps.forEach((step, index) => {
      step.style.animationDelay = `${index * 0.2}s`;
      step.classList.add("fade-in");
    });
  }

  // simulateProgress() {
  //   // Simulate order progress over time
  //   const progressIntervals = [
  //     { step: 3, delay: 5000 }, // Packing after 5 seconds
  //     { step: 4, delay: 10000 }, // Shipped after 10 seconds
  //     { step: 5, delay: 15000 }, // Delivered after 15 seconds
  //   ];

  //   progressIntervals.forEach(({ step, delay }) => {
  //     setTimeout(() => {
  //       this.advanceToStep(step);
  //     }, delay);
  //   });
  // }

  advanceToStep(stepId) {
    if (stepId > this.currentStep) {
      // Mark current step as completed
      this.updateStepStatus(this.currentStep, "completed");

      // Update current step
      this.currentStep = stepId;
      this.updateStepStatus(stepId, "current");

      // Update progress line
      this.updateProgressLine();

      // Show notification
      this.showNotification(
        `Заказ перешел на этап: ${this.steps[stepId - 1].name}`
      );
    }
  }

  showNotification(message) {
    // Create notification element
    const notification = document.createElement("div");
    notification.className = "notification";
    notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">📦</span>
                <span class="notification-text">${message}</span>
            </div>
        `;

    // Add styles
    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #ff6b35, #ff8c42);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            max-width: 300px;
        `;

    // Add to page
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
      notification.style.transform = "translateX(0)";
    }, 100);

    // Remove after 3 seconds
    setTimeout(() => {
      notification.style.transform = "translateX(100%)";
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 300);
    }, 3000);
  }

  setupRefreshButton() {
    const refreshBtn = document.querySelector(".btn-primary");
    if (refreshBtn) {
      refreshBtn.addEventListener("click", () => {
        this.refreshTracking();
      });
    }
  }

  refreshTracking() {
    const btn = document.querySelector(".btn-primary");
    const originalText = btn.textContent;

    // Show loading state
    btn.textContent = "Обновление...";
    btn.disabled = true;

    // Simulate API call
    setTimeout(() => {
      // Check for new status updates
      this.checkForUpdates();

      // Restore button
      btn.textContent = originalText;
      btn.disabled = false;

      // Show success message
      this.showNotification("Статус заказа обновлен");
    }, 2000);
  }

  checkForUpdates() {
    // This would normally make an API call to check for status updates
    // For now, disabled automatic updates - will be controlled by admin dashboard
    console.log("Checking for updates... (disabled for admin control)");
    // const random = Math.random();
    // if (random > 0.7 && this.currentStep < 5) {
    //   this.advanceToStep(this.currentStep + 1);
    // }
  }

  // Method to manually set order status (for testing)
  setOrderStatus(status) {
    const statusMap = {
      placed: 1,
      paid: 2,
      packing: 3,
      shipped: 4,
      delivered: 5,
    };

    const targetStep = statusMap[status];
    if (targetStep) {
      // Reset all steps
      for (let i = 1; i <= 5; i++) {
        if (i < targetStep) {
          this.updateStepStatus(i, "completed");
        } else if (i === targetStep) {
          this.updateStepStatus(i, "current");
        } else {
          this.updateStepStatus(i, "pending");
        }
      }
      this.currentStep = targetStep;
      this.updateProgressLine();
    }
  }
}

// Initialize order tracker when page loads
document.addEventListener("DOMContentLoaded", function () {
  const tracker = new OrderTracker();

  // Make tracker globally available for testing
  window.orderTracker = tracker;

  // Add fade-in animation to steps
  const steps = document.querySelectorAll(".step");
  steps.forEach((step, index) => {
    step.style.opacity = "0";
    step.style.transform = "translateY(20px)";

    setTimeout(() => {
      step.style.transition = "all 0.5s ease";
      step.style.opacity = "1";
      step.style.transform = "translateY(0)";
    }, index * 200);
  });
});

// Global function for refreshing tracking
function refreshTracking() {
  if (window.orderTracker) {
    window.orderTracker.refreshTracking();
  }
}

// Add some CSS for the fade-in animation
const style = document.createElement("style");
style.textContent = `
    .step {
        transition: all 0.5s ease;
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .notification-icon {
        font-size: 1.2rem;
    }
    
    .notification-text {
        font-weight: 500;
    }
`;
document.head.appendChild(style);
