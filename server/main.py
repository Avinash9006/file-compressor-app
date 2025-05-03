from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import file

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or you can specify a list like ["http://localhost:3000"]
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(file.router)
