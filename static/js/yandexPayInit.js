// document.addEventListener('DOMContentLoaded', function() {
//     // Example cart data, replace with your actual cart/order info
//     const paymentData = {
//         version: 1,
//         publicId: 'YOUR_YANDEX_PAY_PUBLIC_ID', // Replace with your public ID
//         merchant: {
//             id: 'YOUR_MERCHANT_ID', // Replace with your merchant ID
//             name: 'Samin Shop'
//         },
//         order: {
//             number: 'ORDER_ID', // Generate/order number
//             amount: 1000, // Amount in kopecks (e.g., 1000 = 10 RUB)
//             currency: 'RUB',
//             items: [
//                 {
//                     label: 'Product Name',
//                     price: 1000,
//                     quantity: 1,
//                     amount: 1000
//                 }
//             ]
//         },
//         paymentMethods: ['CARD'],
//         confirmation: {
//             type: 'redirect',
//             returnUrl: 'http://127.0.0.1:5000/payment-success'
//         }
//     };

//     const checkout = window.YandexPay.createCheckout(paymentData);

//     checkout.render('yandex-pay-container');

//     checkout.on('success', function(event) {
//         // Send payment info to backend for processing
//         fetch('/yandex-pay-callback', {
//             method: 'POST',
//             headers: {'Content-Type': 'application/json'},
//             body: JSON.stringify(event.detail)
//         }).then(res => res.json())
//           .then(data => {
//               if (data.status === 'ok') {
//                   window.location.href = '/payment-success';
//               } else {
//                   alert('Ошибка при обработке платежа');
//               }
//           });
//     });
// });
// function onYaPayLoad() {
//   const YaPay = window.YaPay;

//   // Данные платежа
//   const paymentData = {
//     // Для отладки нужно явно указать `SANDBOX` окружение,
//     // для продакшена параметр можно убрать или указать `PRODUCTION`
//     env: YaPay.PaymentEnv.Sandbox,

//     // Версия 4 указывает на тип оплаты сервисом Яндекс Пэй
//     // Пользователь производит оплату на форме Яндекс Пэй,
//     // и мерчанту возвращается только результат проведения оплаты
//     version: 4,

//     // Код валюты в которой будете принимать платежи
//     currencyCode: YaPay.CurrencyCode.Rub,

//     // Идентификатор продавца, который получают при регистрации в Яндекс Пэй
//     merchantId: "54281716-0b74-4b0e-bf61-bc6c45b67f5c",

//     // Сумма к оплате
//     // Сумма которая будет отображена на форме зависит от суммы переданной от бэкенда
//     // Эта сумма влияет на отображение доступности Сплита
//     totalAmount: "15980.00",

//     // Доступные для использования методы оплаты
//     // Доступные на форме способы оплаты также зависят от информации переданной от бэкенда
//     // Данные передаваемые тут влияют на внешний вид кнопки или виджета
//     availablePaymentMethods: ["CARD", "SPLIT"],
//   };

//   // Обработчик на клик по кнопке
//   // Функция должна возвращать промис которые резолвит ссылку на оплату полученную от бэкенда Яндекс Пэй
//   // Подробнее про создание заказа: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post
//   async function onPayButtonClick() {
//     const orderData = {
//       orderId: "ORDER12345",
//       amount: {
//         value: "15980.00",
//         currency: "RUB"
//       },
//       currencyCode: "RUB",
//       cart: {
//         items: [
//           {
//             productId: "sku-1",
//             name: "Орех грецкий очищенный",
//             quantity: "1", // ✅ обязательно строка!
//             price: {
//               amount: "15980.00",
//               currency: "RUB"
//             },
//             total: "15980.00", // ✅ просто строка!
//             tax: "none"
//           }
//         ],
//         total: {
//           label: "Итого",
//           amount: {
//             value: "15980.00", // ✅ обязательно value, не amount
//             currency: "RUB"
//           }
//         }
//       },
//       merchantId: "54281716-0b74-4b0e-bf61-bc6c45b67f5c",
//       description: "Order from Samin Shop",
//       confirmation: {
//         type: "redirect",
//         returnUrl: "http://127.0.0.1:5000/payment-success"
//       }
//     };

//     console.log("Quantity type:", typeof orderData.cart.items[0].quantity);

//     const response = await fetch("/api/create-yandex-pay-order", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(orderData),
//     });

//     const data = await response.json();

//     if (data.payment_url) {
//       return data.payment_url;
//     } else {
//       throw new Error(
//         "Failed to create Yandex Pay order: " + (data.error || "Unknown error")
//       );
//     }
//   }

//   // Обработчик на ошибки при открытии формы оплаты
//   function onFormOpenError(reason) {
//     // Выводим информацию о недоступности оплаты в данный момент
//     // и предлагаем пользователю другой способ оплаты.
//     console.error(`Payment error — ${reason}`);
//   }

//   // Создаем платежную сессию
//   YaPay.createSession(paymentData, {
//     onPayButtonClick: onPayButtonClick,
//     onFormOpenError: onFormOpenError,
//   })
//     .then(function (paymentSession) {
//       // Показываем кнопку Яндекс Пэй на странице.
//       paymentSession.mountButton(document.querySelector("#yandex-pay-button"), {
//         type: YaPay.ButtonType.Pay,
//         theme: YaPay.ButtonTheme.Black,
//         width: YaPay.ButtonWidth.Auto,
//       });
//     })
//     .catch(function (err) {
//       // Не получилось создать платежную сессию.
//     });
// }

// onYaPayLoad();

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

    console.log("Cart items:", cartItems);
    console.log("Subtotal:", subtotal);
    console.log("Delivery cost:", delivery);
    console.log("Final total:", total);

    const payload = {
      cart: cartItems,
      total: total,
      subtotal: subtotal.toFixed(2),
      delivery: delivery.toFixed(2),
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
