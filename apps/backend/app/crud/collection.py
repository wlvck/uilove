from app.crud.base import CRUDBase
from app.models.collection import Collection

crud_collection = CRUDBase[Collection](Collection)
