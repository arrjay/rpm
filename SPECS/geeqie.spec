%bcond_with lcms1

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%define upstreamversion 1.1
%global _hardened_build 1

Summary: Image browser and viewer
Name: geeqie
Version: 1.1
Release: 22%{?dist}
License: GPLv2+
Group: User Interface/X
Source: http://downloads.sf.net/sourceforge/geeqie/%{name}-%{upstreamversion}.tar.gz
URL: http://geeqie.sourceforge.net/

# add -Wl,--as-needed without disturbing %%configure macro
Patch0: geeqie-1.1-LDFLAGS.patch
# from master branch to fix regression
Patch1: geeqie-1.1-bar_keywords.c.diff
# in upstream bug tracker
Patch2: geeqie-1.0-fix-fullscreen.patch
# bz 889897
# reported upstream: http://sourceforge.net/p/geeqie/patches/28/
Patch3: geeqie-1.0-double_generic_dialog_close.patch
# from master
Patch4: geeqie-1.1-editors-NULL.patch
# reported upstream
# https://sourceforge.net/tracker/?func=detail&atid=1054680&aid=3602709&group_id=222125
Patch5: geeqie-1.1-filedata-change-notification.patch
# reported upstream
# https://sourceforge.net/tracker/?func=detail&aid=3603866&group_id=222125&atid=1054680
# avoid crash due to non-existent files in history path_list and collections
# improved patch in gitorious merge request 5
Patch6: geeqie-1.1-collection-and-history-inexistent-files.patch
# reported upstream
# https://sourceforge.net/tracker/?func=detail&aid=3605406&group_id=222125&atid=1054682
Patch7: geeqie-1.1-large-files.patch
# LCMS2 patch originally from Geeqie-devel mailing-list
# but modified/revised for bug-fixes
Patch8: geeqie-1.1-lcms2.patch
# from master
Patch9: geeqie-1.1-percent-char-in-filenames.patch

BuildRequires: gtk2-devel
%if %{with lcms1}
BuildRequires: lcms-devel
%else
BuildRequires: lcms2-devel
%endif
BuildRequires: exiv2-devel
BuildRequires: lirc-devel
BuildRequires: libjpeg-devel
#BuildRequires: libtiff-devel
BuildRequires: gettext intltool desktop-file-utils
BuildRequires: gnome-doc-utils

# for the included plug-in scripts
BuildRequires: exiv2 fbida ImageMagick zenity
Requires: exiv2 fbida ImageMagick zenity
# at run-time, it is only displayed in menus, if ufraw executable is available
%if 0%{?fedora}
BuildRequires: ufraw
%endif


# Experimental, still disabled by default.
#BuildRequires: libchamplain-gtk-devel >= 0.4


%description
Geeqie has been forked from the GQview project with the goal of picking up
development and integrating patches. It is an image viewer for browsing
through graphics files. Its many features include single click file
viewing, support for external editors, previewing images using thumbnails,
and zoom.


%prep
%setup -q -n %{name}-%{upstreamversion}
# guard against missing executables at (re)build-time,
# these are needed by the plug-in scripts
for f in exiftran exiv2 mogrify zenity ; do
    type $f || exit -1
done
%if 0%{?fedora}
for f in ufraw-batch ; do
    type $f || exit -1
done
%endif
%patch0 -p1 -b .LDFLAGS
%patch1 -p1 -b .keywords
%patch2 -p1 -b .fix-fullscreen
%patch3 -p1 -b .fix-dialog-close
%patch4 -p1 -b .editors-NULL
%patch5 -p1 -b .filedata-notification
%patch6 -p1 -b .collection-inexistent-files
%patch7 -p1 -b .large-files
%if ! %{with lcms1}
%patch8 -p1
autoreconf -f -i
%endif
%patch9 -p1 -b .percent-char-in-filenames

%build
%configure --enable-lirc --disable-tiff \
    --with-readmedir=%{_pkgdocdir}
make %{?_smp_mflags}


%install
mkdir -p ${RPM_BUILD_ROOT}%{_pkgdocdir}/html
make DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p" install

# guard against missing HTML tree
[ ! -f ${RPM_BUILD_ROOT}%{_pkgdocdir}/html/index.html ] && exit -1

# We want these _docdir files in GQ_HELPDIR.
install -p -m 0644 AUTHORS COPYING NEWS README* TODO \
    ${RPM_BUILD_ROOT}%{_pkgdocdir}
rm -f ${RPM_BUILD_ROOT}%{_pkgdocdir}/ChangeLog

desktop-file-install \
    --delete-original \
%if 0%{?fedora} < 19
    --vendor fedora \
%endif
    --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%find_lang %name


%post
update-desktop-database &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :


%files -f %{name}.lang
%doc %{_pkgdocdir}/
%{_bindir}/%{name}*
%{_prefix}/lib/%{name}/
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}/
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/*%{name}.desktop


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-21
- Retrieve a printable CMS image profile and screen profile description
  to avoid crashing g_markup (#1110073).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-19
- Don't print CMS screen profileID garbage that crashes g_markup
  (this should also fix #1051660).

* Tue May 27 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-18
- Merge fix for avoiding crash due to inexistent files in collections.
  This also replaces the history path_list patch.

* Sun Jan 26 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-17
- Merge image-overlay.c fix for handling of filenames with % in them.

* Mon Dec  9 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-16
- Add LCMS2 patch from Geeqie-devel list, fix HAVE_LCMS and build with
  lcms2-devel instead of lcms-devel.

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.1-15
- rebuild (exiv2)

* Sat Nov 16 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-14
- Conditionalize ufraw BR/R for Fedora, since it's not available with
  RHEL and EPEL and is optional at run-time.
- Drop %%defattr usage.

* Tue Aug  6 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-13
- For F-20 unversioned docdirs feature we need to build with
  configure --with-readmedir=... to override the internal GQ_HELPDIR.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun  7 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-11
- Define _hardened_build 1 to please rpm-chksec.

* Wed Feb 20 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-10
- Include config.h earlier in some files, so the large file support
  definition is available early enough for e.g. sys/stat.h
- Drop the aging Obsoletes tag for gqview.

* Fri Feb  8 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-9
- Avoid abort when opening non-existing paths from history.

* Fri Feb  1 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-8
- Drop new idle callback from file_data_send_notification() as it
  causes breakage (in the duplicate finder, for example).

* Sun Jan 27 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-7
- Check exec value for NULL in src/editors.c
- Fedora >= 19: Drop ancient "fedora" vendor prefix from desktop file.

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.1-6
- rebuild due to "jpeg8-ABI" feature drop

* Mon Dec 24 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-5
- Fix crash upon escaping from generic dialogs.

* Thu Dec 13 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-4
- Build with --disable-tiff, as the custom libtiff loader crashes
  for some images as mentioned on geeqie-devel list.

* Thu Nov 22 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-3
- Merge a patch to fix fullscreen mode.

* Sun Aug 26 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-2
- Merge bar_keywords.c master commit to fix regression.

* Tue Aug 14 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-1
- Fix license tag to GPLv2+ as GPL3 (only in file COPYING) had been
  added only temporarily for 1.0-alpha1.
- BR libjpeg-devel libtiff-devel
- Upgrade to 1.1 (also to reduce patch count).

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May  3 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-17
- Complete previous rebuild that failed unexpectedly because html docdir in
  buildroot had not been created (Rawhide only). Now create it explicitly
  at beginning of %%install.

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0-16
- rebuild (exiv2)

* Fri Jan  6 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-15
- rebuild for GCC 4.7 as requested

* Sat Nov  5 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-14
- Link with --as-needed.

* Sun Oct 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-13
- Cherry-pick a few commits (from Vladimir Nadvornik, Klaus Ethgen
  and Vladislav Naumov). With the modified filelist_sort_compare_filedata
  method, Geeqie passes another stress test I've created in order
  to track down rare file_data_unref crashes.

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.0-12
- rebuild (exiv2)

* Tue Aug  9 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-11
- Patch another place where not to exif_free_fd NULL ptr (#728802).

* Fri Apr 15 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-10
- Let's see how we do with a simpler vflist_setup_iter_recursive().

* Sat Mar  5 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-9
- Patch filedata.c check_case_insensitive_ext to accept the first
  tested file name ext and not accept multiple combinations due to
  case-insensitive fs.

* Fri Mar  4 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-8.test1
- Patch filedata.c check_sidecars to avoid adding a file as its own
  sidecar. Case-insensitive sidecar file name generation may not be
  enough if a fs stat is used in conjunction with a case-insensitive fs.

* Tue Feb 22 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-8
- Fix file cache NULL pointer crash in exif-common.c (#679256).
- Patch and build with large file support.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.0-6
- rebuild (exiv2)

* Thu Sep  9 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-5
- Make gqview "Obsoletes" tag conditional: for Fedora newer than 13.

* Mon Jul 26 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-4
- Replace old gqview < 2.0.4-13 with geeqie.

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0-3 
- rebuild (exiv2)

* Tue Apr  6 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-2
- require exiv2, ImageMagick, fbida, ufraw, zenity for plug-in scripts
- BR gnome-doc-utils for HTML documentation (and "Help > Contents" menu)

* Fri Feb 19 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-1
- update to 1.0 final release
 
* Mon Jan 04 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.20.beta2
- rebuild (exiv2)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.19.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.18.beta2
- update to beta2 tarball
- BR intltool
- print-pagesize.patch enabled in 1.0beta2 (#222639)

* Thu May 14 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.16.beta1
- update to beta1 tarball

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.15.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.14.alpha3
- fetch src/utilops.c change from svn 1385 for metadata crash-fix

* Wed Jan 28 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.13.alpha3
- ignore .helpdir/.htmldir values in geeqierc to fix "Help"
- add --enable-lirc again to build with LIRC

* Mon Jan 26 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.12.alpha3
- update to alpha3 tarball

* Thu Jan 22 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.11.alpha2.1341svn
- update to svn 1341 for pre-alpha3 testing (image metadata features)
- drop obsolete patches remote-blank and float-layout

* Wed Dec 24 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.11.alpha2.1307svn
- update to svn 1307 for "Safe delete"

* Thu Dec 18 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.11.alpha2.1299svn
- drop desktop file Exec= invocation patch (no longer necessary)

* Thu Dec 18 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.10.alpha2.1299svn
- update to svn 1299 for new exiv2
- disable LIRC support which is broken

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.9.alpha2
- respin (exiv2)

* Tue Aug 12 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.8.alpha2
- fix float layout for --blank mode

* Mon Aug 11 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.7.alpha2
- fix options --blank and -r file:

* Thu Jul 31 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.6.alpha2
- update to 1.0alpha2 (now GPLv3)
- build with new LIRC support

* Wed Jun 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.5.alpha1 
- respin for exiv2

* Thu May  8 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.4.alpha1
- scriptlets: run update-desktop-database without path
- drop dependency on desktop-file-utils
- drop ChangeLog file as it's too low-level

* Fri Apr 25 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.3.alpha1
- package GQview fork "geeqie 1.0alpha1" based on Fedora gqview.spec
- BR lcms-devel exiv2-devel
- update -desktop and -editors patch
- update spec file with more dir macros

