from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import items, purchases, webhooks, users
from state import connected_clients

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Game Store API")

# Add CORS middleware for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)


# Include routers
app.include_router(items.router)
app.include_router(purchases.router)
app.include_router(webhooks.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Digital Store Backend"}
