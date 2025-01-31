#Creates a db file

from database import engine
from models import Base

def initialize_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized")

if __name__ == "__main__":
    initialize_db()