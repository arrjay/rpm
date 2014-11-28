%global git_checkout 50944f0d
Name:		duc
Version:	0
Release:	2%{?dist}.20141127git%{git_checkout}

Summary:	disk usage calculator

Group:		Applications/File
License:	GPLv2
URL:		https://github.com/zevv/duc
# git archive --prefix=duc-0.0.50944f0d/ -o ~/src/rpm/SOURCES/duc/duc.tgz 50944f0d
Source0:	duc.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, automake, libtool
BuildRequires:	pango-devel cairo-devel tokyocabinet-devel

%description
Duc is a small library and a collection of tools for inspecting and visualizing
disk usage.

Duc maintains a database of accumulated sizes of directories of your file
system, and allows you to query this database with some tools, or create fancy
graphs showing you where your bytes are.

%package debug
Group:		Applications/File
Summary:	%{summary} - debugging binary

%description debug
This package contains an upstream-provided binary to assist in duc usage.

%package devel
Group:		Applications/File
Summary:	%{summary} - development files

%description devel
This package contains libraries and headers for developing against duc.

%prep
%setup -n %{name}-%{version}.0.%{git_checkout}

%build
autoreconf --install
%configure
make

%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/duc
%{_libdir}/libduc*.so*

%files debug
%{_bindir}/duc.debug

%files devel
%{_libdir}/libduc*.la
%{_libdir}/libduc*.a

%changelog
* Thu Nov 27 2014 RJ Bergeron <rpm@arrjay.net> - 0-2.20141127git50944f0d
- fix split of devel and main package, write a changelog

* Thu Nov 27 2014 RJ Bergeron <rpm@arrjay.net> - 0-1.20141127git50944f0d
- initial packaging
* Thu Nov 27 2014 RJ Bergeron <rpm@arrjay.net> - 0.1.20141127git50944f0d
- initial packaging
