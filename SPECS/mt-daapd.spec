%global username mt-daapd
%global homedir %_var/lib/%username
%global gecos mt-daapd

%define basever 1696

Summary: An iTunes-compatible media server
Name: mt-daapd
Epoch: 2
Version: r%{basever}
Release: 3%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Source0: http://distcache.FreeBSD.org/ports-distfiles/%{name}-svn-%{basever}.tar.gz
Source1: %{name}.service
Patch0: mt-daapd-svn-defaults.patch
Patch1: mt-daapd-svn-fedora.patch
Patch2: patch-plugins_out-daap.c
Patch3: mt-daapd.conf.patch
Url: http://www.fireflymediaserver.org/
BuildRequires: gdbm-devel, avahi-devel, zlib-devel
BuildRequires: flac-devel, libogg-devel, libvorbis-devel
BuildRequires: libid3tag-devel, sqlite-devel, gcc-c++
%if 0%{?rhel} >= 7
BuildRequires: systemd-units
Requires(pre):   /usr/sbin/useradd
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(pre): shadow-utils
%endif

%description
The purpose of this project is built the best server software to serve
digital music to the Roku Soundbridge and iTunes; to be able to serve
the widest variety of digital music content over the widest range of
devices.

%prep
%setup -q -n %{name}-svn-%{basever}
%patch0 -p1 -b .defaults
%patch1 -p1 -b .fedora
%patch2 -p0 -b .itunes10
%patch3 -p1 -b .conf

%build
%configure --enable-avahi --enable-oggvorbis --enable-sqlite3 --enable-flac
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_localstatedir}/cache/mt-daapd
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0640 contrib/mt-daapd.conf %{buildroot}%{_sysconfdir}/
%if 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_unitdir}
install %{SOURCE1} %{buildroot}%{_unitdir}/
%else
mkdir -p %{buildroot}%{_initddir}
install -m 0755 contrib/init.d/mt-daapd-fedora %{buildroot}%{_initddir}/mt-daapd
%endif

%pre
getent group %{username} > /dev/null || groupadd -r %{username}
getent passwd %{username} > /dev/null || \
    useradd -r -g %{username} -d %{homedir} -s /sbin/nologin \
    -c '%{gecos}' %{username}
exit 0

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
%if 0%{?rhel} >= 7
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add mt-daapd
%endif
fi


%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
%if 0%{?rhel} >= 7
    /bin/systemctl --no-reload disable mt-daapd.service > /dev/null 2>&1 || :
    /bin/systemctl stop mt-daapd.service > /dev/null 2>&1 || :
%else
    /sbin/service mt-daapd stop > /dev/null 2>&1
    /sbin/chkconfig --del mt-daapd
%endif
fi

%if 0%{?rhel} >= 7
%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mt-daapd.service >/dev/null 2>&1 || :
fi
%endif

%files
%config(noreplace) %{_sysconfdir}/mt-daapd.conf
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initddir}/mt-daapd
%endif
%{_sbindir}/mt-daapd
%{_datadir}/mt-daapd
%{_bindir}/mt-daapd-ssc.sh
%{_bindir}/wavstreamer
%{_libdir}/mt-daapd/plugins/*
%attr(0700,mt-daapd,root) %{_localstatedir}/cache/mt-daapd
%doc AUTHORS COPYING CREDITS NEWS README TODO

%changelog
* Wed Aug 27 2014 RJ Bergeron <rpm@arrjay.net> - 2:r1696-3
- bring back systemd units for EL7 platforms.
- patch sample config to mention symlink following

* Sun Aug 17 2014 RJ Bergeron <rpm@arrjay.net> - 2:r1696-2
- patch for iTunes 10 compatibility.

* Sun Aug 17 2014 RJ Bergeron <rpm@arrjay.net> - 2:r1696-1
- switch to last workable svn release (what freebsd uses)

* Sun Aug 17 2014 RJ Bergeron <rpm@arrjay.net> - 1:0.2.4.2-15
- Rebuild for EL6, drop systemd and fedora user management

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.2.4.2-11
- improve systemd service (forking, wants avahi, order after avahi)

* Fri Sep 09 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.2.4.2-10
- fix systemd scriptlets

* Thu Sep 08 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.2.4.2-9
- convert to systemd

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct  2 2010 Mark Chappell <tremble@fedoraproject.org> - 1:0.2.4.2-7
- Remove INSTALL from files list as per package guidelines

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 18 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-4
   - Change initscript priority to 98, so that mt-daapd starts after avahi.

* Fri Sep 26 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-3
   - Update init script, fix Fedora Bugzilla #461719.

* Thu May 15 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-2
   - Bump epoch.

* Wed May 14 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-1
   - New upstream version.
   - Remove check-input patch; it's upstream.

* Fri Apr 18 2008 W. Michael Petullo <mike[at]flyn.org> - 0.9-0.2.1696
   - Apply patch by Nico Golde to fix integer overflow, Bugzilla #442688.

* Tue Feb 26 2008 W. Michael Petullo <mike[at]flyn.org> - 0.9-0.1.1696
   - New upstream version.

* Mon Dec 24 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-5
   - Change license to GPLv2+.
   - Add requires(post) chkconfig.
   - Change permissions of mt-daapd.playlist.
   - Patch so that service is not enabled by default.

* Thu Dec 20 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-4
   - Build with --enable-avahi to avoid Apache / GPL license mix.
   - Build with Vorbis support.
   - Change BuildRequires accordingly.

* Sat Dec 15 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-3
   - Fix versions in changelog.
   - Use %%config(noreplace) for config files.   
   - Change group to Applications/Multimedia.
   - Don't chkconfig on.
   - Install mt-daapd.conf chmod 0640.
   - Set proper license.

* Thu Dec 13 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-2
   - BuildRequire zlib-devel, which is required for libid3tag-devel.

* Mon Dec 10 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-1
   - New upstream verion.

* Sat Jul 21 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4-3
   - Own /usr/share/mt-daapd.

* Sun Jul 15 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4-2
   - Use directory macros.
   - Don't use %%makeinstall.
   - use cp -P.

* Sat Jul 14 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4-1
   - Initial Fedora RPM release candidate.
