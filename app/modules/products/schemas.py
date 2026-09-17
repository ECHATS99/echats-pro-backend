"""Schémas Pydantic pour le domaine 'products'."""
import uuid

from pydantic import BaseModel, Field


class ProductCategoryOut(BaseModel):
    id: uuid.UUID
    name: str

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    price_fcfa: int = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    cloudinary_image: str | None = None
    available: bool = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    price_fcfa: int | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    cloudinary_image: str | None = None
    available: bool | None = None


class ProductOut(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID | None = None
    name: str
    description: str | None = None
    price_fcfa: int
    stock: int
    cloudinary_image: str | None = None
    available: bool

    model_config = {"from_attributes": True}
