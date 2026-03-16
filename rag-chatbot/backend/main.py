from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/auth/register")
def register(data: dict):
    return {
        "status": "success",
        "message": "User registered",
        "data": data
    }

@app.post("/auth/login")
def login(data: dict):
    # Simple login for testing (no authentication)
    return {
        "status": "success",
        "message": "Login successful",
        "access_token": "fake-jwt-token-" + data.get("email", "user"),
        "token_type": "bearer",
        "user": {
            "email": data.get("email"),
            "first_name": "Test",
            "last_name": "User",
            "is_active": True
        }
    }
