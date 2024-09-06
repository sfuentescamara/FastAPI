// Scripts Room

function copyIdRoom(id) {
    navigator.clipboard.writeText(id);

    alert("Copied the text: " + id)
}

function updateVideoSrc() {
    /* const videoUrlInput = document.getElementById('videoUrlInput');
    const videoSource = document.getElementById('videoSource');
    const videoPlayer = document.getElementById('videoPlayer');

    // Update the source URL of the video
    videoSource.src = videoUrlInput.value;
    
    // Load the new video
    videoPlayer.load(); */

    let video = document.getElementById('videoPlayer');

    video.addEventListener('play', () => {
        window.ws.send(JSON.stringify({action: 'play', time: video.currentTime}));
    });

    video.addEventListener('pause', () => {
        window.ws.send(JSON.stringify({action: 'pause', time: video.currentTime}));
    });

    video.addEventListener('seeked', () => {
        window.ws.send(JSON.stringify({action: 'seek', time: video.currentTime}));
    });

    /* function eventListener(action) {
        window.ws.send(JSON.stringify({"action": action, "time": video.currentTime}));
    } */
}

window.ws.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.action === 'play') {
        video.currentTime = data.time;
        audio.currentTime = data.time;
        video.play();
        audio.play();
    } else if (data.action === 'pause') {
        video.pause();
        audio.pause();
    } else if (data.action === 'seek') {
        video.currentTime = data.time;
        audio.currentTime = data.time;
    }
}

function configFunction1() {
    alert('Config 1 clicked');
}

function configFunction2() {
    alert('Config 2 clicked');
}

function configFunction3() {
    alert('Config 3 clicked');
}

function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const chatWindow = document.getElementById('chatWindow');

    if (chatInput.value.trim() !== '') {
        const message = document.createElement('div');
        message.classList.add('chat-message');
        message.textContent = "Me: " + chatInput.value;
        chatWindow.appendChild(message);

        JSONdata = JSON.stringify({"id_room": document.room, 
                                    "action": "message", 
                                    "user": document.user, 
                                    "message": chatInput.value});
        ws.sendMessage(JSONdata);

        chatInput.value = '';
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}

function obtenerCookie(nombre) {
    const valor = `; ${document.cookie}`;
    const partes = valor.split(`; ${nombre}=`);
    if (partes.length === 2) return partes.pop().split(';').shift();
}

const chatSection = document.getElementById('chat-area');
const toggleChat = document.getElementById('toggleChat');
/* const chatInput = document.getElementById('chatInput'); */
const chatMessages = document.getElementById('chat-message');
const notification = document.getElementById('newMessageNotification');
let isChatVisible = true;

function toggleChatVisibility() {
    if (isChatVisible) {
        chatSection.style.display = 'none';
    } else {
        chatSection.style.display = 'block';
    }
    isChatVisible = !isChatVisible;
}

function checkWindowSize() {
    if (window.innerWidth < 600) {
        chatSection.style.display = 'none';
        isChatVisible = false;
    } else {
        chatSection.style.display = 'block';
        isChatVisible = true;
    }
}

function addMessage(message) {
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    if (!isChatVisible) {
        showNotification();
    }
}

function showNotification() {
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

toggleChat.addEventListener('click', toggleChatVisibility);
window.addEventListener('resize', checkWindowSize);
/* chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addMessage(this.value);
        this.value = '';
    }
}); */

// Inicialización
checkWindowSize();