from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn
from auth.routes import router as auth_router

load_dotenv(dotenv_path="../../.env")

app = FastAPI(title="Expense Tracker", description="A simple expense tracker")

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "API up and running"}

if __name__ == "__main__":
    uvicorn.run("expense-tracker.main:app", host="localhost", port=8000, reload=True)
