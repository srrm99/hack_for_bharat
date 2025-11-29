"""
Bharat Context-Adaptive Engine - FastAPI Application
Main entry point for the inference service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .router_inference import router as inference_router
from .router_recommendations import router as recommendations_router


# Initialize FastAPI app
app = FastAPI(
    title="Bharat Context-Adaptive Engine",
    description="Inference Engine for Day-0 Cold Start Problem - Tier-2/3/4 Indian Users",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inference_router)
app.include_router(recommendations_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Bharat Context-Adaptive Engine",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "inference": "/v1/infer",
            "health": "/v1/health",
            "rules": "/v1/rules",
            "recommendations": "/v1/recommendations/generate",
            "docs": "/docs"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "message": "Internal server error"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

