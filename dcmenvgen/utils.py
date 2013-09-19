import datetime
import random
import string


def random_string():
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase + ' _'
    # TODO - make this configurable
    size = random.randint(8, 16)
    return ''.join(random.choice(chars) for x in range(size))


def random_date_between(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))
