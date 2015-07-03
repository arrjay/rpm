%global commit 582ec614ab749c9b109d3184021c8e0eb7d3f147
%global shortcommit %(/bin/bash -c 'c=%{commit}; echo ${c:0:7}')

Name: redshift
Version: 1.8
Release: 1%{dist}
Summary: Adjusts the color temperature of your screen according to time of day
Group: Applications/System
License: GPLv3+
URL: http://jonls.dk/redshift/
Source0: https://github.com/jonls/redshift/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
# Remove Ubuntu specific geoclue provider
Patch0: redshift-geoclue-provider.patch
BuildRequires: gettext-devel
BuildRequires: libXrandr-devel
BuildRequires: libXxf86vm-devel
BuildRequires: GConf2-devel
BuildRequires: geoclue-devel

%description
Redshift adjusts the color temperature of your screen according to your
surroundings. This may help your eyes hurt less if you are working in
front of the screen at night.

The color temperature is set according to the position of the sun. A
different color temperature is set during night and daytime. During
twilight and early morning, the color temperature transitions smoothly
from night to daytime temperature to allow your eyes to slowly
adapt.

This package provides the base program.

%package -n %{name}-gtk
Summary: GTK integration for Redshift
Group: Applications/System
BuildRequires: python2
BuildRequires: desktop-file-utils
Requires: pygtk2
Requires: pyxdg
Requires: %{name} = %{version}-%{release}
Obsoletes: gtk-%{name} < 1.7-7

%description -n %{name}-gtk
This package provides GTK integration for Redshift, a screen color 
temperature adjustment program.

%prep
%setup -qn %{name}-%{commit}
%patch0 -p1
autoreconf -i -f

%build
%configure
make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL="install -p"
%find_lang %{name}
desktop-file-validate %{buildroot}%{_datadir}/applications/redshift-gtk.desktop

%post -n %{name}-gtk
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n %{name}-gtk
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n %{name}-gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/redshift
%{_mandir}/man1/*

%files -n %{name}-gtk
%defattr(-,root,root,-)
%{_bindir}/redshift-gtk
%{python_sitelib}/*
%{_datadir}/icons/hicolor/scalable/apps/redshift*.svg
%{_datadir}/applications/redshift-gtk.desktop

%changelog
* Thu Nov 30 2013 Milos Komarcevic <kmilos@gmail.com> - 1.8-1
- Update to 1.8 (#1029155)
- Source comes from GitHub now

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Milos Komarcevic <kmilos@gmail.com> - 1.7-5
- Run autoreconf to support aarch64 (#926436)
- Backport fix for geoclue client check (#954014)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 9 2011 Milos Komarcevic <kmilos@gmail.com> - 1.7-1
- Update to 1.7
- Add geoclue BuildRequires
- Change default geoclue provider from Ubuntu GeoIP to Hostip
- Remove manual Ubuntu icons uninstall

* Sun Feb 27 2011 Milos Komarcevic <kmilos@gmail.com> - 1.6-3
- Fix for clock applet detection (#661145)
- Require pyxdg explicitly (#675804)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 13 2010 Milos Komarcevic <kmilos@gmail.com> - 1.6-1
- Update to 1.6
- Remove BuildRoot tag and clean section

* Thu Aug 26 2010 Milos Komarcevic <kmilos@gmail.com> - 1.5-1
- Update to 1.5
- Install desktop file

* Mon Jul 26 2010 Milos Komarcevic <kmilos@gmail.com> - 1.4.1-2
- License updated to GPLv3+
- Added python macros to enable building on F12 and EPEL5
- Specific python version BR
- Subpackage requires full base package version
- Increased build log verbosity
- Preserve timestamps on install

* Thu Jun 17 2010 Milos Komarcevic <kmilos@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Thu Jun 10 2010 Milos Komarcevic <kmilos@gmail.com> - 1.3-1
- Initial packaging
