Name:          jigdo
Version:       0.7.3
Release:       20%{?dist}
Summary:       Ease distribution of large files over the Internet

Group:         Applications/Internet
# Exception is permission to link with OpenSSL
License:       GPLv2 with exceptions
URL:           http://atterer.org/jigdo/
Source0:       http://atterer.org/sites/atterer/files/2009-08/jigdo/%{name}-%{version}.tar.bz2
Source1:       jigdo.desktop
Patch1:        jigdo-0.7.1-debug.patch
Patch2:        jigdo-0.7.3-gcc43.patch
BuildRequires: libdb-devel, bzip2-devel, curl-devel, /bin/awk, gettext
BuildRequires: desktop-file-utils, gtk2-devel >= 0:2.0.6
Requires:      wget

%description
Jigsaw Download, or short jigdo, is a tool designed to ease the
distribution of very large files over the internet, for example CD or
DVD images.  Its aim is to make downloading the images as easy for
users as a click on a direct download link in a browser, while
avoiding all the problems that server administrators have with hosting
such large files.  It accomplishes this by using the separate pieces
of any big file (such as the files contained within a CD/DVD image) to
create a special "template" file which makes reassembly of the big
file very easy for users who only have the pieces.

%package gui
Summary:       Jigdo graphical interface
Group:         Applications/Internet
Requires:      jigdo = %{version}-%{release}

%description gui
GTK2 frontend to jigdo.


%prep
%setup -q
%patch1 -p1 -b .debug
%patch2 -p1 -b .gcc43

%build
export LDFLAGS="$LDFLAGS -lpthread"
%configure --with-libdb=-ldb
make %{?_smp_mflags}

%install
make DESTDIR="$RPM_BUILD_ROOT" INSTALL_EXE="/usr/bin/install -c" install
# remove debian-specific script
rm -f   $RPM_BUILD_ROOT%{_bindir}/jigdo-mirror \
    $RPM_BUILD_ROOT%{_mandir}/man?/jigdo-mirror*
%find_lang %{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
        --vendor fedora \
%endif
        --dir $RPM_BUILD_ROOT/%{_datadir}/applications  \
        --add-category X-Fedora-Extra \
    %{SOURCE1}

# icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 0644 -p gfx/jigdo-icon.png $RPM_BUILD_ROOT%{_datadir}/pixmaps

# jigdo-mirror
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 scripts/jigdo-mirror $RPM_BUILD_ROOT%{_bindir}/jigdo-mirror

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc changelog COPYING README THANKS doc/*.html doc/TechDetails.txt doc/README-bindist.txt
%{_bindir}/jigdo-file
%{_bindir}/jigdo-lite
%{_bindir}/jigdo-mirror
%dir %{_datadir}/%{name}
%attr(0644,root,root) %{_mandir}/man[^3]/jigdo-file*
%attr(0644,root,root) %{_mandir}/man[^3]/jigdo-lite*

%files gui
%defattr(-,root,root,-)
%{_bindir}/jigdo
%{_datadir}/%{name}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%attr(0644,root,root) %{_mandir}/man[^3]/jigdo.*


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar  6 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.3-17
- Remove vendor prefix from desktop file for f19+ https://fedorahosted.org/fesco/ticket/1077
- Fix build by explicitly linking to libpthread

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.7.3-15
- fix the BR: db4-devel to BR: libdb-devel

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-13
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 10 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.7.3-11
- Split out gui into sub-package (#675917)
- Fix URL (#645835)
- Fix missing jigdo-mirror (#587578)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.7.3-7
- fix license tag

* Tue Mar 11 2008 Ian Burrell <ianburrell@gmail.com> - 0.7.3-6
- Add patch for gcc 4.3 support

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.3-5
- Autorebuild for GCC 4.3

* Mon Aug 27 2007 Ian M. Burrell <ianburrell@gmail.com> - 0.7.3-4
- Rebuild for db4 upgrade

* Tue Oct 31 2006 Ian Burrell <ianburrell@gmail.com> - 0.7.3-3
- Rebuild for curl update

* Mon Sep 11 2006 Ian Burrell <ianburrell@gmail.com> - 0.7.3-2
- Rebuild for FC6

* Sun Jun 25 2006 Ian Burrell <ianburrell@gmail> - 0.7.3-1
- Update to 0.7.3
- Remove obsolete patches

* Wed Mar  8 2006 Ian Burrell <ianburrell@gmail.com> - 0.7.2-3
- Remove dependency on w3c-libwww

* Sun Jan 29 2006 Ian Burrell <ianburrell@gmail.com> - 0.7.2-2
- Cleanup BuildRequires
- Patch for GCC 4.1

* Thu Dec 22 2005 Ian Burrell <ianburrell@gmail.com> - 0.7.2-1
- Update to 0.7.2
- Patch from CVS for 64-bit

* Fri Apr 15 2005 Charles R. Anderson <cra@wpi.edu> 0.7.1-4
- add gcc4 patch
- remove --enable-debug and patch out configure's removal of -g

* Fri Apr 15 2005 Charles R. Anderson <cra@wpi.edu> 0.7.1-3
- BR gettext instead
- move icon back to /usr/share/pixmaps
- add Category GTK to desktop file

* Fri Apr 15 2005 Charles R. Anderson <cra@wpi.edu> 0.7.1-2
- BR gettext-devel
- desktop category X-Fedora-Extra

* Mon Apr 11 2005 Charles R. Anderson <cra@wpi.edu> 0.7.1-1
- prepare for Fedora Extras
- update to 0.7.1
- remove unneeded db41 and debug patches

* Fri Jul 02 2004 Charles R. Anderson <cra@wpi.edu> 0:0.7.0-0.fdr.5
- install icon to /usr/share/jigdo/pixmaps and use that path in desktop file
- remove jigdo-mirror, since it is debian-specific

* Tue Jun 01 2004 Charles R. Anderson <cra@wpi.edu> 0:0.7.0-0.fdr.4
- don't strip binaries so debuginfo is created properly
- make jigdo-icon.png non-executable
- fixup buildroot path in jigdo-lite
- use more descriptive summary, description, and desktop file metadata

* Mon Feb 02 2004 Charles R. Anderson <cra@wpi.edu> 0:0.7.0-0.fdr.3
- Revise patch to compile against db-4.1+

* Mon Feb 02 2004 Charles R. Anderson <cra@wpi.edu> 0:0.7.0-0.fdr.2
- Add patch to compile against db-4.2.
- BuildRequires: zlib-devel, /bin/awk
- Requires: wget
- Integrate jigdo.desktop into .spec file

* Sat Jan 31 2004 Charles R. Anderson <cra@wpi.edu> 0:0.7.0-0.fdr.1
- Initial fedoraized release
- Install i18n files
- Install desktop file and icon
- Add a bunch of BuildRequires

* Mon Jan 26 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.6.2-4mdk
- Icons will be provided in the gfx subdirectory of the tarball

* Sun Jan 25 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.6.2-3mdk
- Jigdo compiles with gcc 2.96 now
- Only re-define the macros if they aren't yet defined

* Sat Jan 24 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.6.2-2mdk
- Make the SPEC be generic, so that it can be built on non-Mandrake
  machines

* Sat Jan 24 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.6.2-1mdk
- 0.6.2
- Remove patch1 - merged upstream

* Tue Jan 22 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.6.1-1mdk
- First Mandrake release

