import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router

app = FastAPI(title="SmartTrade API", swagger_ui_parameters={"docExpansion": "none"})

origins = [
    "http://184.73.102.43:3000",
    "http://184.73.102.43:3001",
    "http://184.73.102.43:3002",
    "http://184.73.102.43:3003",
    "http://184.73.102.43:3004",
    "http://184.73.102.43:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes listados
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
