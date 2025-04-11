from models import items
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import items, purchases, webhooks, users


app = FastAPI(title="Digital Game Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(items.router)
app.include_router(purchases.router)
app.include_router(webhooks.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Digital Store Backend"}
