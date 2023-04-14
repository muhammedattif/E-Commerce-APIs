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
    NOT_FOUND = build_code(prefix=PREFIX, base_num=BASE_NUM, code="3")


class UsersCodes:

    PREFIX = "US"
    BASE_NUM = 2

    INVALID_CREDENTIALS = build_code(prefix=PREFIX, base_num=BASE_NUM, code="0", model_prefix="US")
    INACTIVE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="1", model_prefix="US")
    SUSPENDED = build_code(prefix=PREFIX, base_num=BASE_NUM, code="2", model_prefix="US")
    INVALID_UID = build_code(prefix=PREFIX, base_num=BASE_NUM, code="3", model_prefix="US")
    ALREADY_ACTIVATED = build_code(prefix=PREFIX, base_num=BASE_NUM, code="4", model_prefix="US")
    CANNOT_SEND_ACTIVATION_EMAIL = build_code(prefix=PREFIX, base_num=BASE_NUM, code="5", model_prefix="US")
    INVALID_OLD_PASSWORD = build_code(prefix=PREFIX, base_num=BASE_NUM, code="6", model_prefix="US")
    PASSWORD_NOT_MATCH = build_code(prefix=PREFIX, base_num=BASE_NUM, code="7", model_prefix="US")
    INVALID_PASSWORD_CRITERIA = build_code(prefix=PREFIX, base_num=BASE_NUM, code="8", model_prefix="US")
    INVALID_TOKEN = build_code(prefix=PREFIX, base_num=BASE_NUM, code="9", model_prefix="TO")
    INVALID_ACCOUNT_TYPE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="10", model_prefix="US")


class ProductsCodes:

    PREFIX = "PR"
    BASE_NUM = 3

    OUT_OF_STOCK = build_code(prefix=PREFIX, base_num=BASE_NUM, code="0", model_prefix="PR")
    AVAILABLE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="1", model_prefix="PR")
    QUANTITY_UNAVAILBLE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="2", model_prefix="PR")
    NOT_AVAILBLE = build_code(prefix=PREFIX, base_num=BASE_NUM, code="3", model_prefix="PR")


class BrandsCodes:

    PREFIX = "BR"
    BASE_NUM = 4


class PaymentCodes:

    PREFIX = "PA"
    BASE_NUM = 5


class SellersCodes:

    PREFIX = "SE"
    BASE_NUM = 6


def export_response_codes():

    code_classes = [
        ServerCodes,
        GeneralCodes,
        UsersCodes,
        ProductsCodes,
        BrandsCodes,
        PaymentCodes,
        SellersCodes,
    ]
    exclude_keys = [
        "PREFIX",
        "BASE_NUM",
    ]
    all_codes = []
    for _class in code_classes:
        codes = {
            v: getattr(_class, v)
            for v in dir(_class)
            if not callable(getattr(_class, v)) and v.isupper() and v not in exclude_keys
        }
        if codes:
            all_codes.append({"type": f"{_class.__name__}", "codes": codes})
    return all_codes
