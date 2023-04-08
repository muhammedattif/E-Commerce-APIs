# Python Standard Library Imports
import random
import string


def generate_random(size, chars=string.ascii_lowercase + string.digits):
    """generate random string consisting of lowercase letters and digits"""
    return "".join(random.choice(chars) for x in range(size))


def generate_random_ipv4():
    """generates a random ipv4"""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))
