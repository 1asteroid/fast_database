from fastapi import APIRouter
from database import Session, ENGINE
from pydantic import BaseModel, ValidationError
from typing import Optional
from models import Course, Category
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Users, Course, UserCourse, Category

session = Session(bind=ENGINE)

buy_router = APIRouter(prefix="/buy")


class Buy(BaseModel):
    users_id: int
    course_id: int

try:
    Buy()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))


@buy_router.get("/{id}")
async def course_of_user(id: int):
    user = session.query(Users).filter(Users.id == id).first()
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "User not found"})

    courses_users = session.query(UserCourse).filter(UserCourse.users_id == id)
    courses = []
    for i in courses_users:
        courses.append(session.query(Course).filter(Course.id == i.users_id).first())

    cors = [

        {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "price": course.price,
            "category_id": {
                "id": session.query(Category).filter(Category.id == course.category_id).first().id,
                "name": session.query(Category).filter(Category.id == course.category_id).first().name
            }

        }
        for course in courses
    ]

    context = {
        "username": user.username,
        "courses": cors
    }

    return context


@buy_router.post("/create")
async def usercourse(order: Buy):
    user = session.query(Users).filter(Users.id == order.users_id).first()
    course = session.query(Course).filter(Course.id == order.course_id).first()
    check_user_course = session.query(UserCourse).filter(UserCourse.users_id == order.users_id, UserCourse.course_id ==
                                                         order.course_id).first()

    if user:

        if course:

            if check_user_course:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail={"message": "User has this course"})

            new_user_course = UserCourse(
                users_id=order.users_id,
                course_id=order.course_id
            )

            session.add(new_user_course)
            session.commit()
            return HTTPException(status_code=status.HTTP_200_OK, detail={"message": "Added successfully"})

        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Course not found"})

    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "User not found"})


