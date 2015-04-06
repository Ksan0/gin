from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission, \
    _user_get_all_permissions, _user_has_perm, _user_has_module_perms

from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.utils.encoding import python_2_unicode_compatible
from gin.settings_db import SettingsDB


class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, is_superuser=False, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_superuser=is_superuser, last_login=timezone.now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    id = models.AutoField(primary_key=True)

    email = models.EmailField(_('email address'), unique=True, max_length=SettingsDB.MAX_EMAIL_LENGTH)
    first_name = models.CharField(_('first name'), max_length=SettingsDB.MAX_NAME_LENGTH, blank=True)
    last_name = models.CharField(_('last name'), max_length=SettingsDB.MAX_NAME_LENGTH, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    is_operator = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('a_user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the a_user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class AUser(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


@python_2_unicode_compatible
class AnonymousUser(object):
    id = None
    pk = None
    is_operator = False
    is_superuser = False
    _groups = EmptyManager(Group)
    _user_permissions = EmptyManager(Permission)

    def __init__(self):
        pass

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def save(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def _get_groups(self):
        return self._groups
    groups = property(_get_groups)

    def _get_user_permissions(self):
        return self._user_permissions
    user_permissions = property(_get_user_permissions)

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj=obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, module):
        return _user_has_module_perms(self, module)

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False
