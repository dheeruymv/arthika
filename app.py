from fastapi import FastAPI
from uvicorn import run
from arthikaapi.routers import shares
from arthikaapi.routers import users
from database import Base, engine
import arthikaapi.models.users
import arthikaapi.models.stocks
from arthikaapi.middlewares import middlewares
from fastapi.middleware.cors import CORSMiddleware #Cross Origin Resource Sharing


# Below method of events is deprecated in FastAPI
# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)

async def lifespan(app: FastAPI):
    print(f"Executing the start up tasks")
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(docs_url="/arthika-docs", lifespan=lifespan, middleware=middlewares)

origins = [
    "http://localhost:3000",   # React app
    "http://127.0.0.1:3000",   # Another variant
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Frontend origins allowed to call backend
    allow_credentials=True,
    allow_methods=["*"],             # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],             # Allow all headers
)

app.include_router(shares.router)
app.include_router(users.router)

if __name__ == '__main__':
    run(app, host="localhost")