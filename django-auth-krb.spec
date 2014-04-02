%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%define srcname django_auth_krb
%define version 0.1.1
%define release 1

Summary:       Django kerberos authentication backend
Name:          django-auth-krb
Version:       %{version}
Release:       %{release}
URL:           https://pypi.python.org/pypi/django_auth_krb/0.1.0
Source0:       https://pypi.python.org/packages/source/d/django_auth_krb/django_auth_krb-0.1.0.tar.gz
License:       MIT
Group:         Development/Libraries
BuildRoot:     %{_tmppath}/%{srcname}-%{version}-%{release}-buildroot
Prefix:        %{_prefix}
BuildArch:     noarch

BuildRequires: python-setuptools

Requires:      Django >= 1.3
Requires:      python-kerberos >= 1.1

%description
Django kerberos authentication backend.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.rst
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info


%changelog
* Wed Apr 2 2014 Haibo Lin <hlin@redhat.com> - 0.1.0-1
- Initial build

