from django.core.exceptions import ObjectDoesNotExist


def is_obj_exist(klass, **kwargs):
    try:
        klass.objects.get(**kwargs)
        return True
    except ObjectDoesNotExist:
        return False
    except:
        return True


def check_len(val, max=0, min=0):
    l = len(val)
    if l < min:
        raise Exception()
    if l > max:
        raise Exception()
    return val