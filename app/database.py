from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:$%(muchori97)@db.dcwjrqbghffburtaocxi.supabase.co:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### connecting to db using psycopg2

# try:
#   conn = psycopg2.connect(user='postgres', password='$%(muchori97)', host='db.dcwjrqbghffburtaocxi.supabase.co', port='5432', 
#   database='postgres', cursor_factory=RealDictCursor)
#   cursor = conn.cursor()
# except Exception as error:
#   print("Connect to a database: ", error)