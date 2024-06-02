from fastapi import APIRouter
from database import Session, ENGINE
from pydantic import BaseModel
from typing import Optional
from models import Category
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)

category_router = APIRouter(prefix="/category")


class CategoryModel(BaseModel):
    id: Optional[int]
    name: str


@category_router.get("/")
async def category_list(status_code=status.HTTP_200_OK):
    categories = session.query(Category).all()
    context = [
        {
            "id": category.id,
            "name": category.name,
        }
        for category in categories
    ]

    return jsonable_encoder(context)


@category_router.post("/")
async def create(category: CategoryModel):
    check_category = session.query(Category).filter(Category.id == category.id).first()
    if check_category:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exists")

    new_category = Category(
        id=category.id,
        name=category.name
    )
    session.add(new_category)
    session.commit()

    return category


@category_router.get("/{id}")
async def category_only(id: int):
    category = session.query(Category).filter(Category.id == id).first()

    if category:
        return category

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course Not Found")


@category_router.put("/{id}")
async def category_update(id: int, category: CategoryModel):
    check_category = session.query(Category).filter(Category.id == id).first()

    if check_category:

        for key, value in category.dict(exclude_unset=True).items():
            setattr(check_category, key, value)

        session.commit()

        data = {
            "code": 202,
            "message": "Full update"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
