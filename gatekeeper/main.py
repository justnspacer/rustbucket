from fastapi import FastAPI
from routes import user

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "API Gateway Live"}

print("Gatekeeper is running...")