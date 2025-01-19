const socketFlashBox = (socket) => {
  socket.on('flash', function (data) {
    const flashBbox = document.getElementById('flash-box');

    if (!flashBbox) {
      return;
    }

    const socketFlashElement = document.createElement('div');
    socketFlashElement.classList.add("alert", "alert-" + data.category, "mb-0");

    const titleElement = document.createElement('h4');
    titleElement.innerText = data.title;
    titleElement.classList.add("alert-heading");

    const hrElement = document.createElement('hr');

    const textElement = document.createElement('p');
    textElement.innerText = data.text;

    socketFlashElement.appendChild(titleElement);
    socketFlashElement.appendChild(hrElement);
    socketFlashElement.appendChild(textElement);
    flashBbox.append(socketFlashElement);

    setTimeout(() => {
      socketFlashElement.remove();
    }, 10000);

    if (data.type === "notification") {
        document.getElementById('notification-bell').classList.add("active");
    }

    playNotificationSound();
  });
}

const connectNotificationBell = (socket) => {
  document.getElementById('notification-bell').addEventListener('click', (e) => {
    e.target.classList.remove('active');

    const notifications = document.querySelectorAll('.notification[data-notification-id]');

    notifications.forEach(notification => {
      setTimeout(() => notification.classList.remove('active', 'border-light', 'bg-light'), 10000);
    });

    const notificationIds = Array.from(notifications).reduce((ids, notification) => {
      const id = notification.dataset.notificationId;

      if (id) {
        ids.push(id);
      }

      return ids;
    }, []);

    socket.emit("read_notifications", {notificationIds: notificationIds});
  })
}

const connectNotificationsList = (socket) => {
  socket.on("refresh_notifications", function (data) {
    const refreshedNotifications = data.notifications;
    const notificationsComponent = document.getElementById('notifications');

    if (!notificationsComponent) {
      return;
    }

    notificationsComponent.innerHTML = refreshedNotifications;
    connectNotificationBell(socket);
  });
}

// ORDERS TABLE
const connectOrdersSection = (socket) => {
  // Initial registration when the page loads
  registerEventListenersForOrdersTable(socket);

  socket.on("refresh_orders", function (data) {
    const refreshedOrders = data.orders;
    const ordersSection = document.getElementById('orders');

    if (!ordersSection) {
      return;
    }

    ordersSection.innerHTML = refreshedOrders;
    registerEventListenersForOrdersTable(socket);
  });
}

const registerEventListenersForOrdersTable = (socket) => {
  const ordersSection = document.getElementById('orders');

  if (!ordersSection) {
    return;
  }

  ordersSection.querySelectorAll('.orders-table-body select.change-status-select-box').forEach(select => {
    select.addEventListener('change', (e) => {
      socket.emit('order_status_changed', {
        orderId: e.target.dataset.orderId,
        newStatus: e.target.value,
        customerId: e.target.dataset.customerId,
      });
    });
  });
}

// SOUNDS
const playNotificationSound = () => {
  const notificationSound = new Audio('/static/audio/notification.wav');

  notificationSound.play().catch((error) => {
    console.error("Error playing notification sound:", error);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', unlockAudio, {once: true});
});

const unlockAudio = () => {
  const silentAudio = new Audio();

  silentAudio.play().catch(() => {
    console.log("User interaction required to unlock audio playback.");
  });
}
