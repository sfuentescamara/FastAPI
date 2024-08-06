
function showTab(tabIndex) {
    var contents = document.getElementsByClassName('content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
    }
    document.getElementById('content' + tabIndex).style.display = 'block';
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
    connectWebSocket(idClient);
    });
} else {
    connectWebSocket(idClient);
}

function connectWebSocket(idClient) {
  const socket = new WebSocket(`ws://localhost:8080/ws/${idClient}`);

  socket.onopen = function(event) {
    console.log('WebSocket connection established');
  };

  socket.onmessage = function(event) {
    console.log('Received message:', event.data);
  };

  socket.onclose = function(event) {
    console.log('WebSocket connection closed');
  };

  socket.onerror = function(error) {
    console.log('WebSocket error:', error);
  };
}


function darkMode() {
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'dark') {
        document.body.className = 'light-mode';
    } else {
        document.body.className = 'dark-mode';
    }
    const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);

};

