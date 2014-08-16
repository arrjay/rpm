Name:		antlr3-C-lite
Version:	3.4
Release:	1%{?dist}
Summary:	C bindings for ANTLR-generated parsers
Provides:	antlr3-C

Group:		Development/Libraries
License:	BSD
URL:		http://www.antlr3.org/
Source0:	http://www.antlr3.org/download/C/libantlr3c-3.4.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc

%description
This package is *just* the runtime libraries for antlr3-C, it does not include
any of the utilities from a full antlr3 package.

%package devel
Summary:	Header files to link with ANTLR-C bindings
Requires:	%{name} = %{version}-%{release}
Provides:	antlr3-C-devel

%description devel
This package is the link headers and static libraries for antlr3-C, it does not
include any of the utilities from a full antlr3 package.

%prep
%setup -q -n libantlr3c-%{version}

%build
%ifarch x86_64
%configure --enable-64bit
%else
%configure
%endif
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la


%changelog
* Sat Aug 16 2014 RJ Bergeron <rpm@arrjay.net> - 3.4-1
- initial build
