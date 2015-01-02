# $Id: geteltorito.spec 7981 2009-11-03 03:05:34Z dag $
# Authority: dag
# Upstream: R. Krienke <krienke@uni-koblenz.de>


Summary: Tool to extract boot image from an ISO file
Name: geteltorito
Version: 0.5
Release: 1%{?dist}
License: GPL
Group: Applications/File
URL: http://userpages.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/

Source0: http://userpages.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/geteltorito.pl
Source1: http://userpages.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/README
Source2: http://userpages.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/gpl.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Buildarch: noarch
BuildRequires: perl
Requires: perl

%description
geteltorito will extract the initial/default boot image from a CD if existant.
It will not extract any of other possibly existing bootimages that are allowed
by the El Torito standard. The imagedata are written to STDOUT all other
information is written to STDERR (eg type and size of image).

If you want to write the image to a file instead of STDOUT you can
specify the filename wanted on the commandline using option -o <filename>

%prep
%setup -cT
%{__cp} -v %{SOURCE0} geteltorito
%{__cp} -v %{SOURCE1} %{SOURCE2} .

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 geteltorito %{buildroot}%{_bindir}/geteltorito

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc gpl.txt README
%{_bindir}/geteltorito

%changelog
* Fri Jan  2 2015 RJ Bergeron <rpm@arrjay.bnet> - 0.5-1
- update upstream

* Fri May 22 2009 Dag Wieers <dag@wieers.com> - 0.4-1 - 7981/dag
- Initial package. (using DAR)
