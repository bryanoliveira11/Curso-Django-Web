import string
from secrets import SystemRandom
from typing import List


def is_positive_number(value):
    try:
        number_string = float(value)
    except:
        return False

    return number_string > 0


def generate_random_string(length: int) -> str:
    return f"-{''.join(SystemRandom().choices(string.ascii_letters + string.digits, k=length))}"
