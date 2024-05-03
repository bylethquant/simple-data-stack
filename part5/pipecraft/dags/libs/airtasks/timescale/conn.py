import logging

from airflow.models import Variable

# create module logger
logger = logging.getLogger(__name__)


def retrieve_conn_id(id_key: str = "admin") -> str:
    """Retrieves timescale connection id."""
    try:
        if id_key == "admin":
            conn_id = Variable.get("TIMESCALE_CONN_ID_ADMIN")
        elif id_key == "readonly":
            conn_id = Variable.get("TIMESCALE_CONN_ID_READONLY")
        else:
            raise ValueError("Unknown id_key. Select admin or readonly.")
    except Exception as exc:
        logger.exception(f"Retrieving admin timescale connection id: failed. {exc}.")
        raise
    else:
        logger.info(f"Retrieving admin timescale connection id: successful.")
    return conn_id
