document.addEventListener('DOMContentLoaded', () => {
    const roomName = window.location.pathname.split('/').filter(Boolean).pop();

    if (!roomName || isNaN(roomName)) {
        console.error('Invalid room ID');
        return;
    }

    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socketUrl = `${wsScheme}://${window.location.host}/ws/chat/${roomName}/`;

    const chatSocket = new WebSocket(socketUrl);

    chatSocket.onopen = () => {
        console.log('WebSocket connected');
        // Отправляем токен аутентификации если нужно
        const token = localStorage.getItem('access_token');
        if (token) {
            chatSocket.send(JSON.stringify({
                'type': 'auth',
                'token': token
            }));
        }
    };

    chatSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    chatSocket.onclose = (event) => {
        console.log('WebSocket closed:', event);
        if (!event.wasClean) {
            // Пытаемся переподключиться через 5 секунд
            setTimeout(() => window.location.reload(), 5000);
        }
    };

    chatSocket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const chatLog = document.getElementById('chat-log');

            if (chatLog) {
                const messageElem = document.createElement('div');
                messageElem.classList.add('message');
                messageElem.innerHTML = `
                    <strong>${data.username || 'Пользователь'}:</strong>
                    <span>${data.message}</span>
                    <small>${new Date().toLocaleTimeString()}</small>
                `;
                chatLog.appendChild(messageElem);
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        } catch (e) {
            console.error('Ошибка при обработке сообщения:', e);
        }
    };

    // Функция отправки сообщения
    function sendMessage(message) {
        if (chatSocket.readyState === WebSocket.OPEN) {
            const messageData = {
                message: message,
                // Добавляем CSRF токен если нужно
                // csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value
            };
            chatSocket.send(JSON.stringify(messageData));
        } else {
            console.error('WebSocket не подключён');
            setTimeout(() => sendMessage(message), 1000); // Попробовать снова через секунду
        }
    }

    // Обработчики UI
    const sendButton = document.getElementById('chat-message-send');
    const messageInput = document.getElementById('chat-message-input');

    if (sendButton && messageInput) {
        sendButton.addEventListener('click', () => {
            const message = messageInput.value.trim();
            if (message) {
                sendMessage(message);
                messageInput.value = '';
            }
        });

        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const message = messageInput.value.trim();
                if (message) {
                    sendMessage(message);
                    messageInput.value = '';
                }
            }
        });
    }
});