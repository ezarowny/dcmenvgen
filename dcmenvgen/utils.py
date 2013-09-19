import datetime
import random
import string


def random_string(string_length, extra_chars):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    if extra_chars:
        chars += ' _'
    size = random.randint(string_length[0], string_length[1])
    return ''.join(random.choice(chars) for x in range(size))


def random_date_between(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))
