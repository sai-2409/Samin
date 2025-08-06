// New onPayButtonClick
function onYaPayLoad() {
  const YaPay = window.YaPay;

  const paymentData = {
    env: YaPay.PaymentEnv.Sandbox,
    version: 4,
    currencyCode: YaPay.CurrencyCode.Rub,
    merchantId: "54281716-0b74-4b0e-bf61-bc6c45b67f5c",
    totalAmount: "15980.00", // Можно любую сумму для внешнего отображения
    availablePaymentMethods: ["CARD", "SPLIT"],
  };

  async function onPayButtonClick() {
    // Try to get cart data from both possible sources
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    let cartTotal = localStorage.getItem("cartTotal") || "0.00";

    // If cartItems is empty, try to get from 'cart'
    if (cartItems.length === 0) {
      const cartData = JSON.parse(localStorage.getItem("cart")) || [];
      cartItems = cartData;
    }

    // Calculate subtotal from cart items
    let subtotal = 0;
    if (cartItems.length > 0) {
      subtotal = cartItems.reduce(
        (sum, item) => sum + parseFloat(item.price) * parseInt(item.quantity),
        0
      );
    }

    // Calculate delivery price (same logic as in your cart script)
    let delivery = 0;
    if (subtotal > 5000) {
      delivery = 0; // Free delivery for orders over 5000₽
    } else if (subtotal > 0) {
      delivery = Math.ceil(subtotal * 0.15); // 15% delivery cost
    }

    // Calculate final total including delivery
    const total = (subtotal + delivery).toFixed(2);

    // Collect delivery information
    const selectedAddressId = localStorage.getItem("selectedAddressId");
    const savedAddresses =
      JSON.parse(localStorage.getItem("savedAddresses")) || [];
    const selectedAddress = savedAddresses.find(
      (addr) => addr.id === parseInt(selectedAddressId)
    );

    // Get delivery date
    const activeDateBtn = document.querySelector(".payment__date-btn--active");
    const deliveryDate = activeDateBtn
      ? activeDateBtn.textContent.trim()
      : "Не выбрана";

    // Get delivery notes
    const deliveryNotes = [];
    const toggles = document.querySelectorAll(
      '.payment__toggle input[type="checkbox"]'
    );

    if (toggles.length >= 3) {
      const leaveAtDoor = toggles[0].checked;
      const handToPerson = toggles[1].checked;
      const dontCall = toggles[2].checked;

      if (leaveAtDoor) deliveryNotes.push("Оставить у двери");
      if (handToPerson) deliveryNotes.push("Передать на руки");
      if (dontCall) deliveryNotes.push("Не звонить");
    }

    // Get customer information
    const customerInfo = {
      name: selectedAddress ? selectedAddress.fullName : "Не указано",
      phone: selectedAddress ? selectedAddress.phone : "Не указано",
      address: selectedAddress
        ? `${selectedAddress.street}, д${selectedAddress.building}, кв${selectedAddress.flat}, ${selectedAddress.city}`
        : "Не указано",
      zipCode: selectedAddress ? selectedAddress.zipCode : "Не указано",
    };

    // console.log("Cart items:", cartItems);
    // console.log("Subtotal:", subtotal);
    // console.log("Delivery cost:", delivery);
    // console.log("Final total:", total);
    // console.log("Delivery date:", deliveryDate);
    // console.log("Delivery notes:", deliveryNotes);
    // console.log("Customer info:", customerInfo);

    const payload = {
      cart: cartItems,
      total: total,
      subtotal: subtotal.toFixed(2),
      delivery: delivery.toFixed(2),
      deliveryDate: deliveryDate,
      deliveryNotes: deliveryNotes,
      customerInfo: customerInfo,
      selectedAddressId: selectedAddressId,
    };

    const response = await fetch("/api/create-yandex-pay-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (data?.data?.paymentUrl) {
      return data.data.paymentUrl;
    } else {
      console.error("Ошибка при создании заказа:", data);
      throw new Error("Не удалось создать заказ через Яндекс Пэй");
    }
  }

  function onFormOpenError(reason) {
    console.error(`Ошибка отображения формы: ${reason}`);
  }

  YaPay.createSession(paymentData, {
    onPayButtonClick,
    onFormOpenError,
  })
    .then(function (paymentSession) {
      paymentSession.mountButton(document.querySelector("#yandex-pay-button"), {
        type: YaPay.ButtonType.Pay,
        theme: YaPay.ButtonTheme.Black,
        width: YaPay.ButtonWidth.Auto,
      });
    })
    .catch(function (err) {
      console.error("Ошибка при создании сессии Яндекс Пэй:", err);
    });
}

// ВАЖНО: вызываем функцию!
onYaPayLoad();
