from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import users, workouts, diet, progress
from .routers.chat import router as chat_router  
from .models import Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(diet.router)
app.include_router(progress.router)



app.include_router(chat_router, prefix="")

@app.on_event("startup")
def startup():
    
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)