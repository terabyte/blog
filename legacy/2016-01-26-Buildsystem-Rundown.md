# Buildsystem Rundown
## January 26th, 2016

**Note from the editor:**  This blog post is a living document.  In it, I
will try to discuss popular (and unpopular) build tools, and their benefits and
drawbacks.  In the interest of not delaying it forever, I am posting it in this
not-yet-complete form, and will fill in more details for more build tools as I
find time to do so.

There are many specializations in the field of software engineering.  There are
those who specialize in machine learning, in computational linguistics, in
distributed systems, in reliable networks, or in massive-scale systems.  These
areas are often seen as "Sexy", "desireable", and "on the bleeding edge of
computer science".  There are some critically important fields that don't come
to mind quite so easily, however.  Devops is one that is every bit as much a
specialty as those I listed, and every bit as much important, if not moreso.
Here's another:  Build Systems.  Chances are, if you are developing software to
deliver value and solve difficult problems, you are not talking about software
simple enough that you can run `-classpath Foo.java` by hand.
How do you solve a problem in software that is too big to run by hand?  You
write code to do it, of course.  It is from this realization that Make was
born.

### GNU Make

Originally released in 1977, today many derivatives exist (such as [GNU Make](https://www.gnu.org/software/make/)).  Today, even after
almost 4 decades, a plethora of software builds using GNU Make or some other
Make variant.  The key concepts for Make are simple - you have inputs and
outputs, outputs are targets you want to build, inputs are the thing you need to
build those outputs, and the output of one process can be the input of some
other process.  This alone is complex enough to describe a "Directed, Acyclic
Graph" (DAG) of tasks and their dependencies, sort them into a topological
ordering, and then execute them, possibly in parallel.  Make can use filesystem
modification times to detect whether any inputs are "newer" than an output,
meaning the output needs to be rebuilt, or if it can skip building, allowing
incremental builds.  Yes, people were doing incremental builds 40 years ago.  No
shit.  Really.

#### The Good

* Fast
* Supports incremental builds
* Excellent support on practically every platform
* How many pieces of software do YOU use that have 4 decades of stability and bugfixes?

#### The Bad

* With so many variants floating around, whether a given Makefile will work with a given Make is anybody's guess
* Because it is so simple, it is very difficult to do more powerful things, there is no plugin system
* There is no easy way to test make code, it either works or it doesn't.
* There is no external dependency management for depending upon projects built by other tools or outside the current build
* Make does literally nothing for you, even a relatively simple build could require hundreds or thousands of lines of make

#### The Ugly

* Whitespace sensitive.  Requires hard tabs.  EWWWW!
* Have you ever seen a Makefile that actually made it clear what was happening?  Me neither.

#### Known Offenders

* The Linux Kernel and probably 99% of the GNU Userspace tools build using GNU Make
* Amazon's massive propretary, internal build system used Perl scripts to generate makefiles which actually ran the build circa 2009.  My understanding is that this is no longer true, but I have no firsthand knowledge anymore

### Apache Ant

Released in July of 2000, Ant ("Another Neat Tool") was birthed out of the need
to replace a proprietary make flavor with something "platform independent".  In
other words, a bunch of java guys saw a tool not written in Java and decided to
write a "better" version with the exact same (or worse) features, but it'll be
better because it was written in Java.  Unsuprisingly, Ant (now part of the
Apache project, and often called Apache Ant) is little more than a shitty make
rewrite in java, except replace eye-bleeding hard tabs with
even-more-eye-bleeding xml.  What would possess a person to design such a tool
in the year of our lord 2000?  If an unnamed source of mine who claimed to know
the author personally is to be believed, he was dropping a LOT of acid around 2000.
Possibly related.  I'm just sayin'.

#### The Good

* ...Written in Java?  I guess?  We'll call that good?
* Supports "modules" (sorta - it's terrible, but you basically shove jars onto ant's classpath and then you can use extended or custom tasks.  It's completely manual, and completely terrible)

#### The Bad

* No support for incremental builds - filesystem mtime stuff was untenable to do in a cross-platform compatible way
* Lazy property evaluation is not supported - in fact, properties values can only even be changed using "ant contrib" extensions
* Creating new "rules" a la Make cannot be done inline, you need to write a Java class and compile it.
* Again, like Make, there is no easy way to test xml "code", it either works or it doesn't.
* Again, like Make, there is no external dependency management for depending upon projects built by other tools or outside the current build

#### The Ugly

* XML is a travesty.  From the wikipedia page: "The complex structure (hierarchical, partly ordered, and pervasively cross-linked) of Ant documents can be a barrier to learning. The build files of large or complex projects can become unmanageably large. Good design and modularization of build files can improve readability but not necessarily reduce size."  That doesn't even begin to describe the real difficulties of using Ant for large, complex, and intertwined projects.
* If you thought Make was verbose, wait till you see Ant build files.  The simple example on wikipedia is 21 lines long to build a single jar file plus a clean target.
* You haven't known true pain until you found a "portable" ant build.xml that wouldn't work because you needed to somehow get some ant contrib jar on your build tool's classpath (which is different from your buildtime classpath, of course).
* Undefined properties **do not raise an error (!!!!!)** but instead are left alone, so you get the string "${foo.property}" instead, which is just about the only output you can be SURE is not what is intended.  Ever seen this? ```<if><equals first="${foo}" second="$${foo}"/>...```

#### Known Offenders

* Many large Java projects are built using ANT, and little else.  The original case it was written for was to build Tomcat after its open-sourcing.
* Apache Ivy - this external dependency manager can be shoved into Ant (like ant contrib, see other comments about classpath disasters) to give you Real Dependency Management (TM).  Sorta.  It also builds using Ant, of course.

### Maven

Released in July of 2004, Maven (Yiddish for "accumulator of knowledge" or
"expert") took the Java world by storm on account of its undisputed ability to
"suck less than Ant".  That said, a far more appropriate monkier would have
been Nudnik (Yiddish for "pest" or "pain in the neck").  Like Ant (and in a
move that makes no contribution whatsoever to that "sucking less than ant"
thing), Maven uses an XML format for its build files (called pom.xml).
Contrary to Make and Ant, Maven uses "convention over configuration" and
assumes everything it isn't explicitly told is some (presumably sane) default.
Despite having to say fewer things explicitly, the pom format is so insane that
even the simplest pom file is usually much larger than any build.xml would be,
though because Maven has so many more features than Ant it is difficult to make
a fair comparison.  Today, many other build tools have adopted Maven's default
layouts, so you have Maven to thank for any project that has the classic
directory layout of:

* src/
** main/
*** java/
*** resources/
** test/
*** java/
*** resources/

Also contrary to Make and Ant, Maven has a built-in dependency manager.  This
is Maven's greatest strength and a large reason why it has become the defacto
build tool for a majority of modern Java projects.  Maven may even be credited
with causing the explosion of quality, easy-to-depend-upon libraries in the
Java ecosystem which made it such a popular and productive enterprise software
stack.  Even as a self-described Maven hater, I have to admit it is likely
responsible for much of the success Java has enjoyed between 2004 and now.

#### The Good

* Because of its built-in dependency management and plugin architecture, Maven is the first popular build system where you can specify your build tool dependencies and use them, and have it "just work"
* Maven gets an extra "good" line for dependency management, because you can not only specify your dependencies but you can specify if they are "test" or "compile" or "provided" - it supports classpath separation and publishing of a strict, consistent classpath (if you use it correctly)
* Maven has excellent built-in support for interactive development environments (IDEs) such as IntelliJ and Ecilpse
* Maven can be used to build things besides Java (but is very Java-centric and still mostly only used for Java)
* Maven has first-class support of hierarchical projects in a structured way, making building very large monolithic repositories easier
* Maven has clear support workflows which makes supported things very easy, such as running tests, publishing artifacts, etc., and plugins make adding new goals easier than forking Maven (if only slightly)

#### The Bad

* Maven's error messages are TERRIBLE - It lies to you
* Again, Creating new "rules" a la Make cannot be done inline, you need to write a Maven plugin and compile it
* Again, like Make, there is no easy way to test xml "code", it either works or it doesn't

#### The Ugly

* Like Ant, Maven pom.xml files are a travesty
* If you can fathom it, properties are almost WORSE than Ant.  You cannot easily set properties dynamically from environment, they have to be passed in via command line parameters
* Newer versions of Maven have had features <b>intentionally removed</b> because "that is the wrong way to do it" or "you shouldn't be doing that in your build"
* Both Maven 2 and Maven 3 are in common use across many projects but most projects only work with one, or the other - Maven does not bootstrap itself or control the dependency on itself at all
* People have written extensively on the value of Internal Reprogrammability, frequently using Maven as the canonical example of [how to fail at it](http://nealford.com/memeagora/2013/01/22/why_everyone_eventually_hates_maven.html)

#### Known Offenders

* A vast majority of jars you will find on search.maven.org were built using maven (but not all - maven.org is a sort of artifact repository which both Maven and Ivy a la Apache Ant can use)
* Many SDKs bundle a version of Maven to build java-based plugins, such as Atlassian's Plugin SDK

### Gradle

Released in 2007, [Gradle](https://gradle.org/) is finally a build
tool that doesn't completely suck.  I mean, it did in 2007, probably, but Gradle
was created with a mission and supported by a services company and an open
source community together, it has accomplished more than any other open source
build tool in popular use.  Hans Dockter is the CEO of Gradleware, Gradle's
strongest voice of support, and a very smart guy behind the demand that we as an
industry deserve better build tools, a stance I agree with and care deeply
about.

Gradle's mission is to be a reliable, powerful, platform-agnostic tool for
building and testing projects large and small, using any language/technology
stack, with easily-extended and easily-tested build code in a domain specific
language (DSL) based on Groovy.  There is a lot to unpack there.  First off,
Gradle is "unoppinionated".  It doesn't assume anything about your build (that
it is in java or C/C++, that it has dependencies, etc).  Furthermore, because
it uses a Groovy-based DSL, the build files themselves can be very short and
incredibly descriptive.  Because Gradle allows both inline and external plugin
modules, you can write your build code inline for ease-of-use, or in a module
for easy testing.  You can write shared code which doesn't make any assumptions
(in, say, a module called "java-base"), and then an "opinionated" module called
"java".  If you include "java-base", you get the targets you can manually call
to create jars and so on.  If you include "java", you get "java-base" but also
the assumption that your source code lives in `src/main/java` and your
tests in `src/test/java` and so on, making both "configuration over
convention" and "convention over configuration" possible when appropriate.

A Gradle project to build a simple java library following the standard Maven layout looks like this:
```
apply plugin: 'java'
```
Yeah, you aren't missing anything, that's it!  That alone gives you test
targets, compile targets, publish targets, the works.  It gives you incremental
builds (doing an up-to-date check of your source files) and understands that
source and resources goes into your jar.  With a few more lines, you can pull
in dependencies from search.maven.org just like you would with Maven or Ant +
Ivy.  But wait, there's more!

Gradle, unlike any other build tool we have thus far discussed, has a
"bootstrap" step.  Using a minimal jar you check in next to your project,
gradle can download itself - and not just any version of itself, but a specific
version of itself you tell it to use - and it uses that to run the build.  In
this way, Gradle is the first build tool in common use (TODO: apologies to SBT?)
to properly bootstrap itself and control its own dependency.  A new version of
Gradle will never be released causing hundreds or thousands of projects to
break, becasue their bootstrapper will continue to fetch the known-working
version until someone tells it to upgrade.  <b>This</b> is how build tools
should work, ladies and gentleman.  The only dependency Gradle still has is on
Java itself (you need a compatible JDE around to invoke gradle, even the
bootstrapper).  Breaks can still be caused by incompatible Java versions, but
that is a much less common problem, and one which is much easier to fix.

#### The Good

* Dependency management "as good as it gets" for Maven-compatible repositories (and compatible with maven and ivy repositories)
* Because of its superior dependency management and plugin architecture, you can write build code inline or in modules, external or internal to your project, with or without tests of your build code
* The Groovy DSL is concise, expressive, and powerful - you can implement build code in it, in raw Groovy, or even in Java if you prefer
* Like Maven, Gradle supports classpath separation between test and compile targets, but unlike Maven it is even more powerful as you can create arbitrary independent classpaths / targets (i.e. an "api only" classpath, etc)
* Like Maven, Gradle has excellent built-in support for interactive development environments (IDEs) such as IntelliJ and Ecilpse
* Unlike Maven, Gradle is *actually used* to build many non-java projects, and there is a huge ecosysytem of plugins for building non-java projects - Maven says it does it, but Gradle is what people <b>actually use</b> to accomplish that
* Gradle's consistency, reproducibility, and flexibility are unmatched by any other open source tool in common use I am aware of

#### The Bad

* Groovy, the main language build.gradle files tend to be in, is a duck-typed and interpreted language so errors are often non-obvious and difficult for the compiler to report - and the groovy compiler/interpreter is pretty shitty at error reporting.
* Gradle is sloooow - because build.gradle files must be interpreted, and for lage projects, this might mean reading in and building the configuration data structures for hundreds of projects - Gradle can be very slow on startup.  This is partially mitigated by the "Gradle Daemon", which caches configuration information and avoids JVM startup time at the expense of sometimes serving stale or incorrect configuration or artifacts (up to you if that is an acceptable tradeoff or not)

#### The Ugly

* Gradle's incremental builds are not perfect, especially if you use janky plugins which were written incorrectly.  There are known bugs even with core plugins such as "java" though
* Gradle can put crazy things on your classpath, or even execute code you might prefer not to trust, simply by misspelling "apply plugin 'jaav'".  The plugins are automatically searched and downloaded from Gradle.org, and who knows what degree of validation happens before code gets posted there?

#### Known Offenders

* My understanding is that nearly everything built at Netflix is built using Gradle, including their large and generous open-source contributions - they are frequent presenters at Gradle Conferences
* Lots of Android app development happens with Gradle, there are plugins to assist with this


### TODO: GO (Google's golang)

While Gradle was still in its infancy in 2007, somewhere in the Googleplex,
pioneers of computer science were stirring.  Google engineers Robert Griesemer,
Robert Pike, and Ken Thompson (the later two of Bell Labs fame) birthed the Go
programming language, although it wouldn't be released to the world until 2009.
With it came the go build system, which has some interesting features.

Unsuprisingly similar to the Google build system, the `go get` command
fetches a modules dependencies directly and builds them "from tip" (i.e. the
newest version).  For more discussion of "the Google way" versus alternatives,
see my earlier post <a href="2016-01-20-A-Tale-of-Two-Build-Systems.html">A
Tale of Two Build Systems</a>.  The standard operating proceedure then, for
external or open source projects which need to control their dependencies, is
to fetch and check in static versions of those dependencies.  Updating then
becomes a terrible mess.  Some folks in the Go community decided this was a
problem and tried to create an alternative build tool, called godeps.

#### Known Offenders

* Google uses Go internally for many things
* Docker is a commonly used containerization tool written in Go

### TODO: Bazel.io

### QBT - QBT Build Tool

QBT began its life in December of 2014 as a very small prototype, written in
Perl by Keith Amling, an engineer at Palantir Technologies.  The tool's
original name was DBT, which stood for "Distributed Build Tool" but was really
backronymed from Keith's manager's nickname as an inside joke.  When the joke
got old, and his manager couldn't stand his IRC client going nuts every time
someone talked about DBT, the project was renamed to QBT.  Keith worked the
prototype into a fully functional self-building system written in Java before
having a few other engineers (myself included) added to the team, but he very
much played the part of the "Benevolent Dictator for Life" for this project.
Keith insisted from the begining that the tool not compromise its goals for any
reason

QBT was created to solve the very specific problem of many projects, from many
different technology stacks, needing to depend upon eachother in a way that can
be kept consistent, changed atomically, and versioned strictly.
Reproducibility and technology agnosticism were both baked in from the
begining, as well as a strong plan to eventually go open source.  Inspired
heavily by proprietary build system in use at Amazon.com, QBT was meant to be a
decentralized, zero-infrastructure feature-equivalent (though it's design for
accomplishing this was so different from Amazon's build system, the link is
barely recognizeable).

Like godeps, QBT has a "manifest" of sorts which contains the versions of every
package to be built, which is itself checked into source control and thus can
be updated "atomically".  QBT can be thought of as a build framework, a
"repository stitcher and dependency manager", as it uses the manifest to locate
packages in various repositories, stitch together the correct versions of all
of those repositories, and invoke each package's build in topological order,
providing each with its dependencies.  Unlike other build systems, not only are
the versions stored in the manifest but also the complete dependency graph,
allowing QBT to do interesting things like only check out the packages needed
to perform a certain build.

QBT does much of its magic by being coupled with the Git source control
manager.  Though written through an abstraction layer, making writing adapters
to other similar DVCS systems like mercurial possible, QBT utilizes Git for
performing many of its necessary tasks.  QBT analyzes not just the repository
revision, but the actual "tree hash" of the root directory of a package, and
combines that with the tree hashes of its complete transtiive closure of
dependenceies to calculate a "cumulative version" (CV) for each package.  If
you made a commit to a repository which didn't change a particular package,
it's CV would stay the same, therefore QBT doesn't have to rebuild it.  QBT
therefore has package-granularity incremental builds.  Furthermore, since
classpath isolation is generally done at the package level, packages are
encouraged to be small and numerous.  Adding a package is as easy as adding a
few lines to the manifest file and creating a new directory in an existing
repository, so packages are very lightweight.

Unlike most dependency managers, QBT does not assume artifacts will be
published.  Similar to `go get`, qbt must fetch the complete source
(and in fact, grabs the entire source control history for each dependent
repository) in order to build things.  With an extremely flexible configuration
(specified in Groovy), you can configure QBT to consult an artifact server, and
even publish there.  Cache hits (based on package + CV) are never rebuilt if
the artifact is already present, so in that way, QBT <b>can</b> have artifacts,
but it doesn't need to.  Because only changed packages, and other packages that
depend upon those changed packages, need to be rebuilt, even very large graphs
can be built very quickly and efficiently.

Also unique compared to many build tools, QBT can easily function in a
disconnected environment.  Inspired by Git itself, QBT has only two commands
that invoke the network - `qbt fetchPins` and `qbt pushPins`.
If you run a git fetch in your manifest repository, and a qbt fetchPins, you
can guarantee you have every repository of every package in your manifest
cached locally, and ready to build or check out any version in the complete
history of your manifest file.  Similarly, you can make commits in sattelite
repositories, and in meta, as much as you please, working on many different
branches or projects.  No network is needed until you are ready to push your
changes, which you would do by first doing a `git push` of your
manifest file followed by a `qbt pushPins` to get your satellite
versions pushed.

QBT may be a repository stitcher, and dependency manager, but it is <b>not</b>
actually a compile tool beyond that.  If you want to build java, you need to
use ant, maven, or gradle inside your package.  If you want to build C/C++, you
should invoke make, or gcc.  All QBT does is assemble your package and it's
dependencies, place them in a known location, and invoke the shell script
"qbt-make" in the root of your package.  From there, what you do is up to you,
so there are many ways to do it.  In this way, QBT is more of a framework or
toolkit with which you can produce incremental, reproducible,
strict-consistency builds.  Today, QBT builds itself using Gradle, but we could
use a different tool, or even just a shell script that invoked javac, if we
wanted to.

Finally, one of the most important things QBT can do for you that other build
systems cannot is QBT gives us a way to ensure consistency.  Because all
changes occur in the manifest file of the meta repository, we can have a
continuous build that ensures the entire manifest is always consistent.
Furthermore, if someone makes a pull request, *before* merging that pull
request in, we can perform a build of that manifest to ensure the new versions
are also consistent.  This means nobody is ever broken without knowing it.
Because there is only a single version of every dependency in the manifest, any
change someone makes is tested throughout the entire development ecosystem.

#### The Good

* Strict dependency management with atomic changes enables strong consistency guarantees when used correctly
* Tight coupling with Git allows package-granularity incremental building which is the safest incremental building available
* Technology agnosticism allows QBT to build anything from Java to C/C++ to Node.js to lua to LaTeX to copying around text configuration files or static webpages (this webpage is built using QBT)
* The "submanifest" command lets you keep a "private manifest" which is a superset of a public manifest, make changes "in private", and vend only the changes to the public repositories to certain parties (ideal for an enterprise writing proprietary software which depends upon open-source software)
* QBT automatically parallelizes your build at the package granularity and can build <b>very</b> quickly when packages are appropriately granular
* QBT includes a "third party importer" and "link checker" which can import jars from search.maven.org and even examine their bytecode to ensure their dependencies were properly specified in their pom.xmls to guarantee they will work in QBT - this is the next best thing to compiling them from source
* If using a build tool like Bazel.io, it should theoretically be possible to produce byte-for-byte reproducible artifacts.
* QBT has a "runArtifact" command which lets you compile and run your programs in a single step, making the develop/test cycle tighter
* QBT supports "dev protocols", allowing packages to "opt in" to certain protocols (such as eclipse-gen, which generates eclipse project files, help wanted writing protocols for IntelliJ and other IDEs)
* QBT versions itself internally - while you do need to get a binary version of QBT first in order to build QBT, you can always use that to build the version of QBT specified in a given manifest and use that to build the software, guaranteeing that future QBT changes do not break you until you merge them into your manifest
* QBT supports mechanisms for versioning external tools as well (such as JDKs, which are too large and platform-specific to include as a regular package in your manifest).  These external dependencies impact CVs correctly and don't interfere with reproducibiltiy or dependency management

#### The Bad

* QBT has only been well-tested on Linux so far
* QBT is still immature and not widely used
* QBT does not yet have a good answer for "realms" (how will different organizations vend manifests to eachother?)


#### The Ugly

* Not unlike Git, QBT has a steep learning curve and can be very difficult to use correctly, especially at first

#### Known Offenders

* www.cmyers.org is built using QBT
* QBT builds itself
* A large set of useful java libraries called "misc1" were developed for use by QBT and are available via QBT - Libraries include argument parsing, concurrent programming, and immutable data structures and struct libraries of immensely high quality

There is a lot more to write about QBT, but hopefully this quick look at QBT and many other build systems will put into context what QBT can and cannot do for you.

### Sir Not Appearing in this Blog
Honorable mentions (and possible future targets) include:

* SBT
* npm
* Grunt
* Rake
* Pants


====

