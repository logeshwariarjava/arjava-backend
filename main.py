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

@app.get("/")
async def root():
    return {"message": "Welcome to Arjava API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/users")
async def create_user(user: User):
    global next_user_id
    new_user = {"id": next_user_id, "name": user.name, "email": user.email}
    users_db[next_user_id] = new_user
    next_user_id += 1
    return new_user

@app.get("/users")
async def get_users():
    return {"users": list(users_db.values())}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.name is not None:
        users_db[user_id]["name"] = user.name
    if user.email is not None:
        users_db[user_id]["email"] = user.email
    
    return users_db[user_id]

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = users_db.pop(user_id)
    return {"message": "User deleted", "user": deleted_user}

# IMPORTANT for Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
