from app.crud.base import CRUDBase
from app.models.platform import Platform

crud_platform = CRUDBase[Platform](Platform)
