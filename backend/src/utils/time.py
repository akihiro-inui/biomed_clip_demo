from datetime import datetime


def generate_timestamp() -> str:
    """
    Generate timestamp as ISO format
    :return: Current timestamp
    """
    return datetime.utcnow().isoformat(timespec='milliseconds') + "Z"
