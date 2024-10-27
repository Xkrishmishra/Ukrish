from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(
    getenv(
        "API_ID", "23270941")
)
API_HASH = getenv("API_HASH", "307571de99aa4e7f108e9a21932ec8ac")

STRING_SESSION = getenv("STRING_SESSION", "BQBiMZkAencMRi7_jY7wYBODdc_nEj0bjM-SIBUFTJIGrhzBqB3SCdzPxVZ6aAue5WCQeHc1AbH7Ipz0jFG4kIQWTL_jDA_6rvRcGNAzZV0esNvGWozY6FfEUPT2WCoMQ-z_kGw3wPwiiV-_VwqCQOzE7vQ6HKd0O7dj8ZLemMdS4NomdlWCETrYiuexiLKna1Yo_U3VZ3jNWGgCNRqBtWNfLg0I1Hnq9j2YubTj7y_I2vJQd_rUtc4l1GofrGbaFetB1CCbpiv16Q0S0At1w1jvDkZBS1pc4jnnAhh40XeFHuYgrhZD9i2sAoqVYsRej8dSiV9XFIfUgAAAAGPYj5JAA")

BOT_TOKEN = getenv("BOT_TOKEN", "7517701478:AAGSNXJOAvtFty0vARA38m34")

LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1002359358037)

OWNER_ID = list(
    map(int, getenv("OWNER_ID", "7458057585").split())
)

PREFIX = list(map(str, getenv("PREFIX", "" ".").split()))


ONLY_FOR_SUDO = bool(getenv("ONLY_FOR_SUDO", True))
