const socket = io();

console.log("scripts.js loaded");

socket.on("connect", () => {
    console.log("Connected:", socket.id);
});

socket.on("disconnect", () => {
    console.log("Disconnected");
});

document.getElementById('message-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message) {
        socket.emit('message', { data: message });
        messageInput.value = '';
    }
});

socket.on('message', function(data) {
    const messagesDiv = document.getElementById('messages');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    messageDiv.innerHTML = `<strong>${data.name}:</strong> ${data.message}`;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});
