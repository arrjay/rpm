Name: dmapd
Version: 0.0.70
Release: 1%{?dist}
Summary: A server that provides DAAP and DPAP shares

Group: Applications/Multimedia
License: GPLv2+
URL: http://www.flyn.org/projects/dmapd/
Source0: http://www.flyn.org/projects/%name/%{name}-%{version}.tar.gz

BuildRequires: libdmapsharing-devel >= 2.9.18, vips-devel >= 7.36, gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
Requires(pre): shadow-utils
Requires(post): systemd-units systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units

%description 
The dmapd project provides a GObject-based, Open Source implementation 
of DMAP sharing with the following features:

 o Support for both DAAP and DPAP

 o Support for realtime transcoding of media formats not natively 
 supported by clients

 o Support for many metadata formats, such as those associated with Ogg 
 Vorbis and MP3 (e.g., ID3)

 o Detection of video streams so that clients may play them as video

 o Use of GStreamer to support a wide range of audio and video CODECs

 o Caching of photograph thumbnails to avoid regenerating them each time 
 the server restarts

Dmapd runs on Linux and other POSIX operating systems. It has been 
used on OpenWrt Linux-based systems with as little as 32MB of memory 
to serve music, video and photograph libraries containing thousands of 
files.

%prep
%setup -q

%build
%configure                                      \
	--disable-static                        \
	--with-systemdsystemunitdir=%{_unitdir} \

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -f %{buildroot}%{_libdir}/libdmapd.la
rm -f %{buildroot}%{_libdir}/dmapd/%{version}/modules/*.la
rm -f %{buildroot}%{_sbindir}/dmapd-test
mkdir -p %{buildroot}%{_localstatedir}/cache/dmapd/DAAP
mkdir -p %{buildroot}%{_localstatedir}/cache/dmapd/DPAP
mkdir -p %{buildroot}%{_localstatedir}/run/dmapd
install -D -m 644 distro/dmapd.conf %{buildroot}%{_sysconfdir}/dmapd.conf

%clean
rm -rf %{buildroot}

%files 
%defattr(-, root, root, -)
%{_libdir}/*.so.0
%{_libdir}/*.so.%{version}
%{_libdir}/dmapd
%{_sbindir}/dmapd
%{_bindir}/dmapd-transcode
%{_bindir}/dmapd-hashgen
%config(noreplace) %{_sysconfdir}/dmapd.conf
%attr(0700,dmapd,root) %{_localstatedir}/cache/dmapd/
%attr(0700,dmapd,root) %{_localstatedir}/run/dmapd
%{_mandir}/*/*
%{_unitdir}/dmapd.service
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README FAQ 

%pre
getent group dmapd >/dev/null || groupadd -r dmapd
getent passwd dmapd >/dev/null || useradd -r -g dmapd -d / -s /sbin/nologin -c "dmapd Daemon" dmapd
exit 0

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then 
       /bin/systemctl enable dmapd.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
       /bin/systemctl --no-reload disable dmapd.service > /dev/null 2>&1 || :
       /bin/systemctl stop dmapd.service > /dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
       /bin/systemctl try-restart dmapd.service >/dev/null 2>&1 || :
fi

# FIXME: Remove once Fedora 15 EOL'ed.
# See http://fedoraproject.org/wiki/Packaging:ScriptletSnippets
%triggerun -- dmapd < 0.0.37-2
%{_bindir}/systemd-sysv-convert --save dmapd >/dev/null 2>&1 || :
/bin/systemctl --no-reload enable dmapd.service >/dev/null 2>&1 || :
/sbin/chkconfig --del dmapd >/dev/null 2>&1 || :
/bin/systemctl try-restart dmapd.service >/dev/null 2>&1 || :

%package devel
Summary: Files needed to develop modules using dmapd's libraries
Group: Development/Libraries
Requires: dmapd = %{version}-%{release}, pkgconfig

%description devel
This package provides the libraries, include files, and other 
resources needed for developing modules using dmapd's API.

%files devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/dmapd.pc
%{_includedir}/dmapd-*/
%{_libdir}/*.so
%ghost %attr(0755,dmapd,dmapd) %dir %{_localstatedir}/run/dmapd
%ghost %attr(0600,root,root) %{_localstatedir}/lock/subsys/dmapd

%changelog
* Mon Aug 25 2014 RJ Bergeron <rpm@arrjay.net> 0.0.70-1
- update to 0.0.70, build on el7(-ish)

* Fri Jul 05 2013 W. Michael Petullo <mike[@]flyn.org> 0.0.55-2
- Remove dmapd-vips-7.32.patch

* Fri Jul 05 2013 W. Michael Petullo <mike[@]flyn.org> 0.0.55-1
- New upstream version

* Thu Apr 11 2013 W. Michael Petullo <mike[@]flyn.org> 0.0.51-1
- New upstream version
- Build against GStreamer 1.0

* Sun Mar 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.50-7
- rebuild (libcfitsio)

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.0.50-6
- rebuild (OpenEXR)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.0.50-4
- rebuild due to "jpeg8-ABI" feature drop

* Mon Oct 29 2012 W. Michael Petullo <mike[@]flyn.org> - 0.0.50-3
- Another change to VIPS patch

* Mon Oct 29 2012 W. Michael Petullo <mike[@]flyn.org> - 0.0.50-2
- Update dmapd-vips-7.30.patch

* Mon Oct 29 2012 W. Michael Petullo <mike[@]flyn.org> - 0.0.50-1
- New upstream version
- Patch to use VIPS 7.30

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 W. Michael Petullo <mike[@]flyn.org> - 0.0.48-1
- New upstream version
- No longer need sed modification of configure.ac for VIPS 7.28
- No longer run autotools
- Do not require GraphicsMagick-devel; vips-devel will pull in requirements

* Fri Apr 13 2012 Tom Callaway <spot@fedoraproject.org> - 0.0.47-3
- rebuild for new ImageMagick

* Fri Mar 30 2012 W. Michael Petullo <mike[@]flyn.org> - 0.0.47-2
- Create /var/cache/dmapd/DAAP and DPAP

* Fri Mar 30 2012 W. Michael Petullo <mike[@]flyn.org> - 0.0.47-1
- New upstream version
- Apply database directory patch
- Apply glib include patch

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.0.45-2
- Rebuild for new libpng

* Mon Dec 05 2011 W. Michael Petullo <mike[@]flyn.org> - 0.0.45-1
- New upstream version
- Remove systemd conditionals

* Mon Sep 26 2011 W. Michael Petullo <mike[@]flyn.org> - 0.0.37-3
- Patch to use VIPS 7.26

* Mon Jul 11 2011 W. Michael Petullo <mike[@]flyn.org> - 0.0.37-2
- Use systemd on Fedora > 15

* Fri Feb 11 2011 W. Michael Petullo <mike[@]flyn.org> - 0.0.37-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.34-3
- Add file attributes for lock/subsys/dmapd

* Thu Dec 30 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.34-2
- Fix Bugzilla #656575

* Sun Nov 28 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.34-1
- New upstream version

* Sun Nov 28 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.33-1
- New upstream version

* Mon Nov 01 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.31-1
- New upstream version

* Wed Sep 29 2010 jkeating <> - 0.0.25-5
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.25-4
- Bump release in an attempt to build on Rawhide

* Wed Aug 04 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.25-3
- Use VIPS instead of GraphicsMagick

* Tue Jun 22 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.25-2
- Don't install dmapd-test

* Tue Jun 22 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.25-1
- New upstream version

* Fri Jun 04 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.24-1
- New upstream version

* Wed Feb 17 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.23-1
- New upstream version, set User= in dmapd.conf

* Fri Feb 05 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.22-1
- New upstream version

* Thu Jan 28 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.21-1
- New upstream version
- no longer install /etc/sysconfig/dmapd, use /etc/dmapd.conf
- no longer create /var/db/dmapd*

* Thu Jan 14 2010 W. Michael Petullo <mike[@]flyn.org> - 0.0.18-2
- use macro for init directory throughout

* Fri Dec 04 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.18-1
- New upstream version
- reorder specfile blocks to resemble output of rpmdev-newspec
- add noreplace to config file
- do not depend on avahi-, dbus- or libsoup-devel, just libdmapsharing
- make pre, post, etc. requirements satisfy Fedora SysV init docs

* Sun Nov 22 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.17-1
- New upstream version
- Fix ldconfig placement
- No empty NEWS
- Move data directory to /var/db/dmapd

* Sat Nov 21 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.16-1
- New upstream version
- Move %%doc to %%files
- No empty FAQ
- Require GraphicsMagick-devel

* Tue Nov 10 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.15-1
- New upstream version
- Require dbus-devel to build
- Properly set permissions of /etc/sysconfig/dmapd
- Run ldconfig
- Fix user creation

* Thu Jul 23 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.14-1
- New upstream version
- Fix URL

* Thu May 07 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.10-1
- New upstream version
- Use %%{buildroot} exclusively
- Add requirements for pre, post, preun and postun
- Remove disttags from changelog
- Remove extra defattr

* Sun Jan 11 2009 W. Michael Petullo <mike[@]flyn.org> - 0.0.8-1
- Initial package for Fedora

