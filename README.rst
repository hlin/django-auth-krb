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

RemoteKrbBackend
~~~~~~~~~~~~~~~~

Make sure following settings are configured in ``settings.py``:

::

    INSTALLED_APPS = (
        ...
        'django_auth_krb',
        ...
    )

    KRB5_REALM = 'EXAMPLE.COM'

    AUTHENTICATION_BACKENDS = (
       'django_auth_krb.backends.RemoteKrbBackend',
    )

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.auth.middleware.PersistentRemoteUserMiddleware',
        ...
    ]

    LOGIN_REDIRECT_URL = '/'

Include auth url in project urls.py

::

    from django.conf.urls include

    urlpatterns = [
        url(r'^auth/', include('django_auth_krb.urls')),
        ...
    ]

Config apache as follow if you want to use RemoteKrbBackend:

::

    <VirtualHost *:443>
        ServerAdmin webmaster@host.example.com
        ServerName host.example.com

        SSLEngine on
        SSLCertificateFile /etc/httpd/conf/ssl.crt
        SSLCertificateKeyFile /etc/httpd/conf/ssl.key

        WSGIScriptAlias / /path/to/django/project/wsgi.py
        WSGIPassAuthorization On

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
    </VirtualHost>

Enable login/logout view in ``url.py``:

::

    from django.conf.urls import include

    urlpatterns = patterns('',
        ...
        url(r'^auth/', include('django_auth_krb.urls')),
        ...
    )

