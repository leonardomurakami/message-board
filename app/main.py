import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Message Board")

@app.get("/")
def home():
    return {"message": "Health check for now"}

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
