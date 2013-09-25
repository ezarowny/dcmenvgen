import datetime
import random
import string


def random_string(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def random_date_between(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))
