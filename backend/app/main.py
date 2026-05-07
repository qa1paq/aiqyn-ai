from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, profile, assessment, universities, choices, matching, roadmap, gamification

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered career guidance and university admission platform for high school graduates",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["Authentication"])
app.include_router(profile.router, prefix=f"{API_PREFIX}/profile", tags=["Profile"])
app.include_router(assessment.router, prefix=f"{API_PREFIX}/assessment", tags=["Assessment"])
app.include_router(universities.router, prefix=f"{API_PREFIX}", tags=["Universities"])
app.include_router(choices.router, prefix=f"{API_PREFIX}/choices", tags=["University Choices"])
app.include_router(matching.router, prefix=f"{API_PREFIX}/matching", tags=["Matching"])
app.include_router(roadmap.router, prefix=f"{API_PREFIX}/roadmap", tags=["Roadmap"])
app.include_router(gamification.router, prefix=f"{API_PREFIX}/gamification", tags=["Gamification"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
