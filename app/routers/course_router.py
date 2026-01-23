from fastapi import APIRouter, Request
from app.models.course_schemas import CourseSearchRequest
from app.services.course_service import search_courses
from app.core.rate_limit import limiter

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/search")
@limiter.limit("10/minute")
def search(
    req: CourseSearchRequest,
    request: Request   # 👈 REQUIRED by slowapi
):
    matches = search_courses(
        query=req.query,
        answers=req.answers,
        top_k=req.top_k
    )

    return {"matches": matches}
