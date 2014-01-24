import kerberos
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, RemoteUserBackend


class KrbBackend(ModelBackend):

    """
    Kerberos auth backend based on Django ModelBackend.

    Required correct ``/etc/krb5.conf`` configuration.
    """

    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
            username = username.split('@')[0]
        except ValidationError:
            pass

        try:
            kerberos.checkPassword(
                username, password, '',
                settings.KRB5_REALM
            )
        except kerberos.BasicAuthError:
            return None

        user, created = User.objects.get_or_create(
            username=username
        )
        user.set_unusable_password()
        user.email = username + '@' + settings.KRB5_REALM.lower()
        user.save()

        return user


class RemoteKrbBackend(RemoteUserBackend):

    """
    Remote kerberos backend based on Django RemoteUserBackend.

    Required correct ``/etc/httpd/conf/http.<hostname>.keytab``,
    ``/etc/krb5.conf`` and correct ``mod_auth_krb5`` module settings
    for apache.

    Example apache settings:

    # Set a httpd config to protect krb5login page with kerberos.
    # You need to have mod_auth_kerb installed to use kerberos auth.
    # Httpd config /etc/httpd/conf.d/<project>.conf should look like this:

    <Location "/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE <project>.settings
        PythonDebug On
    </Location>

    <Location "/auth/krb5login">
        AuthType Kerberos
        AuthName "<project> Kerberos Authentication"
        KrbMethodNegotiate on
        KrbMethodK5Passwd off
        KrbServiceName HTTP
        KrbAuthRealms EXAMPLE.COM
        Krb5Keytab /etc/httpd/conf/http.<hostname>.keytab
        KrbSaveCredentials off
        Require valid-user
    </Location>
    """

    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.
        """
        user.email = user.username + '@' + settings.KRB5_REALM.lower()
        user.set_unusable_password()
        user.save()
        return user

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.

        For more info, reference clean_username function in
        django/auth/backends.py
        """
        if email_re.search(username):
            username = username.split('@')[0]

        # truncate username which length exceeds field max_length
        max_length = User._meta.get_field('username').max_length
        if len(username) > max_length:
            username = username[:max_length]

        return username
