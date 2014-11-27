#!/usr/bin/env python

import platform
import os
import subprocess
import shutil
import optparse
import errno

# we don't bother importing python rpm bindings, as we're interacting with
# rpmbuild, which the bindings don't support.

parser = optparse.OptionParser()
parser.add_option("-u", "--unsigned",
                  action="store_false", dest="sign_rpms", default=True,
                  help="skip RPM signing")

(options, args) = parser.parse_args()

# tuneables
# mock chroot base to use
mockroot = 'arrjay'

# distributions to build for
dists = ['el5', 'el6', 'el7']

# map dist tags back to mock sub-component
mockmap = {'el6': '6', 'el5': '5', 'el7': '7'}

# architectures to build for given a particular cpu
#defarchs = {'x86_64' : ['x86_64', 'i386']}
defarchs = {'x86_64': ['x86_64', 'i386']}

# architectures targetable via linux32 on a 64-bit system.
linux32_archs = ['i386']

# directory full of binaries
outputdir = os.environ.get('HOME')+'/rpm-repos'

# directory where mock runs
mockdir = '/var/lib/mock'

# directory for mock configs
mockcfgs = 'buildsystem/mock'

# directory for rpm macros
rpmmacrodir = 'buildsystem/rpmmacros/'

# basic rpm macro path (we don't want user or system configs!)
base_rpmmacropath = '/usr/lib/rpm/macros:/usr/lib/rpm/macros.d/macros.*:/usr/lib/rpm/platform/%{_target}/macros:/usr/lib/rpm/fileattrs/*.attr:'

# do we have a SPECS directory?
if not os.path.isdir('SPECS'):
    raise Exception('There is no SPECS directory')

# do we have mock configs?
if not os.path.isdir(mockcfgs):
    raise Exception('there is no mock config directory')

# do we have a default rpmrc?
if not os.path.isfile(rpmmacrodir+'default'):
    raise Exception('There is no default rpmmacros')

try:
    buildarchs = defarchs[platform.machine()]
except KeyError:
    print(platform.machine(), 'has no defined architectures')
    exit()

# reverse the mock mapping so we can use it later, too
mockrevmap = dict((v, k) for k, v in mockmap.iteritems())

# wrench open the null device
NUL = open(os.devnull, 'w')

# holder for rpm binary outputs
# for a given binary, what spec would buld it? what mock chroot does it
# live in? what is the dist tag? what is the arch?
bin2spec = {}
ven2bin = {}
binaries = set()  # all the buildable binaries possible
vendorpkgs = set() # all the pre-built vendor RPMs we deem to sign.
tobuild = set()  # missing binaries
topkg = set() # missing vendor binaries
buildspecs = set()  # the collection of specs needed to produce needed binaries
new_srpms = {}    # for a given spec, what SRPM is the result?
mockups = {}    # for a given chroot, what specs need to be built?
createrepos = set() # final repos that need updating

have_rpmspec = True
# see if we *have* rpmspec
try:
    subprocess.call(['rpmspec', '--quiet'])
except OSError:
    have_rpmspec = False

if have_rpmspec is False:
    # well that sucks. do I have a linux32?
    have_linux32 = True
    try:
        subprocess.call(['linux32', 'rpm', '--quiet'])
    except OSError:
        have_linux32 = False

# Preflight check - verify all specfiles are pareseable
for spec in os.listdir('SPECS'):
    if not spec.endswith('.spec'):
        continue
    if have_rpmspec:
        rpmcmds = ['rpmspec','-q','--quiet']
    else:
        rpmcmds = ['rpm','-q','--quiet','--specfile']
    rpmcmds.append('SPECS/' + spec)
    try:
        speccheck = subprocess.Popen(rpmcmds, stdout=subprocess.PIPE, stderr=NUL)
        code = speccheck.wait()
        if code != 0:
            raise Exception('parse check returned non-zero status')
    except Exception as e:
        print 'rpm spec parsing failed on ' + spec
        print str(e)
        print speccheck.stdout.read()
        raise Exception('ABORTING BUILD')

# okay, for every file in the spec directory, see if we can get the
# resulting rpm name(s)
# create the rpm repo output dirs at the same time.
for dist in dists:
    try:
        os.makedirs(outputdir + '/' + dist)
    except OSError, exc:
        if exc.errno == errno.EEXIST and os.path.isdir(outputdir + '/' + dist):
            pass
        else: raise

    # dist-specific hacks: there is no el7 i386
    if dist == 'el7':
        if 'i386' in buildarchs:
            buildarchs.remove('i386')

    for arch in buildarchs:
        try:
            os.makedirs(outputdir + '/' + dist + '/' + arch)
        except OSError, exc:
            if exc.errno == errno.EEXIST and os.path.isdir(outputdir + '/' + dist + '/' + arch):
                pass
            else: raise
        try:
            os.makedirs(outputdir + '/' + dist + '/' + arch + '-debug')
        except OSError, exc:
            if exc.errno == errno.EEXIST and os.path.isdir(outputdir + '/' + dist + '/' + arch + '-debug'):
                pass
            else: raise

        for spec in os.listdir('SPECS'):
            # not all our specs/srpms actually build on all dists. this lets us
            # specify where to build.
            if os.path.isfile('SPECS/' + spec + '.supported-dists'):
                build_dist = False  # don't build unless...
                f = open('SPECS/' + spec + '.supported-dists')
                for line in f:
                    if dist in line:
                        build_dist = True
                f.close()
                # drop to next spec if dist is unsupported.
                if not build_dist:
                    continue
            # skip any non-spec files.
            if not spec.endswith('.spec'):
                continue
            # rpmspec likes to print warnings at this point, sometimes. we
            # don't really care.
            if have_rpmspec is True:
                rpmspec_cmd = ['rpmspec', '--target=' + arch]
            else:
                # attempt to emulate rpmspec via rpm and linux32. yuck. fortunately, linux32 does work if you're already *on* linux32
                if arch in linux32_archs:
                    rpmspec_cmd = ['linux32', 'rpm', '--specfile']
                else:
                    rpmspec_cmd = ['rpm', '--specfile']
            if 'el' in dist:
                rhel = mockmap[dist]
                rpmspec_cmd.extend(['-D', 'rhel ' + rhel])
            rpmspec_cmd.extend(['-q', '-D', 'dist .' + dist, 'SPECS/' + spec])
            rpmspec = subprocess.Popen(rpmspec_cmd, stdout=subprocess.PIPE, stderr=NUL)
            code = rpmspec.wait()
            rpmpkgnames = rpmspec.stdout.read()
            for line in rpmpkgnames.splitlines():
                if not '-debuginfo-' in line:
                    # these paths are just ones I made up that work *for me*
                    mock_dist = mockmap[dist]
                    mock_tuple = mockroot + '-' + mock_dist + '-' + arch
                    bin2spec[
                        dist + '/' + arch + '/' + line + '.rpm'] = [spec, mock_tuple]

        # vendor packages are convenient to handle here, but really live in their own datastructures
        if os.path.isdir('RPMS/' + dist + '/' + arch):
            for rpm in os.listdir('RPMS/' + dist + '/' + arch):
                if not rpm.endswith('.rpm'):
                    continue
                if not os.stat('RPMS/' + dist + '/' + arch + '/' + rpm + '.reason').st_size:
                    raise Exception('attempt to shove through a binary with no explanation! aborting.')
                rpmq = subprocess.Popen(
                    ['rpm', '-pq', 'RPMS/' + dist + '/' + arch + '/' + rpm], stdout=subprocess.PIPE, stderr=NUL)
                code = rpmq.wait()
                rpmpkgname = rpmq.stdout.read().rstrip()
                ven2bin[dist + '/' + arch + '/' + rpmpkgname + '.rpm'] = 'RPMS/' + dist + '/' + arch + '/' + rpm
                mock_dist = mockmap[dist]
                createrepos.add(mockroot + '-' + mock_dist + '-' + arch)

# now, flatten bin2spec
for binary in bin2spec.keys():
    binaries.add(binary)

# flatten vendor package list as well.
for vendorbin in ven2bin.keys():
    vendorpkgs.add(vendorbin)

# splay that back out and see if packages exist. hahahaha.
tobuild.update(
    [binary for binary in binaries if not os.path.isfile(outputdir + '/' + binary)])

topkg.update(
    [binary for binary in vendorpkgs if not os.path.isfile(outputdir + '/' + binary)])

# which then turns in to specs and mock calls we need.
for binary in tobuild:
    buildspecs.add(bin2spec[binary][0])
    if not bin2spec[binary][1] in mockups:
        mockups[bin2spec[binary][1]] = set()
    mockups[bin2spec[binary][1]].add(bin2spec[binary][0])

# copy the mockup keys and vendoys to create repos that need signing/createrepo-ing
for set in mockups.keys():
    createrepos.add(set)

# if there isn't anything *to* build, that's actually an error.
if not buildspecs and not topkg:
    raise Exception('There is nothing to do')

# create build directories if nonexistent, and give an error if they *did* exist
for repo in createrepos:
    distdata = repo.split('-')
    reposub = mockrevmap[distdata[1]]
    os.makedirs(reposub + '/' + distdata[2])
    os.makedirs(reposub + '/' + distdata[2] + '-debug')

# make all the SRPMS - unsigned for mock
# rpmspec can't give you the package name, so we have to grovel the rpmbuild -bs output.
# I don't *think* you can have a spec produce multiple SRPMS, but if I'm
# wrong, you'll want to rethink your life^Wcode here.
for spec in buildspecs:
    rpmbuild = subprocess.Popen(
        # hardcoded to use default spec because this isn't a sign operation, and mock
        # can do whatever the hell it likes.
        ['rpmbuild', '-bs', '--macros', base_rpmmacropath + rpmmacrodir + 'default', 'SPECS/' + spec], stdout=subprocess.PIPE, stderr=NUL)
    code = rpmbuild.wait()
    if code != 0:
        raise Exception ('SRPM PACKAGE FAILED')
    rpm_srpmoutput = rpmbuild.stdout.read()
    for line in rpm_srpmoutput.splitlines():
        if line.startswith('Wrote: '):
            fields = line.partition(': ')
            new_srpms[spec] = fields[2]

# build all the RPMS
for mock_tuple in mockups:
    print "Building rpms for " + mock_tuple
    # if playing with the createrpo scructures you probably want to alter the
    # code here.
    distdata = mock_tuple.split('-')
    reposub = mockrevmap[distdata[1]]
    for spec in mockups[mock_tuple]:
        # mock scribbles all over stderr. let it. we'll check if any RPMs
        # showed up next.
        try:
            subprocess.check_call(
                ['/usr/bin/mock', '--configdir', mockcfgs, '-r', mock_tuple, '-D', 'dist .' + reposub, '--rebuild', new_srpms[spec]])
        except Exception as e:
            print 'MOCK FAILED (' + str(e) + ') MOCK LOGS PROCEED'
            # dump only the build and state logs to stdout so we easily see it.
            # root.log is Not That Helpful.
            for logfile in ['state.log', 'build.log']:
                f = open(mockdir + '/' + mock_tuple + '/result/' + logfile, 'r')
                text = f.read()
                print text
                f.close()
            raise Exception('MOCK FAILED')
        # if we got to here, mock should be good. snarf the rpms and stuff in
        # appropriate repos.
        for rpmfile in os.listdir(mockdir + '/' + mock_tuple + '/result/'):
            if rpmfile.endswith('.rpm'):
                # skip srpms
                if rpmfile.endswith('.src.rpm'):
                    continue
                if '-debuginfo-' in rpmfile:
                    shutil.copy2(
                        mockdir + '/' + mock_tuple + '/result/' + rpmfile, reposub + '/' + distdata[2] + '-debug/')
                else:
                    shutil.copy2(
                        mockdir + '/' + mock_tuple + '/result/' + rpmfile, reposub + '/' + distdata[2])

# handle vendor RPMS now.
for destination in vendorpkgs:
    shutil.copy2(ven2bin[destination], destination)

if options.sign_rpms:
    # if we got to this point, all the binries successfully built. so, sign
    # the srpms
    if new_srpms:
        print "Signing SRPMS"
        rpmsign = ['./buildsystem/rpmsign.exp',
            '--macros', base_rpmmacropath + rpmmacrodir + 'default',
            '--addsign']
        rpmsign.extend(new_srpms.values())
        try:
            subprocess.check_call(rpmsign)
        except:
            raise Exception('RPMSIGN FAILED')

    # now sign the RPMs per output directory. note that check_call here uses shell globbing.
    # we don't sign debuginfo (today?)
    print "Signing packages"
    rpmsign = './buildsystem/rpmsign.exp --macros '
    for repo in createrepos:
        distdata = repo.split('-')
        reposub = mockrevmap[distdata[1]]
        dist_sign = rpmsign + base_rpmmacropath + rpmmacrodir + reposub +' --addsign ' + reposub + '/' + distdata[2] + '/*.rpm'
        try:
            subprocess.check_call(dist_sign, shell=True)
        except:
            raise Exception('RPMSIGN FAILED')

# push staged binaries into repo
for repo in createrepos:
    distdata = repo.split('-')
    reposub = mockrevmap[distdata[1]]
    try:
        subprocess.check_call('cp ' + reposub + '/' + distdata[
                              2] + '/*.rpm ' + outputdir + '/' + reposub + '/' + distdata[2], shell=True)
    except Exception:
        raise Exception('REPO COPYIN FAILED')
    # handle debuginfo
    debugfiles = os.listdir(reposub + '/' + distdata[2] + '-debug')
    if debugfiles:
        try:
            subprocess.check_call('cp ' + reposub + '/' + distdata[
                                  2] + '-debug/*.rpm ' + outputdir + '/' + reposub + '/' + distdata[2] + '-debug', shell=True)
        except Exception:
            raise Exception('REPO DEBUG COPYIN FAILED')

# push staged SRPMS into repo
if new_srpms:
    srpm_cp = ['cp']
    srpm_cp.extend(new_srpms.values())
    srpm_cp.extend([outputdir + '/SRPMS'])
    try:
        subprocess.check_call(srpm_cp)
    except Exception:
        raise Exception('SRPM COPYIN FAILED')

# update binary repos
for repo in createrepos:
    distdata = repo.split('-')
    reposub = mockrevmap[distdata[1]]
    try:
        subprocess.check_call(
            ['createrepo', outputdir + '/' + reposub + '/' + distdata[2]])
    except Exception:
        raise Exception('CREATEREPO FAILED')

# update SRPM repo
if new_srpms:
    try:
        subprocess.check_call(['createrepo', outputdir + '/SRPMS'])
    except Exception:
        raise Exception('CREATEREPO FAILED')
