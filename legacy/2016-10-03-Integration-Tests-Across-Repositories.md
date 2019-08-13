# Integration Tests Across Repositories
## October 3rd, 2016

It is well understood that in the world of software development, coding without tests is like tightrope
walking without a net.  In enterprise, where software reaches massive scale and is generally
composed of many discrete modules linked together in a top-level application, it is standard to have
not only component-level unit tests, but also integration tests.  For my purposes, when I say "unit
tests" I mean tests which run very quickly, and test local functionality.  When I say "integration
tests", I mean tests which may take longer to run, but most importantly, which test functionality
across different components (i.e. test that two or more components are able to function correctly
together).

The problem is, in many enterprises, these tests require coordination across different teams or
business units responsible for those different components, making integration tests both
technologically and organizationally challenging to maintain, monitor, and fix.  In the open source
world, the challenge is even greater because the different components may have no link whatsoever
(besides both being used by the same top-level application).  With no hierarchy, management chain,
or lever to pull, who is responsible for these integration tests?

We can improve this situation in both enterprise and open source worlds by using a repository
stitcher and dependency manager to perform our builds and tests.  Tests, just like builds, must be
reproducible and deterministic.  In order to accomplish this, there must be stable versions.  If
each time your tests run they potentially pull in different versions of the components under test,
they are worthless.  However, if you use static versions like most dependency managers do (ivy, maven,
etc) then it is difficult to test new changes, or notice when things break.  The solution is to
stitch together disparate repositories into a "virtual repo" that includes all version information.

The simplest implementation of this would be git submodules.  A single parent repository could
include a git submodule for each needed repository.  Then tests and builds could check out the
parent repository, do a submodule update to fetch all the submodules at their static versions, and
run the builds and tests.  A particular sha1 of the parent repository exactly specifies all versions
of the sattelite repositories, making it completely deterministic and reproducible.  To pick up new
versions, you could automatically detect changes in the sattelite repositories and update the
submodules.  You might then only merge in those changes if the build and tests succeed.  In this
way, you can maintain a consistent set of versions known to work.  Should the new changes ever fail,
the old working versions would be kept and an alert can be sent out to someone to remedy the
situation.

So, what do we do to improve on this situation?  Well, first off, git submodules are terrible to
work with.  Developers would need to commit in the sattelites, push those changes, then make a
second commit in the parent repository to update them - this means every change requires at least
two commits.  Another problem is, what if a "coordinated change" needs to be made to multiple
components at once?  That is, what if a change impacts two components and only works if both are the
old version, or both are the new version?  It seems dangerous to push the two sattelite commits to
their repositories and "hope they both get picked up" - a developer would like to have more control
over the process.  Additionally, the history is very difficult to read.  The diffs in the main
repository are just sha1s of submodules changing from one hash to another.  But in the sattelite
repositories, you can only see the diffs of single modules at a time.  Coordinated changes will be
difficult to match up and review.  Finally, there is a problem here in that the authority is
uncertain.  Which is the <i>real</i> version of some component?  The one in the sattelite
repository, or the one in the parent repo?  Nothing stops people from pushing further changes while
the sattelite repository has a broken change in it, which would cause the parent repo to fall
farther and farther behind, making the fix harder and harder.

What to do?  The answer is to go one step farther.  What we need is a "meta git" - a build tool
which is SCM-aware and can both stitch multiple repositories together - <b>and also</b> understand
the dependencies between repositories and the coordinates changes that happen to them.  One such
tool is [QBT Build Tool](https://qbtbuildtool.com).  The way this works is, instead of
git submodules, the parent repository has a metadata file (QBT uses a simple JSON format, could be
anything though) which explicitly lists repositories, sha1 versions of said repositories, and also
tracks packages within those repositories, and the dependencies between those packages.  This
metadata, or qbt manifest, includes **every** package in the graph, which should include every
top-level target you are interested in.  This means the entire dependency graph can be calculated
from this metadata.  Additionally, each package that is built has a Cumulative Version (CV), which
is determined by the tree hash of the package directory, plus the CVs of every dependent package,
all hashed together.  In this way, the CV is a "content hash" for a package just like a git sha1 is
for a commit.  The system can now easily determine what needs to be rebuilt / retested, because any
top-level whose dependencies or tree has changed will have a changed CV - no graph traversal needed.
The system can also automatically make commits in the sattelite repositories and update the metadata
in the parent repository in a single step, and that change can be dealt with atomically.  The tool
can also display diffs by calling git diff in each sattelite repository that has changed, since it
understands the format of the metadata.

Finally, and most importantly, the authority is with this metadata.  The branches in a sattelite
repository can be completely ignored.  QBT achieves this by pushing "pins", which means hidden
branches (in the namespace refs/qbt-pins/X where X is a commit sha1).  Pins are world-writable but
immutable - there are technical reasons for this - but it means that all that matters is that the
sha1s present in the manifest are also present in pins, and no pin will ever be lost.  When a
manifest is examined, the exact sha1s are pulled straight from the pins, no other branches are
consulted.  This means the manifest is the authority, regardless of whether or not we control the
sattelite repositories.  When a branch in a sattelite repository updates, the manifest can be
updated as well, or an automatic process can track that branch (we call this an "auto-bumper"), but
if the resultant builds or tests fail, we won't accept that change.  In this way, a manifest is like
a "branch across repositories".  This is superior to how other repository stitchers work (such as
android's repo tool).

An inevitable result of this - one which is particularly bad with submodules, is that two developers
could make unrelated changes in the submodule.  In the parent repository, this is seen as a sha1
changing from A to B on the left side, and from A to C on the right side.  Should this happen, a
developer must manually check out the sattelite repository, merge B and C to create D, then manually
set that as the resolution to the conflict.  Tools like QBT can (and QBT already does) implement a
special custom merger which automatically handles this situation.  Even if there are multiple
conflicts in multiple repositories, QBT will automatically check out the sattelites and merge their
commits, dropping to a shell for manual resolution if neccessary, then create a proper merge commit
in the parent repository.  This is incredibly powerful.

So what would it look like, if enterprises and the open source world adopted this system?  Companies
dedicated to open source, like Google and Cloudera, could vend a manifest including their projects
and other third-party dependencies all at revisions known to build and pass tests.  Other companies
and open source projects could build their software on this "set of working versions", and never
have to worry that some library they need might not be compatible with some other library they need.
Furthermore, open source organizations like the Apache Software Foundation could vend manifests for
similar purposes.  Huge API rewrites, like the httpclient disaster (a popular java library used to
talk http protocol) would become much easier because people would either take a manifest from before
the rewrite (and get all the libraries using the old API) or after the rewrite (and get all the
libraries using the new API), and know confidently that all code compiles and tests pass.
Backporting changes between these two "manifest branches" would be much easier because you have not
only the history of the httpclient module, but all the other modules around it and can easily see
what changes were needed to accomodate the new API.

What if you needed libraries from two different manifests (say, Guava from Google and httpclient
from ASF).  You can simply merge the manifests together, to create a single manifest that contains
both!  The package namespace is global, so as long as packages are named carefully this will do
exactly what you might hope (or, at least, the best you possibly **could** hope).  If your source
manifests are disjoint, you wind up with a manifest that contains everything in all source
manifests, and is guaranteed to still build and pass tests (if all the parents built and passed
tests).  If any packages do overlap, for each of those, they will be merged.  If the differences are
non-trivial and conflict, you will be dropped to a shell where you might accept "ours" or "theirs",
or manually set it to some other version (or even fork the package, adjusting one side to use your
fork of the package, in a case of severe emergency).  Once you have produced a working manifest with
all your dependencies, you can develop your software in confidence, and vend your own manifest to
others (who can then easily see the history of how you produced your set of working third-party
versions, as well as your first party software).

In this way, companies like Cloudera, which vends CDH (the Cloudera Distribution of Hadoop) would
now have a powerful tool through which they can maintain their distribution - which is basically
just a set of versions of many open source packages which they have tested and guaranteed to work
together.  Using this system internally would probably make their lives much easier and free up
resources to focus on feature development and other tasks.

====

