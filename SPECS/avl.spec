Name:           libavl
Version:        0.3.5
Release:        2%{?dist}
Summary:        AVL tree manipulation library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://git.fruit.je/avl
# Upstream development is API-incompatible per discussion with its author,
# he suggested using Debian orig.tar.gz
Source0:        http://ftp.debian.org/debian/pool/main/liba/libavl/libavl_0.3.5.orig.tar.gz
Patch0:         avl-0.3.5-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library consists of a set of functions to manipulate AVL trees. AVL
trees are very efficient balanced binary trees, similar to red-black
trees. The functions in this library can handle any kind of payload and
search key type.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n avl-%{version}
%patch0 -p1 -b .build

%build
export CFLAGS="%{optflags}"
make -f GNUmakefile %{?_smp_mflags}  libdir=%{_libdir}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} libdir=%{_libdir}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -exec chmod +x '{}' \;

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Fri Aug 15 2014 RJ Bergeron <rpm@arrjay.net> - 0.3.5-2
- resurrected from the dead, and renamed to libavl, as upstream now has some other avl package.

* Mon Dec 06 2010 Matěj Cepl <mcepl@redhat.com> - 0.3.5-1
- Experimental build for review.
