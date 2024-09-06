import WebSocketService from '/static/websocketService.js';
import {showTab, darkMode, createRoom} from '/static/scriptFrontend.js';

window.showTab = showTab;
window.darkMode = darkMode;
window.createRoom = createRoom;

window.ws = new WebSocketService();
ws.connect();

