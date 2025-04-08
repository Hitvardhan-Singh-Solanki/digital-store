from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import items, purchases, webhooks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Game Store API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router)
app.include_router(purchases.router)
app.include_router(webhooks.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Digital Store Backend"}
