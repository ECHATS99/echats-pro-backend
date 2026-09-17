"""Logique métier du domaine 'products' (boutique BLACKHAWK LAB)."""
import uuid

from app.core.exceptions import NotFoundError, ValidationError
from app.models.product import Product
from app.modules.products import repository as products_repo
from app.modules.products.schemas import ProductCategoryOut, ProductCreate, ProductOut, ProductUpdate
from app.services.audit_service import log_action
from app.utils.pagination import paginate


def list_categories(db) -> list[ProductCategoryOut]:
    return [ProductCategoryOut.model_validate(c) for c in products_repo.list_categories(db)]


def list_products(db, page: int, limit: int, category_id: uuid.UUID | None):
    items, total = products_repo.list_products(db, page, limit, category_id)
    return paginate([ProductOut.model_validate(p).model_dump() for p in items], page, limit, total)


def get_product(db, product_id: uuid.UUID) -> ProductOut:
    product = products_repo.get_by_id(db, product_id)
    if product is None:
        raise NotFoundError("Produit introuvable.")
    return ProductOut.model_validate(product)


def create_product(db, payload: ProductCreate, actor_id: uuid.UUID) -> ProductOut:
    product = products_repo.create(db, Product(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="product.created", module="products", resource="product", resource_id=str(product.id))
    return ProductOut.model_validate(product)


def update_product(db, product_id: uuid.UUID, payload: ProductUpdate, actor_id: uuid.UUID) -> ProductOut:
    product = products_repo.get_by_id(db, product_id)
    if product is None:
        raise NotFoundError("Produit introuvable.")
    fields = payload.model_dump(exclude_unset=True)
    product = products_repo.update(db, product, fields)
    log_action(db, user_id=actor_id, action="product.updated", module="products", resource="product", resource_id=str(product.id))
    return ProductOut.model_validate(product)


def delete_product(db, product_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    product = products_repo.get_by_id(db, product_id)
    if product is None:
        raise NotFoundError("Produit introuvable.")
    products_repo.delete(db, product)
    log_action(db, user_id=actor_id, action="product.deleted", module="products", resource="product", resource_id=str(product_id))
