
class WebSocketService {
  constructor(url) {
    const clientId = Date.now();
    this.url = `ws://localhost:8000/ws/${clientId}`;
    this.socket = null;
  }

  connect() {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("WebSocket connection established");
    };

    this.socket.onmessage = (event) => {
      console.log("Message received from server:", event.data);
    };

    this.socket.onclose = (event) => {
      console.log("WebSocket connection closed:", event);
      this.reconnect();
    };

    this.socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  sendMessage(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    } else {
      console.error("WebSocket is not open. ReadyState:", this.socket.readyState);
    }
  }

  reconnect() {
    setTimeout(() => {
      console.log("Reconnecting WebSocket...");
      this.connect();
    }, 5000);
  }
}

export default WebSocketService;
