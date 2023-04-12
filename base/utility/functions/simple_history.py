def adjusted_get_user(request, **kwargs):
    # First Party Imports
    from base.users.models import User

    try:
        user = request.user
        if not isinstance(user, User):
            return None
        return request.user
    except AttributeError:
        return None
