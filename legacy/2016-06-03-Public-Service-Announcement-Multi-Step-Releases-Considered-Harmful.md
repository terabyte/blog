# Public Service Announcement: Multi-Step Releases Considered Harmful
## May 3rd, 2016

Our industry has understood for [going on 16 years now](http://www.joelonsoftware.com/articles/fog0000000043.html)
that the ability to perform a build in a single step is a critical
metric for judging a software organization's process quality, ranking right up
there with "you use source control, right?"  I'm going to argue that **all**
release engineering process should follow this rule as well.  This includes
releasing, branching, hotfixing, etc.  It is massive failure of engineering
pattern-recognition that this is not recognized across our industry and just as
common as it is for builds.  While there exist many companies that do perform
releases and branches in a single, simple step - many many more do not, even
those that understand the value of simple single-step builds.  For builds, Many
consider this result to be self-evident, but it will be valuable to rehash the
discussion for the sake of the parallels it exposes.

Builds are things that should happen "early and often".  The more you build, the
more you find problems early, which itself is an important good which I've
discussed [in-depth in the past](2016-01-27-Better-Debugging-Through-Socratic-Method.md).
Things which are good should be easy and incentivized.  A process
that is annoying, difficult, long, or complex is not incentivized.  Therefore, a
build should be a single step.  That is just one consequence of this thinking,
however.  A build should also be easy and fast.  You should be able to run it on
your local machine, preferrably.  It should be
[reliable](2016-01-28-The-Importance-of-Build-Reliability.md), or developers
will not keep it reliable or find value in running it.  All of these
aspects come from the observation that builds are a thing that ought to be
incentivized.  All of these things are true of release engineering processes as
well.

A developer should be able to produce a hotfix locally, trivially, and in a
single step, so they can test a critical fix.  A developer should be able to
produce a branch in a single step, so they can experiment with long-lived
changes that cannot go into trunk development yet.  A developer should be able
to produce a release - exactly like an official one - to reproduce problems in
production exactly, or verify a fix.  Also, continuous release is becoming "the
new hotness", and for this very reason.  A developer should be able to do all
of these things on a whim, to detect problems with the process early.  Does the
branching process even still work given all the development that has happened
since the last branch?  Five minutes before the release is scheduled to happen
is just about the worst time to find out.

So what happens when we now consider massive-scale software - software with 30
different components, each of which has 100+ dependencies in its dependency tree
- spread across many different repositories, controlled by different entities?
One must engineer around this problem.  A build framework is needed that can
understand dependencies and stitch together disparate repositories into a single
unified snapshot of known-good revisions.  This tool should store its metadata
in a way that you can create a "branch across packages" (Amazon would call this
a "versionset") in a single step.  This tool should be able to build the entire
build tree in a single reliable step (no guarantees it'll be fast, but if your
tool is good, it will support parallelism and incremental builds and only build
that which has changed).  Notice that [QBT Build Tool](https://qbtbuildtool.com)
is an excellent candidate for this - that is by design.

There is a potentially-low-hanging fruit available to a huge fraction of the
software engineering shops out there - make your releases and branching
processes easy, and a single step.  Make them run locally.  Don't couple them to
a jenkins job that runs code that exists nowhere in source control, that someone
needs to run on a dedicated slave that has special credentails, whose
entrypoints are archaic parameters only documented in some wiki somewhere.  If
you can't replicate it, it isn't automated.  If you can't do it locally, it
isn't transparent or easy to understand.  If the "how to create a branch" wiki
page is longer than "run this command", or "run this jenkins job", that's an
anti-pattern.  If the codebase is massive, and this fruit is not "low-hanging",
maybe there are other priorities, but this is something that should eventually
be done.  The best time to plant a tree is 20 years ago, but the second best
time to plant a tree is right now.
