"""WebSocket handlers for real-time updates."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
        # Remove from all subscriptions
        for topic in self.subscriptions:
            self.subscriptions[topic].discard(websocket)

    async def subscribe(self, websocket: WebSocket, topic: str):
        """Subscribe a connection to a topic."""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(websocket)

    async def broadcast(self, message: dict):
        """Broadcast to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_to_topic(self, topic: str, message: dict):
        """Broadcast to clients subscribed to a topic."""
        if topic not in self.subscriptions:
            return

        disconnected = set()
        for connection in self.subscriptions[topic]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn)


# Global connection manager
manager = ConnectionManager()


@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for live updates."""
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # Handle subscription requests
            if data.get("type") == "subscribe":
                topic = data.get("topic")
                if topic:
                    await manager.subscribe(websocket, topic)
                    await websocket.send_json({
                        "type": "subscribed",
                        "topic": topic
                    })

            # Handle ping/pong for keepalive
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

            # Handle unsubscribe
            elif data.get("type") == "unsubscribe":
                topic = data.get("topic")
                if topic and topic in manager.subscriptions:
                    manager.subscriptions[topic].discard(websocket)
                    await websocket.send_json({
                        "type": "unsubscribed",
                        "topic": topic
                    })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


# Export for use in background tasks
websocket_router = router
websocket_manager = manager
