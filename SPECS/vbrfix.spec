Name:		vbrfix
Version:	0.24
Release:	1%{?dist}
Summary:	corrects MP3 files that have incorrect VBR information

Group:		Applications/Multimedia
License:	GPL
Source0:	http://archive.ubuntu.com/ubuntu/pool/universe/v/vbrfix/vbrfix_0.24.orig.tar.gz
Patch0:		fix-typos.diff
Patch1:		fix-endianness.diff
Patch2:		gcc-4.3.diff
Patch3:		exit-error-code.diff
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc gcc-c++

%description
small command-line utility to regenerate VBR data tags

%prep
%setup -q -n vbrfixc-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mv $RPM_BUILD_ROOT/%{_bindir}/vbrfixc $RPM_BUILD_ROOT/%{_bindir}/vbrfix


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/usr/bin/vbrfix

%changelog
* Mon Aug 18 2014 <rj@arrjay.net> - 0.24-1
- initial release
