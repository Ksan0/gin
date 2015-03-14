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
    if val < min:
        raise Exception()
    if val > max:
        raise Exception()
    return val