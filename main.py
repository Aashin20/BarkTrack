from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from utils.db import Database
from utils.breed import create_model
from routers import auth_route, user_route, predict_route,doctor_route
from utils.rib_compression import load_rib_model
from utils.panting import load_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to MongoDB.....")
    Database.initialize()
    print("Loading ML model...")
    app.state.breed_model = create_model()
    app.state.rib_model = load_rib_model()
    app.state.panting_model = load_model()
    yield
    print("Shutting down MongoDB....")
    if Database.client:
        Database.client.close()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_route.router, prefix="/auth",tags=["auth"])
app.include_router(user_route.router, prefix="/user",tags=["user"])
app.include_router(predict_route.router, prefix="/predict", tags=["predict"])
app.include_router(doctor_route.router,prefix="/doctor", tags=["doctor"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
