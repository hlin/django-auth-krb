%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%define srcname django_auth_krb
%define version 0.2.0
%define release 1

Summary: Django kerberos authentication backend
Name: django-auth-krb
Version: %{version}
Release: %{release}%{?dist}
URL: https://pypi.python.org/pypi/%{srcname}/%{version}
Source0: https://pypi.python.org/packages/source/d/%{srcname}/%{srcname}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{srcname}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch

BuildRequires: python-setuptools

Requires: Django >= 1.10

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
* Fri Nov 4 2016 Haibo Lin <hlin@redhat.com> - 0.2.0-1
- Update for django 1.10
- Only support remote auth

* Wed Apr 2 2014 Haibo Lin <hlin@redhat.com> - 0.1.1-1
- Bug fix

* Wed Apr 2 2014 Haibo Lin <hlin@redhat.com> - 0.1.0-1
- Initial build

