const socket = io.connect(window.location.origin);

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










import { useEffect, useState } from "react";

function App() {
  let [count, setCount] = useState(0);

  // Corrected the handle function to update count
  function handle() {
    setCount(count + 1); // Increment count when button is clicked
  }

  useEffect(() => {
    console.log("this is useEffect hook.");
  }, [count]); // This will run every time count changes

  return (
    <div>
      <h1>count: {count}</h1>
      <button onClick={handle}>Increment</button> {/* Updated the button text */}
    </div>
  );
}

export default App;