from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'productos'
    
    id_producto = Column(Integer, primary_key=True)  # Changed to match your column name
    nombre_producto = Column(String(45), nullable=False)  # Changed to match your column name and length
    stock = Column(Integer, nullable=False, default=0)
    bodega = Column(Integer, nullable=False)  # Changed to match your column name

    __table_args__ = (
        CheckConstraint('bodega >= 1 AND bodega <= 3', name='check_bodega_range'),
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()