// src/services/webSocket.ts

export class WebSocketService {
  private socket: WebSocket | null = null;

  connect() {
    this.socket = new WebSocket(`ws://${import.meta.env.VITE_API_URL}/image/ws`);

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Handle different types of messages
      if (data.type === 'update') {
        // Update UI with progress
      } else if (data.type === 'error') {
        console.error('WebSocket error:', data.data.message);
      }
    };
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
    }
  }
}