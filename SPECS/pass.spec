Name:           pass
Summary:        A password manager using standard Unix tools
Version:        1.6.5
Release:        1%{?dist}
License:        GPLv2+
Url:            http://zx2c4.com/projects/password-store/
BuildArch:      noarch
Source:         http://git.zx2c4.com/password-store/snapshot/password-store-%{version}.tar.xz

BuildRequires:       git
BuildRequires:       gnupg2
BuildRequires:       pwgen
BuildRequires:       tree >= 1.7.0
Requires:            xclip
Requires:            git
Requires:            gnupg2
Requires:            pwgen
Requires:            tree >= 1.7.0

%description
Stores, retrieves, generates, and synchronizes passwords securely using gpg,
pwgen, and git.

%prep
%setup -q -n password-store-%{version}
rm -f contrib/emacs/.gitignore

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} \
     BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir} \
     MANDIR=%{_mandir} FORCE_ALL=1 \
     install

%check
make test

%files
%doc README COPYING contrib
%{_bindir}/pass
%{_datadir}/bash-completion/completions/pass
%{_datadir}/fish/vendor_completions.d/pass.fish
%{_datadir}/zsh/site-functions/_pass
%doc %{_mandir}/man1/*

%changelog
* Wed Jan 28 2015 Christophe Fergeau <cfergeau@redhat.com> 1.6.5-1
- Update to pass 1.6.5

* Thu Dec 04 2014 Christophe Fergeau <cfergeau@redhat.com> 1.6.3-1
- Update to pass 1.6.3

* Sat Jun 07 2014 Christophe Fergeau <cfergeau@redhat.com> 1.6.2-1
- Update to pass 1.6.2

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Christophe Fergeau <cfergeau@redhat.com> 1.6.1-2
- Make sure tree 1.7 is present
- Run test suite when building package
- Various small spec cleanups

* Fri Apr 25 2014 Christophe Fergeau <cfergeau@redhat.com> 1.6.1-1
- Update to 1.6.1

* Wed Apr 23 2014 Christophe Fergeau <cfergeau@redhat.com> 1.5-2
- Fix location of bash completion files

* Thu Apr 17 2014 Christophe Fergeau <cfergeau@redhat.com> - 1.5-1
- Update to 1.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 30 2012 Christophe Fergeau <cfergeau@redhat.com> - 1.4.1-1
- Update to 1.4.1
- Fix gnupg dependency (pass needs gnupg2)

* Mon Sep 24 2012 Christophe Fergeau <cfergeau@redhat.com> - 1.4-1
- Update to 1.4

* Tue Sep 11 2012 Christophe Fergeau <cfergeau@redhat.com> - 1.2.0-1
- Update to 1.2 release

* Thu Sep 06 2012 Christophe Fergeau <cfergeau@redhat.com> - 1.1.4-1
- Initial import

