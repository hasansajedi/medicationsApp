from datetime import datetime

from pydantic import BaseModel


class LogModel(BaseModel):
    timestamp: str
    data_to_log: str


def print_log(data: str) -> None:
    from src.main import logger

    log = LogModel(timestamp=datetime.utcnow().isoformat(), data_to_log=data)
    logger.info(log.model_dump_json())
