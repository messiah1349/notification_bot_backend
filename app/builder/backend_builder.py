from app.backend import Backend
from app.db.deed import get_engine
from app.common.constants import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_PASSWORD

engine = get_engine(POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_HOST)
backend_controller = Backend(engine)