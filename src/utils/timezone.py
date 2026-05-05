import pytz
import os


TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
