from ..backend import Backend
from ..db.deed import get_engine
from ..common.constants import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_PASSWORD

engine = get_engine(POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_HOST)
backend_controller = Backend(engine)