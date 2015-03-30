# Component versions
%define appres 1.0.4
%define editres 1.0.6
%define listres 1.0.3
%define viewres 1.0.4

Summary:    X.Org X11 X resource utilities
Name:       xorg-x11-resutils
Version:    7.5
Release:    11%{?dist}
License:    MIT
URL:        http://www.x.org

Source0:    http://www.x.org/pub/individual/app/appres-%{appres}.tar.bz2
Source1:    http://www.x.org/pub/individual/app/editres-%{editres}.tar.bz2
Source2:    http://www.x.org/pub/individual/app/listres-%{listres}.tar.bz2
Source3:    http://www.x.org/pub/individual/app/viewres-%{viewres}.tar.bz2

Patch0:     editres-1.0.6-format-security.patch

BuildRequires:  libtool
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Provides:   appres = %{appres}
Provides:   editres = %{editres}
Provides:   listres = %{listres}
Provides:   viewres = %{viewres}

%description
A collection of utilities for managing X resources.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3
%patch0 -p0 -b .fmt

%build
# Build all apps
{
    for app in * ; do
        pushd $app
            autoreconf -vif
            %configure --disable-xprint
            make %{?_smp_mflags}
        popd
    done
}

%install
# Install all apps
{
    for app in * ; do
        pushd $app
            %make_install
        popd
    done
}

%files
%{_bindir}/appres
%{_bindir}/editres
%{_bindir}/listres
%{_bindir}/viewres
%{_datadir}/X11/app-defaults/Editres
%{_datadir}/X11/app-defaults/Editres-color
%{_datadir}/X11/app-defaults/Viewres
%{_datadir}/X11/app-defaults/Viewres-color
%{_mandir}/man1/appres.1*
%{_mandir}/man1/editres.1*
%{_mandir}/man1/listres.1*
%{_mandir}/man1/viewres.1*

%changelog
* Tue Nov 04 2014 Simone Caronni <negativo17@gmail.com> - 7.5-11
- Clean up SPEC file, fix rpmlint warnings.
- Simplify build requirements.
- appres 1.0.4
- listres 1.0.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 09 2014 Adam Jackson <ajax@redhat.com> 7.5-9
- Fix FTBFS with -Werror=format-security 

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.5-7
- autoreconf for aarch64

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.5-5
- editres 1.0.6
- viewres 1.0.4

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-1
- appres 1.0.3
- editres 1.0.5
- viewres 1.0.3
- listres 1.0.2

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 7.1-10
- Fixed bad directory ownership of /usr/share/X11
