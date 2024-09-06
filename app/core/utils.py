import uuid

from app.core.dependencies import *


def get_timestamp_string():
    now = time.time()
    now_string = str(int(now))
    return now_string

def generate_id():
    now = get_timestamp_string()
    unique_id = f"{now}-{uuid.uuid4()}"
    return unique_id
