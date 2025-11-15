from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
# DATABASE_URL = "sqlite:///./database.db"
DATABASE_URL = "mysql+pymysql://appuser:apppass@localhost:3306/postcode_db"

# DATABASE_URL = os.getenv(
#   "DATABASE_URL",
#   "sqlite:///./database.db"
# )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()