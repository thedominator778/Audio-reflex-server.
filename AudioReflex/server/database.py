import sys
import os

# Add the parent directory (AudioReflex) to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://neondb_owner:npg_W8PsyVK1nbra@ep-morning-math-ahdpjo90-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" # Updated to Neon

engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False} # Not needed for PostgreSQL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from server import models
    Base.metadata.create_all(bind=engine)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()