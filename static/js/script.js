// Coding JS code for the index.html
// Setting variables for the first time
const header = document.querySelector(".header");
const headerCart = document.querySelector(".header__cart");
const nav = document.querySelector(".nav");
// const navHeight = nav.getBoundingClientRect().height;
const headerButton = document.querySelector(".header__button");
const headerButton2 = document.querySelector(".mbutton1");
const headerButtonCalc = document.querySelector(".mbutton2");
const section3 = document.getElementById("section__3");
const sectionCalc = document.getElementById("section__calc");
const floatingCart = document.querySelector(".floating__cart-go");

// Going to the cart with headerCart
headerCart.addEventListener("click", function () {
  window.location.href = "/cart";
});
// Going to the cart with floating cart
floatingCart.addEventListener("click", function () {
  window.location.href = "/cart";
});

// Coding for the logout button

// Scrolling to Menu section with headerButton
headerButton.addEventListener("click", function () {
  section3.scrollIntoView({ behavior: "smooth" });
});
// Scrolling to Menu from another common button
headerButton2.addEventListener("click", function () {
  section3.scrollIntoView({ behavior: "smooth" });
});
// Scrolling  to Calculator section with headerButton
headerButtonCalc.addEventListener("click", function () {
  sectionCalc.scrollIntoView({ behavior: "smooth" });
});

// Fixing the header to be sticky
const stickyObserver = new IntersectionObserver(
  ([entry]) => {
    if (!entry.isIntersecting) {
      nav.classList.add("sticky");
    } else {
      nav.classList.remove("sticky");
    }
  },
  {
    root: null,
    threshold: 0,
    rootMargin: "-1px", // чтобы сработало сразу как ушло
  }
);
stickyObserver.observe(header);

// Fixing the header to be sticky

// Making menu fade animation
const HandleHover = function (e) {
  if (e.target.classList.contains("nav__link")) {
    const link = e.target;
    const siblings = link.closest(".nav").querySelectorAll(".nav__link");
    const logo = link.closest(".nav").querySelector(".header__logo");

    siblings.forEach((el) => {
      if (el !== link) el.style.opacity = this;
    });
    logo.style.opacity = this;
  }
};

nav.addEventListener("mouseover", HandleHover.bind(0.5));
nav.addEventListener("mouseout", HandleHover.bind(1));
// Making menu fade animation

// I should fix this code (slider for cards, functionalities, etc.)

// Working with counter for the Cart and this shit is working man for now !
// const cartCounter = document.querySelector('.floating__cart-counter');
// const btnCart = document.querySelectorAll('.card__cart');

// btnCart.forEach((btnItem) => {
//   btnItem.addEventListener('click', () => {
//     let currentCount = parseInt(cartCounter.textContent);
//     cartCounter.textContent = currentCount + 1;
//   });
// });

// Reveal sections
const allSections = document.querySelectorAll(".section");

if (window.scrollY > 0) {
  // User is not at the top: show all sections immediately
  allSections.forEach((section) => section.classList.remove("section__hidden"));
} else {
  // User is at the top: use reveal animation
  const revealSection = function (entries, observer) {
    const [entry] = entries;
    if (!entry.isIntersecting) return;
    entry.target.classList.remove("section__hidden");
    observer.unobserve(entry.target);
  };
  const sectionObserver = new IntersectionObserver(revealSection, {
    root: null,
    threshold: 0,
  });
  allSections.forEach(function (section) {
    sectionObserver.observe(section);
    section.classList.add("section__hidden");
  });
}

// Coding slider for the cardsM
const sliders = document.querySelectorAll(".cardM__slider");

sliders.forEach((currentCard) => {
  const images = currentCard.querySelectorAll(".cardM__slider-img");
  let currentIndex = 0;
  let canSlide = true;

  currentCard.addEventListener("mousemove", (e) => {
    if (!canSlide) return; // Stop if not allowed yet

    const rect = currentCard.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const middle = rect.width / 2;

    if (x > middle && currentIndex < images.length - 1) {
      images[currentIndex].classList.remove("active");
      currentIndex++;
      images[currentIndex].classList.add("active");
      canSlide = false;
    } else if (x < middle && currentIndex > 0) {
      images[currentIndex].classList.remove("active");
      currentIndex--;
      images[currentIndex].classList.add("active");
      canSlide = false;
    }

    // Cooldown: allow sliding again after 1 second (1000ms)
    setTimeout(() => {
      canSlide = true;
    }, 400);
  });
});

// Wrirring code for changing card's product's size between 500 and 1000 gramms
// ✅ Код для выбора граммов
function setupCardSizeSwitching() {
  const sizeButtons = document.querySelectorAll(".cardM__size-button");

  sizeButtons.forEach((button) => {
    const parentCard = button.closest(".cardM");
    const allSizeButtons = parentCard.querySelectorAll(".cardM__size-button");
    const priceElement = parentCard.querySelector(".cardM__price");
    const imageElements = parentCard.querySelectorAll(".cardM__slider-img");

    const price500 = parentCard.getAttribute("data-price-500");
    const price1000 = parentCard.getAttribute("data-price-1000");
    const img500 = parentCard.getAttribute("data-img-500");
    const img1000 = parentCard.getAttribute("data-img-1000");

    const defaultButton = parentCard.querySelector(".cardM__size-1000");
    if (defaultButton) defaultButton.classList.add("cardM__size-active");

    button.addEventListener("click", function () {
      allSizeButtons.forEach((btn) =>
        btn.classList.remove("cardM__size-active")
      );
      button.classList.add("cardM__size-active");

      let newPrice = "";
      let newImageSrc = "";

      if (button.classList.contains("cardM__size-500")) {
        if (price500) newPrice = `${price500} ₽`;
        if (img500) newImageSrc = img500;
      } else if (button.classList.contains("cardM__size-1000")) {
        if (price1000) newPrice = `${price1000} ₽`;
        if (img1000) newImageSrc = img1000;
      }

      if (newPrice) priceElement.textContent = newPrice;

      // Replace the visible image with slide-in-from-left animation
      if (newImageSrc && imageElements.length > 0) {
        const currentActiveImage = imageElements[0];
        const parent = currentActiveImage.parentNode;

        // Track last direction for each card
        if (!parent.dataset.lastDirection) {
          parent.dataset.lastDirection = "left"; // default
        }

        // Determine direction
        let direction;
        if (button.classList.contains("cardM__size-1000")) {
          direction = "left"; // 1000 slides in from left
        } else {
          direction = "right"; // 500 slides in from right
        }

        // Clean up any temp images
        parent
          .querySelectorAll(".temp-animation-img")
          .forEach((img) => img.remove());

        // Create new image for animation
        const tempImg = currentActiveImage.cloneNode();
        tempImg.src = newImageSrc;
        tempImg.classList.add("temp-animation-img");
        tempImg.style.position = "absolute";
        tempImg.style.left = 0;
        tempImg.style.top = 0;
        tempImg.style.width = "100%";
        tempImg.style.height = "100%";
        tempImg.style.zIndex = 2;
        tempImg.style.pointerEvents = "none";
        tempImg.style.opacity = 1;
        tempImg.style.transform = `translateX(${
          direction === "left" ? "-100%" : "100%"
        })`;
        parent.appendChild(tempImg);

        // Make sure parent is positioned
        parent.style.position = "relative";
        currentActiveImage.style.position = "absolute";
        currentActiveImage.style.left = 0;
        currentActiveImage.style.top = 0;
        currentActiveImage.style.width = "100%";
        currentActiveImage.style.height = "100%";
        currentActiveImage.style.zIndex = 1;

        // Step 1: Slide in new image on top
        gsap.to(tempImg, {
          x: "0%",
          duration: 0.5,
          ease: "power2.inOut",
          onComplete: () => {
            // Step 2: Slide out old image underneath
            currentActiveImage.style.zIndex = 0;
            tempImg.style.zIndex = 1;
            gsap.to(currentActiveImage, {
              x: direction === "left" ? "100%" : "-100%",
              duration: 0.1, // much faster
              ease: "power2.in",
              onComplete: () => {
                // After animation, set main image to new src and reset styles
                currentActiveImage.src = newImageSrc;
                currentActiveImage.style.position = "";
                currentActiveImage.style.left = "";
                currentActiveImage.style.top = "";
                currentActiveImage.style.width = "";
                currentActiveImage.style.height = "";
                currentActiveImage.style.zIndex = "";
                currentActiveImage.style.transform = "";
                tempImg.remove();
                // Update last direction for this card
                parent.dataset.lastDirection = direction;
              },
            });
          },
        });

        // Update active class
        imageElements.forEach((img) => img.classList.remove("active"));
        currentActiveImage.classList.add("active");
      }
      // Recalculating the total certain item in the cart
      updateCardItemCounters();
    });
  });
}

setupCardSizeSwitching();
updateCardItemCounters();

// Playing with the cartCard Button
const cartCardButton = document.querySelector(".card__cart");
const cartCardAmount = document.querySelector(".card__cart-amount");

cartCardButton.addEventListener("click", function () {
  let currentCardAmount = parseInt(cartCardAmount.textContent);
  cartCardAmount.textContent = currentCardAmount + 1;

  cartCardAmount.style.opacity = 1;
});

// I don't know what am I doing
function setupItemAdding() {
  document.querySelectorAll(".card__cart").forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".cardM");
      const productName = card
        .querySelector(".cardM__title")
        .textContent.trim();
      const image = card.querySelector(".cardM__slider-img-first").src;
      const size =
        card.querySelector(".cardM__size-active")?.textContent || "1000гр";
      const price = parseInt(card.querySelector(".cardM__price").textContent);

      const newItem = { productName, image, size, price, quantity: 1 };

      // Получаем текущую корзину
      let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

      // 🔍 Проверим, есть ли уже такой товар (по productName + size)
      const existingIndex = cartItems.findIndex(
        (item) =>
          item.productName === newItem.productName && item.size === newItem.size
      );

      if (existingIndex !== -1) {
        // ✅ Такой товар уже есть — увеличиваем количество
        cartItems[existingIndex].quantity += 1;
      } else {
        // 🆕 Новый товар — добавляем
        cartItems.push(newItem);
      }

      // Сохраняем
      localStorage.setItem("cartItems", JSON.stringify(cartItems));
      updateFloatingCartCounter();
      updateCardItemCounters();

      const counter = document.querySelector(".floating__cart-counter");
      if (counter) {
        counter.classList.add("bump");
        setTimeout(() => counter.classList.remove("bump"), 400);
      }
    });
  });
}
setupItemAdding();

document.addEventListener("DOMContentLoaded", function () {
  const cartCounter = document.querySelector(".floating__cart-counter");
  if (cartCounter) {
    cartCounter.textContent = getTotalCartQuantity();
  }
});

getTotalCartQuantity();

// Recalculating the total certain item in the cart
function updateCardItemCounters() {
  const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

  document.querySelectorAll(".cardM").forEach((card) => {
    const productName = card.querySelector(".cardM__title").textContent.trim();
    const size =
      card.querySelector(".cardM__size-active")?.textContent || "1000гр";
    const counterElem = card.querySelector(".card__cart-amount");

    const matchingItem = cartItems.find(
      (item) => item.productName === productName && item.size === size
    );

    if (counterElem) {
      counterElem.textContent = matchingItem ? matchingItem.quantity : 0;
      counterElem.style.opacity = matchingItem ? 1 : 0;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  updateCardItemCounters();
});

// Almond animated background scroll effect for main section
// const mainSection = document.querySelector(".main");
// const almondBgScrollThreshold = 100; // px
// window.addEventListener("scroll", () => {
//   if (window.scrollY > almondBgScrollThreshold) {
//     mainSection.classList.add("show-almond-bg");
//   } else {
//     mainSection.classList.remove("show-almond-bg");
//   }
// });

// Making the sideBar menu
const toggleBtn = document.getElementById("toggleBtn");
const closeBtn = document.getElementById("closeBtn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

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

document.addEventListener("DOMContentLoaded", function () {
  const greeting = document.getElementById("welcome-greeting");
  if (greeting) {
    setTimeout(() => {
      greeting.remove();
    }, 2500); // Match the animation duration
  }
});

// User Reviews Functionality
function loadUserReviews() {
  const container = document.getElementById("userReviewsContainer");
  if (!container) return;

  // Show loading state
  container.innerHTML = `
    <div class="user-reviews-loading">
      <div style="margin-bottom: 20px; font-size: 20px; font-weight: 600;">Загрузка отзывов...</div>
      <div style="font-size: 16px; opacity: 0.8;">Находим лучшие отзывы наших покупателей</div>
    </div>
  `;

  // Fetch all reviews from the API
  fetch("/api/get-all-reviews")
    .then((response) => response.json())
    .then((data) => {
      if (data.reviews && data.reviews.length > 0) {
        displayUserReviews(data.reviews);
      } else {
        showEmptyReviews();
      }
    })
    .catch((error) => {
      console.error("Error loading reviews:", error);
      showEmptyReviews();
    });
}

function displayUserReviews(reviews) {
  const container = document.getElementById("userReviewsContainer");
  if (!container) return;

  // Sort reviews by date (newest first)
  const sortedReviews = reviews.sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );

  // Take only the first 6 reviews for display
  const displayReviews = sortedReviews.slice(0, 6);

  container.innerHTML = displayReviews
    .map(
      (review, index) => `
    <div class="user-review-card" style="animation-delay: ${index * 0.1}s">
      <div class="user-review-header">
        <div class="user-review-avatar">
          ${
            review.user_avatar
              ? `<img src="https://avatars.yandex.net/get-yapic/${review.user_avatar}/islands-retina-50" alt="Avatar">`
              : `<span>${getInitials(review.user_name)}</span>`
          }
        </div>
        <div class="user-review-info">
          <div class="user-review-name">${review.user_name}</div>
          <div class="user-review-date">${formatDate(review.timestamp)}</div>
        </div>
      </div>
      <div class="user-review-rating">
        ${generateStars(review.rating)}
      </div>
      <div class="user-review-text">${review.review_text}</div>
      ${
        review.image_filename
          ? `
      <div class="mt-2">
        <img src="/static/uploads/reviews/${review.image_filename}" 
             alt="Review image" 
             class="w-16 h-16 object-cover rounded cursor-pointer hover:opacity-80 transition-opacity"
             onclick="openImageModal('/static/uploads/reviews/${review.image_filename}')"
             title="Click to enlarge">
      </div>
      `
          : ""
      }
              <div class="user-review-product">
          <span style="font-weight: 600; color: var(--primary-color);">🏪</span> Отзыв о магазине Samin
        </div>
    </div>
  `
    )
    .join("");

  // Add hover effects and interactions
  setTimeout(() => {
    const cards = container.querySelectorAll(".user-review-card");
    cards.forEach((card) => {
      card.addEventListener("mouseenter", function () {
        this.style.transform = "translateY(-8px) scale(1.02)";
        this.style.boxShadow = "0 30px 60px rgba(0, 0, 0, 0.15)";
      });

      card.addEventListener("mouseleave", function () {
        this.style.transform = "translateY(0) scale(1)";
        this.style.boxShadow = "0 20px 40px rgba(0, 0, 0, 0.1)";
      });
    });
  }, 100);
}

function showEmptyReviews() {
  const container = document.getElementById("userReviewsContainer");
  if (!container) return;

  container.innerHTML = `
    <div class="user-reviews-empty">
      <div class="user-reviews-empty-icon">🌟</div>
      <p style="font-size: 18px; margin-bottom: 15px; font-weight: 600;">Пока нет отзывов от покупателей</p>
      <p style="font-size: 16px; opacity: 0.9;">Будьте первым, кто оставит отзыв и получите скидку!</p>
      <div style="margin-top: 25px;">
        <span style="background: rgba(255, 255, 255, 0.2); padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 500;">
          🎁 Специальное предложение для первых отзывов
        </span>
      </div>
    </div>
  `;
}

function getInitials(name) {
  if (!name) return "А";
  return name
    .split(" ")
    .map((word) => word.charAt(0))
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

function generateStars(rating) {
  let stars = "";
  for (let i = 1; i <= 5; i++) {
    stars += `<span class="user-review-star">${i <= rating ? "★" : "☆"}</span>`;
  }
  return stars;
}

function formatDate(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// Image modal functionality
function openImageModal(imageSrc) {
  const modal = document.createElement("div");
  modal.className =
    "fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50";
  modal.innerHTML = `
                <div class="relative max-w-4xl max-h-full p-4">
                  <button onclick="this.parentElement.parentElement.remove()" 
                          class="absolute top-2 right-2 text-white text-2xl hover:text-gray-300 z-10">
                    ✕
                  </button>
                  <img src="${imageSrc}" alt="Full size image" 
                       class="max-w-full max-h-full object-contain rounded-lg">
                </div>
              `;
  document.body.appendChild(modal);

  // Close modal on background click
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.remove();
    }
  });
}

// Load user reviews when page loads
document.addEventListener("DOMContentLoaded", function () {
  loadUserReviews();
});
