from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from pydantic import BaseModel

# =========================================================================
# 1. DATABASE CONFIGURATION (PostgreSQL)
# =========================================================================
DATABASE_URL = "postgresql+psycopg://postgres:Pratham%4019@localhost:5432/Library_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# =========================================================================
# 2. SQLALCHEMY DB MODEL
# =========================================================================
class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True)
    stock = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# =========================================================================
# 3. PYDANTIC SCHEMAS
# =========================================================================
class ProductCreate(BaseModel):
    title: str
    sku: str
    stock: int

class ProductResponse(BaseModel):
    id: int
    title: str
    sku: str
    stock: int

    class Config:
        from_attributes = True  

# =========================================================================
# 4. FASTAPI APP & DEPENDENCY INJECTION
# =========================================================================
app = FastAPI(title="FastAPI + PostgreSQL Production Test")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================================================================
# 5. API ENDPOINTS
# =========================================================================

@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(DBProduct).filter(DBProduct.sku == product.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists in database")

    db_product = DBProduct(title=product.title, sku=product.sku, stock=product.stock)
    db.add(db_product)
    db.commit()          
    db.refresh(db_product)  
    return db_product

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return db_product