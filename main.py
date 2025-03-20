from fastapi import FastAPI
from routes.user import router as user_router
from routes.issues import router as issue_router
from routes.admin import router as admin_router

app = FastAPI()

# Include routers
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(issue_router, prefix="/issue", tags=["Issue"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "GreenGuard Backend is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}