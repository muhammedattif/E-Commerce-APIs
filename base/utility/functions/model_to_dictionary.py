# Python Standard Library Imports
from itertools import chain


def model_to_dict(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Model's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    related_fields = [f.name for f in opts.get_fields() if (f.one_to_many or f.many_to_one)]
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, "editable", False):
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if f.name in related_fields:
            data[f"{f.name}_id"] = f.value_from_object(instance)
        else:
            data[f.name] = f.value_from_object(instance)
    return data
