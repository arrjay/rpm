Name:           arrjay-release
Version:        6
Release:        4
Summary:        Arrjay.net Packages for Enterprise Linux repository configuration

Group:          System Environment/Base
License:        BSD

# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0:        RPM-GPG-KEY-arrjay.net
Source1:	arrjay.repo

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

%description
This package contains the arrjay.net repository GPG key

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-arrjay.net

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Fri Aug 15 2015 <rj@arrjay.net> - 6-4
- fix repo tag

* Fri Aug 15 2015 <rj@arrjay.net> - 6-3
- drop EPEL requirement as the repo doesn't consistently need it...
- add repo file
- sign it

* Thu Aug 14 2014 <rj@arrjay.net> - 6-2
- rebuild from lost rpmbuilder

* Sat Mar 30 2013 <rj@arrjay.net> - 6-1
- Initial Package
