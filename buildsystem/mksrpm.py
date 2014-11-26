#!/usr/bin/env python

import os
import subprocess
import argparse

# we don't bother importing python rpm bindings, as we're interacting with
# rpmbuild, which the bindings don't support.

# tuneables
# directory for rpm macros
rpmmacrodir = 'buildsystem/rpmmacros/'

# basic rpm macro path (we don't want user or system configs!)
base_rpmmacropath = '/usr/lib/rpm/macros:/usr/lib/rpm/macros.d/macros.*:/usr/lib/rpm/platform/%{_target}/macros:/usr/lib/rpm/fileattrs/*.attr:'

parser = argparse.ArgumentParser()
parser.add_argument('specfiles', metavar='SPECFILE', type=str, nargs='*')
args = parser.parse_args()

# do we have a SPECS directory?
if not os.path.isdir('SPECS'):
    raise Exception('There is no SPECS directory')

# do we have a default rpmrc?
if not os.path.isfile(rpmmacrodir+'default'):
    raise Exception('There is no default rpmmacros')

# wrench open the null device
NUL = open(os.devnull, 'w')

new_srpms = {}    # for a given spec, what SRPM is the result?

# make an unsigned RPM for the name requested on the command line
# rpmspec can't give you the package name, so we have to grovel the rpmbuild -bs output.
# I don't *think* you can have a spec produce multiple SRPMS, but if I'm
# wrong, you'll want to rethink your life^Wcode here.
for spec in args.specfiles:
    rpmbuild = subprocess.Popen(
        # hardcoded to use default spec because this isn't a sign operation, and mock
        # can do whatever the hell it likes.
        ['rpmbuild', '-bs', '--macros', base_rpmmacropath + ':' + rpmmacrodir + 'default', spec], stdout=subprocess.PIPE, stderr=NUL)
    code = rpmbuild.wait()
    if code != 0:
        raise Exception ('SRPM PACKAGE FAILED')
    rpm_srpmoutput = rpmbuild.stdout.read()
    for line in rpm_srpmoutput.splitlines():
        if line.startswith('Wrote: '):
            fields = line.partition(': ')
            new_srpms[spec] = fields[2]

print new_srpms
