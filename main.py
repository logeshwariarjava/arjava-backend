import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

# Data models
class User(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str = None
    email: str = None

# In-memory storage
users_db = {
    1: {"id": 1, "name": "John", "email": "john@example.com"},
    2: {"id": 2, "name": "Jane", "email": "jane@example.com"}
}
next_user_id = 3

app = FastAPI(
    title="Arjava API",
    description="Backend API for Arjava application",
    version="1.0.0"
)

@app.middleware("http")
async def validate_host(request: Request, call_next):
    allowed_hosts = ["arjava.localhost",]
    host = request.headers.get("host", "").split(":")[0]
    
    print(f"Incoming host: {host}")  # Debug print
    
    if host not in allowed_hosts:
        raise HTTPException(status_code=403, detail=f"Access denied. Only arjava .localhost allowed, got: {host}")
    
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to Arjava API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# CREATE - Add new user
@app.post("/users")
async def create_user(user: User):
    global next_user_id
    new_user = {"id": next_user_id, "name": user.name, "email": user.email}
    users_db[next_user_id] = new_user
    next_user_id += 1
    return new_user

# READ - Get all users
@app.get("/users")
async def get_users():
    return {"users": list(users_db.values())}

# READ - Get single user
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# UPDATE - Update user
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.name is not None:
        users_db[user_id]["name"] = user.name
    if user.email is not None:
        users_db[user_id]["email"] = user.email
    
    return users_db[user_id]

# DELETE - Delete user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = users_db.pop(user_id)
    return {"message": "User deleted", "user": deleted_user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)