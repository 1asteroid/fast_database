from database import ENGINE, Base
from models import UserCourse

Base.metadata.create_all(ENGINE)
