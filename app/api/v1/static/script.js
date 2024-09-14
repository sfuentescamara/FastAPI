import WebSocketService from '/static/websocketService.js';
import {showTab, darkMode, createRoom, joinToRoom} from '/static/scriptFrontend.js';

window.showTab = showTab;
window.darkMode = darkMode;
window.createRoom = createRoom;
window.joinToRoom = joinToRoom;

window.ws = new WebSocketService();
ws.connect();

