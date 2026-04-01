from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.checkins import router as checkin_router

app = FastAPI(title="Better Days API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(checkin_router)

@app.get("/")
def read_root():
    return {"message": "Better Days API is running"}
