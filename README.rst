django-auth-krb
===============

Django kerberos authentication backend.

Install
-------

::

    # install via pip
    pip install django-auth-krb
    # or install from source
    python setup.py install

Usage
-----

KrbBackend
~~~~~~~~~~

Make sure following settings are configured in ``settings.py``:

::

    INSTALLED_APPS = (
        ...
        'django_auth_krb',
        ...
    )

    # kerberos realm
    KRB5_REALM = 'EXAMPLE.COM'

    # redirect url after login
    LOGIN_REDIRECT_URL = '/'

    # enable kerberos auth backends
    AUTHENTICATION_BACKENDS = (
        'django_auth_krb.backends.KrbBackend',
    )

Enable login/logout view in ``url.py``:

::

    urlpatterns = patterns('',
        ...
        url(r'^accounts/login/$', 'django_auth_krb.views.krb_login'),
        url(r'^accounts/logout/$', 'django_auth_krb.views.krb_logout'),
        ...
    )

RemoteKrbBackend
~~~~~~~~~~~~~~~~

Make sure following settings are configured in ``settings.py``:

::

    INSTALLED_APPS = (
        ...
        'django_auth_krb',
        ...
    )

    # kerberos realm
    KRB5_REALM = 'EXAMPLE.COM'

    # redirect url after login
    LOGIN_REDIRECT_URL = '/'

    # enable kerberos auth backends
    AUTHENTICATION_BACKENDS = (
        'django_auth_krb.backends.RemoteKrbBackend',
    )

    # enable session, auth, remoteuser middleware
    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.RemoteKrbMiddleware',
        ...
    )

Config apache as follow if you want to use RemoteKrbBackend:

::

    NameVirtualHost *:80

    <VirtualHost *:80>
        ServerAdmin webmaster@host.example.com
        ServerName host.example.com

        WSGIScriptAlias / /path/to/django/project/wsgi.py
        WSGIPassAuthorization On

        <Location "/">
            SetHandler wsgi-script
        </Location>

        <Location "/accounts/login">
            # Kerberos authentication:
            AuthType Kerberos
            AuthName "example - Kerberos login (if negotiate unavailable)"
            KrbMethodNegotiate on
            KrbMethodK5Passwd on
            KrbAuthoritative on
            KrbServiceName HTTP
            KrbAuthRealm EXAMPLE.COM
            KrbVerifyKDC on
            Krb5Keytab /etc/httpd/conf/httpd.keytab
            KrbSaveCredentials off
            Require valid-user
        </Location>
    </VirtualHost>

Enable login/logout view in ``url.py``:

::

    urlpatterns = patterns('',
        ...
        url(r'^accounts/login/$', 'django_auth_krb.views.krb_login'),
        ...
    )

