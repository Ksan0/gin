from django.core.exceptions import ObjectDoesNotExist


def is_obj_exist(klass, **kwargs):
    try:
        klass.objects.get(**kwargs)
        return True
    except ObjectDoesNotExist:
        return False
    except:
        return True