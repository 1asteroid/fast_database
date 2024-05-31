from db.database import ENGINE, Base
Base.metadata.create_all(ENGINE)
