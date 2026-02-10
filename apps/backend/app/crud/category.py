from app.crud.base import CRUDBase
from app.models.category import Category

crud_category = CRUDBase[Category](Category)
