from .crud_series import series
from .crud_user import user
from .crud_episode import episode
from .crud_episode_image import episode_image
from .crud_cash import cash
from .crud_cash_deposit import cash_deposit
from .crud_cash_usage import cash_usage

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
