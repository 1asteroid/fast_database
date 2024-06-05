from fastapi import APIRouter
from database import Session, ENGINE
from pydantic import BaseModel
from typing import Optional
from models import Course, Category
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

session = Session(bind=ENGINE)

course_router = APIRouter(prefix="/course")


class CourseModel(BaseModel):
    id: Optional[int]
    name: str
    description: str | None = None
    price: float
    category_id: Optional[int]


@course_router.get("/")
async def course_list(status_code=status.HTTP_200_OK):
    courses = session.query(Course).all()
    context = [
        {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "price": course.price,
            "category_id": course.category_id,
        }
        for course in courses
    ]
    return jsonable_encoder(context)


@course_router.post("/")
async def course_create(course: CourseModel):
    check_course = session.query(Course).filter(Course.id == course.id).first()
    check_category = session.query(Category).filter(Category.id == course.category_id).first()
    if check_course:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course id already exist")

    if check_category:
        new_course = Course(
            id=course.id,
            name=course.name,
            description=course.description,
            price=course.price,
            category_id=course.category_id
        )
        session.add(new_course)
        session.commit()
        return new_course

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category not found")



@course_router.get("/{id}")
async def course_only(id: int):
    course = session.query(Course).filter(Course.id == id).first()

    if course:
        return course

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course Not Found")


@course_router.put("/{id}")
async def course_update(id: int, course: CourseModel):
    check_course = session.query(Course).filter(Course.id == id).first()

    if check_course:

        for key, value in course.dict(exclude_unset=True).items():
            setattr(check_course, key, value)

        session.commit()

        data = {
            "code": 202,
            "message": "Full update"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@course_router.delete("/{id}")
async def course_delete(id: int):
    check_course = session.query(Course).filter(Course.id == id).first()
    if check_course:
        session.delete(check_course)
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
