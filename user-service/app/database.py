import os
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ CORRECCIÓN DE PERSISTENCIA PARA DOCKER:
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Apunta la base de datos a /app/data/user.db
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'user.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    wardrobe_items = relationship("WardrobeItemModel", back_populates="owner")

class WardrobeItemModel(Base):
    __tablename__ = "wardrobe_items"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    perfume_id = Column(String, nullable=False)
    perfume_name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)

    owner = relationship("UserModel", back_populates="wardrobe_items")

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(UserModel).filter(UserModel.username == "kaito").first():
        default_user = UserModel(username="kaito", email="kaito@scentcraft.com", password="password123")
        db.add(default_user)
        db.commit()
        
        default_item = WardrobeItemModel(
            id="kaito-khamrah-01",
            username="kaito",
            perfume_id="khamrah-01",
            perfume_name="Khamrah",
            brand="Lattafa",
            category="signature"
        )
        db.add(default_item)
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()