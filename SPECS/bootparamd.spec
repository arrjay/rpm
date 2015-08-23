Summary: A server process which provides boot information to diskless clients
Name: bootparamd
Version: 0.17
Release: 43%{?dist}
License: BSD
Group: System Environment/Daemons
Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1: bootparamd.service
Patch: bootparamd-manpage-63567.patch
Patch1: bootparamd-resolver.patch
Patch2: bootparamd-debug.patch
Patch3: bootparamd.fast-dns.patch
Patch4: bootparamd-resolver-fix.patch
Patch5: bootparamd-get-router.patch
Patch6: bootparamd-err.patch
Patch7: bootparamd-byteorder.patch
Patch8: bootparamd-getopt.patch

BuildRequires: systemd-units
Requires(post):	systemd-units
Requires(post):	systemd-sysv
Requires(preun):systemd-units
Requires(postun): systemd-units

Requires: portmap
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The bootparamd process provides bootparamd, a server process which
provides the information needed by diskless clients in order for them
to successfully boot.  Bootparamd looks first in /etc/bootparams for an
entry for that particular client; if a local bootparams file doesn't
exist, it looks at the appropriate Network Information Service (NIS)
map.  Some network boot loaders (notably Sun's) rely on special boot
server code on the server, in addition to the RARP and TFTP servers.
This bootparamd server process is compatible with SunOS bootparam clients
and servers which need that boot server code.

You should install bootparamd if you need to provide boot information to
diskless clients on your network.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch -p1
%patch1 -p1
%patch2 -p1 -b .unblocksignals
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .router
%patch6 -p1 -b .err
%patch7 -p1 -b .byteorder
%patch8 -p1 -b .getopt

%build
sh configure --with-c-compiler=gcc
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -D_BSD_SOURCE \$(f_PIE),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    ' MCONFIG
%ifarch s390 s390x 
export f_PIE="-fPIE"
%else
export f_PIE="-fpie"
%endif
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}

mkdir -p "${RPM_BUILD_ROOT}%{_unitdir}/"
cp -a "%{SOURCE1}" "${RPM_BUILD_ROOT}%{_unitdir}/"

make INSTALLROOT=%{buildroot} install

%clean
rm -rf %{buildroot}

%post
%systemd_post bootparamd.service

%preun
%systemd_preun bootparamd.service

%postun
%systemd_postun_with_restart bootparamd.service

%files
%defattr(-,root,root)
%{_sbindir}/rpc.bootparamd
%{_bindir}/callbootd
%{_mandir}/man8/rpc.bootparamd.*
%{_mandir}/man8/bootparamd.*
%{_unitdir}/*

%changelog
* Fri Jul 10 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 0.17-43
- fix unit-file

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 0.17-37
- Use int instead of char for return of getopt (#891105)

* Wed Aug 22 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 0.17-36
- Use %systemd macros (#850017)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 05 2011 Lukas Nykryn <lnykryn@redhat.com> - 0.17-33
- Add postun section in spec file

* Thu Sep 05 2011 Lukas Nykryn <lnykryn@redhat.com> - 0.17-32
- Migration from SysV daemon handling to systemd (#722629)

* Thu Aug 11 2011 Lukas Nykryn <lnykryn@redhat.com> - 0.17-31
- fixed byte order
- reverted changes in get-router.patch - it was impossible to build package

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17-27
- Autorebuild for GCC 4.3

* Mon Oct 08 2007 Ondrej Dvoracek <odvorace@redhat.com> - 0.17-26
- added LSB header in the initscript
- corrected issues from merge review (#225623)

* Wed May 30 2007 Ondrej Dvoracek <odvorace@redhat.com> - 0.17-25
- corrected init script (#237824)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-24.devel.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17-24.devel.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17-24.devel.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Martin Stransky <stransky@redhat.com> 0.17-24.devel
- fix for #177902 - Callbootd segfaults when connecting to 
  nonexistent server

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Aug 17 2005 Martin Stransky <stransky@redhat.com> 0.17-23.devel
- added patch for #143032, written by Robert Jelinek (jelinekr@ms.com)
- updated a man page

* Thu Feb 17 2005 Martin Stransky <stransky@redhat.com>
- rebuilt

* Thu Jan 13 2005 Martin Stransky <stransky@redhat.com> 0.17-20.devel
- fix DNS look-up extension patch (#144933)

* Mon Dec 20 2004 Martin Stransky <stransky@redhat.com>
- fast DNS look-up extension

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt
- Add debug patch (which is really there to fix a bug in signal checking)

* Thu Jun 10 2004 Dan Walsh <dwalsh@redhat.com> 0.17-16
- Add resolver patch

* Fri May 14 2004 Thomas Woerner <twoerner@redhat.com> 0.17-16
- compiling PIE

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 23 2002 Tim Powers <timp@redhat.com> 0.17-12
- bump and rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com>
- Fix 63567 and don't strip binaries.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Tue Feb  6 2001 Trond Eivind Glomsrod <teg@redhat.com>
- i18nize initscript
- exit cleanly if no /etc/bootparams

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Preston Brown <pbrown@redhat.com>
- move initscript
 
* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- FHS packaging
- 0.17

* Thu Feb 03 2000 Erik Troan <ewt@redhat.com>
- gzipped man pages

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Fri Sep 25 1999 Bill Nottingham <notting@redhat.com>
- *sigh*.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initrscript munging

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- removed triggerpostun.

* Fri May 01 1998 Jeff Johnson <jbj@redhat.com>
- added triggerpostun

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Thu Jan 08 1998 Erik Troan <ewt@redhat.com>
- updated initscript to include functions
- fixed 'stop' action of initscript
- added requirement for portmap

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- added an initscript

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
