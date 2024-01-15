import pytz
import datetime
import logging


def setup_logger(timezone="UTC") -> logging.Logger:
    """
    Setup logger to print messages along with regional time.

    :param timezone: The timezone to use for timestamps. Default is 'UTC'.
    """

    # Create a custom logger
    logger = logging.getLogger("Scheduler")
    logger.setLevel(logging.INFO)

    # Define log format with regional time
    log_format = logging.Formatter(
        f"%(asctime)s %(name)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Timezone
    tz = pytz.timezone(timezone)
    log_format.converter = lambda _: datetime.datetime.now(tz).timetuple()

    # Add console handler
    handler = logging.StreamHandler()

    handler.setFormatter(log_format)
    logger.addHandler(handler)

    return logger


logger = setup_logger(
    timezone="Europe/Copenhagen",
)
