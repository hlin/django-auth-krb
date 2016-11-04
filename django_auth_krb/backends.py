import re

from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User


class RemoteKrbBackend(RemoteUserBackend):

    """Remote kerberos backend based on Django RemoteUserBackend.

    Required correct ``/etc/httpd/conf/httpd.keytab``,
    ``/etc/krb5.conf`` and correct ``mod_auth_kerb`` module settings
    for apache.

    Example apache settings:

    # Set a httpd config to protect auth/login page with kerberos.
    # You need to have mod_auth_kerb installed to use kerberos auth.
    # Httpd config /etc/httpd/conf.d/<project>.conf should look like this:

    <Location "/">
        Require all granted
    </Location>

    <Location "/auth/login/">
        SSLRequireSSL
        AuthType Kerberos
        AuthName "Kerberos login"
        KrbMethodNegotiate on
        KrbMethodK5Passwd off
        KrbServiceName HTTP
        KrbAuthRealm EXAMPLE.COM
        Krb5Keytab /etc/httpd/conf/httpd.keytab
        KrbSaveCredentials off
        KrbVerifyKDC on
        Require valid-user
    </Location>

    """

    def configure_user(self, user):
        """Configures a user after creation and returns the updated user."""

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
        if re.search('@', username):
            username = username.split('@')[0]

        # Replace / with + since kerberos principal may contain / and it's
        # invalid character in django user model's username field
        if '/' in username:
            username = username.replace('/', '+')

        # truncate username which length exceeds field max_length
        max_length = User._meta.get_field('username').max_length
        if len(username) > max_length:
            username = username[:max_length]

        return username
