"""Accès aux données du domaine 'products' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product, ProductCategory


def list_categories(db: Session) -> list[ProductCategory]:
    return list(db.execute(select(ProductCategory)).scalars().all())


def get_by_id(db: Session, product_id: uuid.UUID) -> Product | None:
    return db.get(Product, product_id)


def list_products(db: Session, page: int, limit: int, category_id: uuid.UUID | None, available_only: bool = True) -> tuple[list[Product], int]:
    filters = []
    if available_only:
        filters.append(Product.available.is_(True))
    if category_id:
        filters.append(Product.category_id == category_id)
    total = db.execute(select(func.count()).select_from(Product).where(*filters)).scalar_one()
    stmt = select(Product).where(*filters).order_by(Product.created_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total


def create(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product: Product, fields: dict) -> Product:
    for key, value in fields.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def decrement_stock(db: Session, product: Product, quantity: int) -> None:
    product.stock = max(0, product.stock - quantity)
    db.add(product)
    db.commit()
