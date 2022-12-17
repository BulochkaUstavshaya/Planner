from fastapi import FastAPI
from routers.users import user_routers
from routers.events import event_routers
import uvicorn

app = FastAPI()

app.include_router(user_routers, prefix="/user")
app.include_router(event_routers, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)