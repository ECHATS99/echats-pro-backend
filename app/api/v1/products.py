"""Routes HTTP /api/v1/products."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.products import service as products_service
from app.modules.products.schemas import ProductCategoryOut, ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/categories", response_model=list[ProductCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return products_service.list_categories(db)


@router.get("")
def list_products(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), category_id: uuid.UUID | None = None, db: Session = Depends(get_db)):
    return products_service.list_products(db, page, limit, category_id)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    return products_service.get_product(db, product_id)


@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return products_service.create_product(db, payload, current.id)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: uuid.UUID, payload: ProductUpdate, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return products_service.update_product(db, product_id, payload, current.id)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: uuid.UUID, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    products_service.delete_product(db, product_id, current.id)
