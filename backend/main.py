import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.config import API_PREFIX

# Create FastAPI app
app = FastAPI(
    title="AI Tutor API",
    description="API for AI Tutor with Gemini AI integration",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=API_PREFIX)

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "AI Tutor API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)