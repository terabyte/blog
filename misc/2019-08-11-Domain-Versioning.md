# Domain Versioning
## August 11th, 2019

There are a lot of broken things about how most of us build software, but few things are as broken as how we use and abuse version numbers.  What is a version number supposed to tell you, exactly?  A version has many jobs:

* **Uniquely** identify a specific version of the software
* Communicate certain properties of this version of the software (dev build? alpha? production? hotfix? fork? terrifying release ending in '.0'?)
* Communicate how much has changed since some other version of the software (1.0 versus 1.1 versus 3.4?  Semantic Versioning?)
* Bidirectionally link a release or artifact of a build with the exact inputs from source control

Unfortunately, these items are in conflict with each other and achieving all at the same time is very challenging.

One way to ensure your version numbers are unique is to literally make them
a commit name (in git, a sha1, or in projects built from a combination of
multiple repositories, you could hash the metadata which includes the hashes of
all input and use that identifier).  Unfortunately, comparing two hashes
generated in such fashion gives you zero useful information about how much has
changed between them.  Additionally, irreversibility, which is pretty much the
main thing hashes do, makes the relationship unidirectional, rather than our
desired bidirectionality.

A tempting alternative might seem to be a tag, but tags in git are a global
namespace and not to be trifled with, so let's not go there.  In fact, any
human-generated name with a hope of giving you the information from bullet 2 or
3 above leads unavoidably to lookups, whether it is a lookup of tags in the git
repo, or a lookup of versions in some version database maintained for the
software building infrastructure, which is undesirable.

Consider also a common pattern - we typically achieve bullet two and three by
committing that version number into source control.  After all, how else are we
going to get it into our build and release process?  This is incredibly dumb
and responsible for a huge portion of the pain and suffering endured by release
engineers the world over.  First of all, if the source knows what version it
is, then if you have two different branches which are for two different product
lines, you can't ever merge them without making a "lying merge" where you
manually edit out one of the changes (the one that changed the version number).
This is the biggest reason people end up using cherry-pick workflows instead of
merge workflows, which is yet **another** source of pain all by itself and
which I should address in a future blog post.

It is generally acknowledged to be a desirable trait for your software to be
releasable at **any** time.  In fact, any build you might make ought to be
releasable via a simple, constant-time process which does not modify the
source or artifacts. However, if that is to happen, how do you assign those
artifacts release version without a rebuild?  The answer is, you can't.  People
who actually live by this rule do not check in version numbers as most people
understand them.  Let's not even get into the shitshow that is maven versions
and running maven commands that go insert themselves forcibly into your pom
files and update all their version numbers every time you branch or release, or
even worse, *people who do the same things with a terrible sed script or
something*.  If you've got a variable in your java somewhere that looks like
`anyco_product_version_6_0_x = "6.0.4"`, you have my deepest sympathies.

So we are starting to see some desirable traits surface for version strings:

* Must not be part of the source
* Must include the name of the commit
* Must be human-comparable in some way
* Must be able to communicate other properties

# The Answer: Domain Versions

Considering these issues, my colleagues and I have come up with what we feel is a pretty good solution, which I call Domain Versions.  Domain versions come in the form `domain-X-gY` where X is the total count of commits history, and Y is the name of the git commit, normally truncated to some sensible length like 12 or 16 characters.  The "domain" part can be anything you want, but is preferrably a name or version string looking thing.  You could even use semantic versions if you wanted, e.g. `1.0.5-X-gY`.  The domain part should be inserted into your build/release process somehow (checked into a *different* repo where your release code lives, for example, or made a variable of your release job you run, or communicated some other way).  Domain versions have the following benefits:

* You can actually type then directly into git commands - for example, `git checkout -b temp domain-X-gY`.  Try it!  Git sees that it is in the format of a git describe string, so it dutifully ignores everything except the 'Y' part and tries to check that out.
* You can easily generate it in a repo with no databases, lookups, or other information
* changing the **domain** doesn't actually change anything else about the version, so you can pretty safely take a version in an artifact like 'pre-release-1234-gSHA1' and just rename it to '1.0-GA-1234-gSHA1', and because the sha1 in there is extremely unique, a find-and-replace is quite safe.  Of course, ideally, the string appears 1 or 0 times in the entire artifact, so it is just a matter of renaming the file and maybe updating a single instance (like version.txt) which the application can read in order to put the right string into an about box or something.
* You still have the flexibility to use semver with your domain string if your requirements demand it (i.e. 1.0.1, 1.0.2, 1.1.0, etc).
* You never have commits bumping version strings creating merge conflicts between branches

====

Title: Domain Versioning
Date: 2019-08-11
Tags:  build systems, domain versioning, programming, tools, dependency management, maven
