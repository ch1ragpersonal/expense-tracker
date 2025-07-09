from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uvicorn
from auth.routes import router as auth_router
from expenses.routes import router as expenses_router

load_dotenv(dotenv_path="../../.env")

app = FastAPI(title="Expense Tracker", description="A simple expense tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(expenses_router)

@app.get("/")
async def root():
    return {"message": "API up and running"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="localhost", port=8000, reload=True)
