from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    """every backend method should return response object"""
    status: int  # 0 status - everything is good, else - there is error
    answer: Any  # result
