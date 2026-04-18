"""
TriageX - AI-Powered Visual Medical Triage Assistant
Main FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routes import triage, auth, admin, reports, translations

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(auth.router)
app.include_router(triage.router)
app.include_router(admin.router)
app.include_router(reports.router)
app.include_router(translations.router)


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()
    print(f"\n{'='*50}")
    print(f"  🧠 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"  {settings.APP_DESCRIPTION}")
    print(f"  Docs: http://localhost:8000/docs")
    print(f"{'='*50}\n")


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": "Explain. Assess. Act.",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
