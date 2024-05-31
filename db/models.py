from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    email = Column(String(40), nullable=True)
    user_course = relationship('UserCourse', back_populates='user')


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=True)
    course = relationship('Course', back_populates='category')


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='course')
    user_course = relationship('UserCourse', back_populates='course')


class UserCourse(Base):
    __tablename__ = 'user_course'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='user_course')
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship('Course', back_populates='user_course')
