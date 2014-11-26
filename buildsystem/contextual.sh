#!/bin/bash
set +e

# this script is not as flexible as intremental.py, but it allows you to build a branch for $DISTS on x86_64, which is 99% of what we care about.
DISTS="el5 el6 el7"
MOCKCONF="buildsystem/mock"
MOCKOUT="/var/lib/mock"

# within the context of a tree, perform a build of only the files that have changed between master and that tree.
me=${BUILD_TAG}

rpmrepo="${HOME}/rpm-repos/verify_builds/${me}"

# get objects that are different between master and ourselves - since we should only be running against a commit, we're not worrying about untracked files.
output=$(git diff --name-only master)

specs2build=$(echo "${output}" | grep '^SPECS/' | grep '.spec$' )

if [ -n "${specs2build}" ] ; then
  # okay, we actually have something worth doing, let's get to it.
  declare -A spec2srpm # we need this to hold the spec->srpm mappings
  echo "CLEAN: recreating output directory ${rpmrepo}"
  rm -rf "${rpmrepo}"
  mkdir -p "${rpmrepo}/SRPMS"
  echo "running builds for ${me} against the following specs: "
  echo "${specs2build}"

  # SRPMS
  for spec in ${specs2build} ; do
    rpmspec_out=$(./buildsystem/mksrpm.py "${spec}")
    # this is...evil, but works Well Enough
    rpmspec_out=$(echo "${rpmspec_out}" | sed -e 's/{//' -e 's/}//' -e "s/'//g")
    specname=$(echo "${rpmspec_out}" | awk -F: '{ print $1 }')
    srpmname=$(echo "${rpmspec_out}" | awk -F: '{ print $2 }')
    spec2srpm[${specname}]="${srpmname}"
  done

  # move the SRPMS now, since that allows the job to explode later and we still get things to poke at.
  mv SRPMS/* "${rpmrepo}/SRPMS"

  # okay this one gets a little weirder - all the SRPMS are now moved, and we have a list of SPECS, but we still need to check if the supported-dists flag
  # is about.
  for spec in ${specs2build} ; do
    # get filename of srpm (we moved it!)
    specname=$(basename "${spec}")
    specname="${specname%.spec}"
    srpm=$(basename "${spec2srpm[$spec]}")
    srpm="${rpmrepo}/SRPMS/${srpm}"

    # loop over dists we could build and see...
    for dist in ${DISTS} ; do
      buildit=1 # assume we're going to do the build
      if [ -f "${spec}.supported-dists" ] ; then
        grep -q "${dist}" "${spec}.supported-dists"
        if [ ${?} -ne 0 ] ; then
          buildit=0	# you will not be building today
        fi
      fi

      if [ ${buildit} -eq 1 ] ; then
        # run mock, with our arg collection
        mock --configdir "${MOCKCONF}" -r arrjay-${dist##el}-x86_64 -D "dist .${dist}" --rebuild "${srpm}"
        # create holding directory if nonexistent
        if [ ! -d "${dist}/${specname}" ] ; then
          mkdir -p "${dist}/${specname}"
        fi
        mv "${MOCKOUT}/arrjay-${dist##el}-x86_64/result/"* "${dist}/${specname}"
      fi
    done
  done

  # pile any resulting dist dirs in the rpmrepo
  for dist in ${DISTS} ; do
    if [ -d "${dist}" ] ; then
      mv "${dist}" "${rpmrepo}"
    fi
  done
fi
