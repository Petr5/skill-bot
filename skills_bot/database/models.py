from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)

# Replace 'DATABASE_URL' with your database URL
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)

AsyncSession = sessionmaker(bind=engine, class_=aiomysql.sa.orm.Session, expire_on_commit=False)
