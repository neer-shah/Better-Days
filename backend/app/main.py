from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.checkins import router as checkin_router
from app.api.routes.dashboard import router as dashboard_router

app = FastAPI(title="Better Days API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(checkin_router)
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    return {"message": "Better Days API is running"}
