def any_none(*args):
    return any(x is None for x in args)

def get_or_none(model, **kwargs):
    x = None
    try:
        x = model.objects.get(**kwargs)
    except model.DoesNotExist:
        pass
    return x

def filter_or_none(model, **kwargs):
    x = None
    try:
        x = model.objects.filter(**kwargs)
    except model.DoesNotExist:
        pass
    return x

