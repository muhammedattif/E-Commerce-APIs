# Code Format <App First+Second Letter><Model First+Second letter><Code>


def build_code(prefix, base_num, code, model_prefix=None):
    NONE_MODEL_PREFIX = "GE"
    return "{0}{1}{2}{3}".format(
        prefix,
        model_prefix or NONE_MODEL_PREFIX,
        base_num,
        code,
    )


class ServerCodes:

    PREFIX = "SE"
    BASE_NUM = 0

    SERVICE_UNAVAILABLE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="0")


class GeneralCodes:

    PREFIX = "GE"
    BASE_NUM = 1

    SUCCESS = build_code(prefix=PREFIX, base_num=BASE_NUM, code="0")
    INVALID_DATA = build_code(prefix=PREFIX, base_num=BASE_NUM, code="1")
    ALREADY_EXISTS = build_code(prefix=PREFIX, base_num=BASE_NUM, code="2")


class UsersCodes:

    PREFIX = "US"
    BASE_NUM = 2

    INACTIVE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="0", model_prefix="US")
    SUSPENDED = build_code(prefix=PREFIX, base_num=BASE_NUM, code="1", model_prefix="US")
    INVALID_UID = build_code(prefix=PREFIX, base_num=BASE_NUM, code="2", model_prefix="US")
    ALREADY_ACTIVATED = build_code(prefix=PREFIX, base_num=BASE_NUM, code="3", model_prefix="US")
    CANNOT_SEND_ACTIVATION_EMAIL = build_code(prefix=PREFIX, base_num=BASE_NUM, code="4", model_prefix="US")
    INVALID_OLD_PASSWORD = build_code(prefix=PREFIX, base_num=BASE_NUM, code="5", model_prefix="US")
    PASSWORD_NOT_MATCH = build_code(prefix=PREFIX, base_num=BASE_NUM, code="6", model_prefix="US")
    INVALID_PASSWORD_CRITERIA = build_code(prefix=PREFIX, base_num=BASE_NUM, code="7", model_prefix="US")
    INVALID_TOKEN = build_code(prefix=PREFIX, base_num=BASE_NUM, code="8", model_prefix="TO")


class ModelsCodes:

    PREFIX = "MO"
    BASE_NUM = 3


class BrandsCodes:

    PREFIX = "BR"
    BASE_NUM = 4


class PaymentsCodes:

    PREFIX = "PA"
    BASE_NUM = 5


class SellersCodes:

    PREFIX = "SE"
    BASE_NUM = 6
