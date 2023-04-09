# Python Standard Library Imports
import random
import string


def generate_random(size, chars=string.ascii_lowercase + string.digits):
    """generate random string consisting of lowercase letters and digits"""
    return "".join(random.choice(chars) for x in range(size))


def generate_random_referal_code(CODE_LENGTH=6):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(CODE_LENGTH))


def generate_random_ipv4():
    """generates a random ipv4"""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))
