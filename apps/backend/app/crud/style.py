from app.crud.base import CRUDBase
from app.models.style import Style

crud_style = CRUDBase[Style](Style)
