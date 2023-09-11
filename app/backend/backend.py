from app.backend.deed_processor import DeedProcessor
from app.backend.requester import Requester

class Backend(DeedProcessor, Requester):

    def __init__(self, engine):
        DeedProcessor.__init__(self, engine)
        Requester.__init__(self)

    def health_check(self):
        return "backend ok!"