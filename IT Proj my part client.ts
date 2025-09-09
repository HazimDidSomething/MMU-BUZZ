const DM_POLL_INTERVAL = 3000; // Poll every 3 seconds
let currentUser = 'user1'; // Replace with your authenticated user's ID
let recipientUser = null;
let lastMessageTimestamp = 0;

// Create DM UI
const dmContainer = document.createElement('div');
dmContainer.id = 'dm-container';
dmContainer.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 300px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    display: none;
    font-family: Arial, sans-serif;
`;
dmContainer.innerHTML = `
    <div id="dm-header" style="padding: 10px; background: #0084ff; color: white; border-radius: 8px 8px 0 0;">
        <span id="dm-recipient">Select User</span>
        <button id="dm-close" style="float: right; background: none; border: none; color: white; cursor: pointer;">X</button>
    </div>
    <div id="dm-messages" style="height: 200px; overflow-y: auto; padding: 10px;"></div>
    <input id="dm-input" type="text" placeholder="Type a message..." style="width: 60%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;">
    <button id="dm-send" style="padding: 8px; background: #0084ff; color: white; border: none; border-radius: 5px;">Send</button>
    <input id="dm-image" type="file" accept="image/*" style="display: none;">
    <button id="dm-image-btn" style="padding: 8px; background: #00cc44; color: white; border: none; border-radius: 5px;">Image</button>
    <input id="dm-video" type="file" accept="video/*" style="display: none;">
    <button id="dm-video-btn" style="padding: 8px; background: #ff4444; color: white; border: none; border-radius: 5px;">Video</button>
`;
document.body.appendChild(dmContainer);

// Toggle DM window
function toggleDM(recipient) {
    recipientUser = recipient;
    document.getElementById('dm-recipient').textContent = recipient;
    document.getElementById('dm-container').style.display = 'block';
    document.getElementById('dm-messages').innerHTML = '';
    lastMessageTimestamp = 0;
    loadMessages();
    startPolling();
}

// Close DM window
document.getElementById('dm-close').addEventListener('click', () => {
    document.getElementById('dm-container').style.display = 'none';
    recipientUser = null;
    stopPolling();
});

// Send text message
document.getElementById('dm-send').addEventListener('click', async () => {
    const messageInput = document.getElementById('dm-input');
    const message = messageInput.value.trim();
    if (message && recipientUser) {
        await fetch('/api/dm/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender: currentUser, recipient: recipientUser, message })
        });
        messageInput.value = '';
        loadMessages();
    }
});

// Send image
document.getElementById('dm-image-btn').addEventListener('click', () => {
    document.getElementById('dm-image').click();
});
document.getElementById('dm-image').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file && recipientUser) {
        const formData = new FormData();
        formData.append('media', file);
        formData.append('sender', currentUser);
        formData.append('recipient', recipientUser);
        formData.append('type', 'image');
        await fetch('/api/dm/send-media', {
            method: 'POST',
            body: formData
        });
        event.target.value = '';
        loadMessages();
    }
});

// Send video
document.getElementById('dm-video-btn').addEventListener('click', () => {
    document.getElementById('dm-video').click();
});
document.getElementById('dm-video').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file && recipientUser) {
        const formData = new FormData();
        formData.append('media', file);
        formData.append('sender', currentUser);
        formData.append('recipient', recipientUser);
        formData.append('type', 'video');
        await fetch('/api/dm/send-media', {
            method: 'POST',
            body: formData
        });
        event.target.value = '';
        loadMessages();
    }
});

// Load messages
async function loadMessages() {
    if (!recipientUser) return;
    const response = await fetch(`/api/dm/messages?sender=${currentUser}&recipient=${recipientUser}&since=${lastMessageTimestamp}`);
    const messages = await response.json();
    if (messages.length > 0) {
        const messagesDiv = document.getElementById('dm-messages');
        messages.forEach(data => {
            const messageDiv = document.createElement('div');
            messageDiv.style.cssText = `
                margin: 5px;
                padding: 8px;
                border-radius: 5px;
                ${data.sender === currentUser ? 'background: #0084ff; color: white; margin-left: 20%;' : 'background: #e4e6eb; margin-right: 20%;'}
            `;
            if (data.message) {
                messageDiv.innerHTML = `<strong>${data.sender}</strong>: ${data.message}`;
            } else if (data.imageUrl) {
                messageDiv.innerHTML = `<strong>${data.sender}</strong>:<br><img src="${data.imageUrl}" style="max-width: 150px; border-radius: 5px;">`;
            } else if (data.videoUrl) {
                messageDiv.innerHTML = `<strong>${data.sender}</strong>:<br><video src="${data.videoUrl}" style="max-width: 150px; border-radius: 5px;" controls></video>`;
            }
            messagesDiv.appendChild(messageDiv);
            lastMessageTimestamp = Math.max(lastMessageTimestamp, data.timestamp);
        });
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

// Polling for new messages
let pollingInterval = null;
function startPolling() {
    stopPolling();
    pollingInterval = setInterval(loadMessages, DM_POLL_INTERVAL);
}
function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}