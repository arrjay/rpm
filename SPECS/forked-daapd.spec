Name:		forked-daapd
Version:	21.0
Release:	2%{?dist}
Summary:	A DAAP protocol media server (iTunes, Rhythmbox, Soundbridge)

Group:		Applications/Multimedia
License:	GPLv2
URL:		https://github.com/ejurgensen/forked-daapd
# er, you need to use the real release source, since that includes the antlr3 pregen files and configure scripts.
Source0:	https://github.com/arrjay/forked-daapd/releases/download/21.0/forked-daapd-21.0.tgz
Source99:	forked-daapd-filter-requires.sh
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	sqlite-unlock_notify-devel antlr3-C-devel gperf libunistring-devel zlib-devel libconfuse-devel avahi-devel ffmpeg-devel mxml-devel libevent-devel libavl-devel libgcrypt-devel alsa-lib-devel
Requires:	sqlite-unlock_notify

# override the provide generator to not produce crap
%{?filter_setup:
%filter_from_provides /forked-daapd-sqlext.la/d
%filter_setup
}

# override the internal dependency generator with a shell script - this lets us require the sqlite-unlock_notify
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE99}

%description
This is a 'fork' of the original mt-daapd DAAP server, providing a few
improvements and support for things like multiple library volumes.

%prep
%setup -q

%build
export PKG_CONFIG_PATH=/usr/lib64/sqlite3-unlock_notify/pkgconfig
export CFLAGS="-I/usr/include/sqlite3-unlock_notify -Wl,-R/usr/lib64/sqlite3-unlock_notify/"
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/forked-daapd.conf
%{_libdir}/forked-daapd/forked-daapd-sqlext.la
%{_libdir}/forked-daapd/forked-daapd-sqlext.so
%{_sbindir}/forked-daapd
%{_mandir}/man8/forked-daapd.8.gz

%changelog
* Sat Aug 16 2014 <rj@arrjay.net> - 21.0-2
- set library search path in build stage so we pick the 'right' sqlite

* Sat Aug 16 2014 <rj@arrjay.net> - 21.0-1
- initial packaging
