from fastapi import APIRouter, WebSocket, WebSocketDisconnect
router = APIRouter()
connections=set()
@router.websocket("/ws/alerts")
async def alerts(ws:WebSocket):
    await ws.accept(); connections.add(ws)
    try:
        while True:
            msg = await ws.receive_text()
            for c in list(connections):
                try: await c.send_text(msg)
                except Exception: pass
    except WebSocketDisconnect:
        connections.discard(ws)
