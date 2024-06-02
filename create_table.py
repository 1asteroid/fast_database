from database import ENGINE, Base
from models import User, UserCourse, Category, Course

Base.metadata.create_all(ENGINE)



