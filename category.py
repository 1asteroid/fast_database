from fastapi import APIRouter
from db.database import Session, ENGINE
from pydantic import BaseModel
from typing import Optional
from db.models import Category
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


@category_router.post("/create")
async def create(category: CategoryModel):
    check_category = session.query(Category).filter(Category.id == category.id).first()
    if check_category:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Allready exists")

    new_category = Category(
        id=category.id,
        name=category.name
    )
    session.add(new_category)
    session.commit()

    return category