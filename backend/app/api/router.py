from fastapi import APIRouter

from app.api.routes import health, jobs, queue

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(queue.router, prefix="/queue", tags=["queue"])
