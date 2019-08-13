# A Tale of Two Build Systems
## January 20, 2016

Company culture is a tricky thing.  Everyone has an opinion about it, and
companies spend millions, sometimes billions of dollars trying to reinforce
their culture because they believe it can be the difference between success and
failure.  In few places is culture considered as important as it is in software
engineering.  The sort of collaboration necesasry by individuals working on
teams and teams working together to produce massive scale software is impacted
greatly by culture.  I've been thinking about how this relates to internal
tools for a long time and I've come to believe that tools are an important and
often-overlooked contributor to developer culture at a software company.

When I think about tools and build culture, I divide companies into two groups,
"the Google way" and "the Amazon way".  I'm not saying either way is better
than the other (though I prefer the Amazon way), they are just different.
Also, of course, these are not binary but rather fall on a spectrum.  What I
mean by "the Google way" is "everyone has to use the same tools" and "everyone
builds everything from tip all the time".  Team A makes a new version, and the
next time team B builds something that depends upon that project they get Team
A's new changes - whether they want to or not.  Whether it works or not.  They
immediately know if there is a problem - and if things break, they fix it.
Because someone said so.  Because you have to.  Because process.

On the other hand, you have "the Amazon way".  There is a huge shared
development ecosystem.  People may or may not be "required" to use it, but they
sorta defacto are required to use it because depending upon anything anyone
else in the company built using that ecosystem is practically impossible unless
you completely buy into it yourself.  More importantly, that development
ecosystem has complex, expressive, powerful, and strictly enforced dependency
management.  Your software builds on fixed versions.  This means that if Team A
makes a change, and Team B depends upon Team A's software project, and that
change would break Team A, the build system tells them so, and prevents them
from breaking.  Maybe the impetus falls on Team B to "eventually upgrade to the
newest code and fix the break", or maybe Team A is responsible for driving the
deprecation of old versions of their software within the company.  But neither
team is **blocked** and neither team is **broken**.  Never ever.  Being
blocked or broken is simply unacceptable and the build system goes to extreme
lengths to ensure that nobody is ever blocked - not really - they always have
the information to know what their change breaks, and the power to fix it or
work around it.  Whether that's a good idea or not.  Because tools give you
power.  And with great power, comes great complexity.  I mean, responsibility
too, but mostly complexity.  [Uncle Ben got it half right](http://en.wikipedia.org/wiki/Uncle_Ben#.22With_great_power_comes_great_responsibility.22)

I've witnessed people argue fervently for both sides of this spectrum, often
relying upon the best argument for any such system: "It's the worst way to do
it except every other way".  But what I actually think should determine which
way a company goes is the company structure and culture itself.  Does your
company value independence, ownership, and pushing decision making as low in
the (possibly barely existent) hierarchy as possible?  Then you want "the
Amazon way".  Does your company value high-level decision making by the folks
that have the most data?  Are team interactions metered via a comprehensive
hierarchy?  Are tools simple and bureaucracy thick?  Are "we all adults here"
and "we're all on the same team" and "if something breaks, we all just fix it
because we aren't goddamned clowns"?  Then you probably want "the Google way".

Again, while I am obviously biased, I've never worked for Google (or any
similarly large company that does it "the Google way"), so take that part with
a grain of salt for sure.  I have seen many projects and smaller companies try
to do it "the Google way" and suffer greatly for it, because their culture was
not a match for that method.  When other teams make changes and break you, and
you have no recourse, no way to fix it, literally no remedy other than filing a
support ticket against that team and begging "please, please, please unbreak
us, we are slipping our release by another week!", that is bad times for
everyone.

Another reason why I personally prefer "the Amazon way", however, is that it is
also the (ideal) open source way.  There *is* no hierarchy in Open Source -
projects do own their own software, and depend upon each other, and have to work
together somehow.  That necessitates not always building everything using the
same version of every library.  But it also creates the very complex problem of
diamond dependencies, compatibility, and consistency, which are still unsolved
outside the walls of enterprise (and very few apart from Amazon have solved it
inside those walls, either).  Generally, open source projects either lock their
dependencies in to specific versions, periodically try to bump those versions,
and suffer when they break (at a time of their choosing).  Or - they don't - and
in so doing they choose to suffer constantly instead (but at least they learn of
breaks more quickly).

So, my description still sounds like a lot of suffering - why is that?  The
reason is there is no open source build system which can enforce strict
dependency management across projects.  What Amazon has, they built themselves,
and unfortunately they did it in a way they couldn't share even if they wanted
to (because it depends upon a huge amount of infrastructure).  When there IS no
unified system, or hierarchy, how can you ever prevent your dependencies from
breaking you?  The best you can do is set up a continuous build of their newest
release to send you (and them) a nicely worded email if (when) they ever break
you.

Can we do any better?  Well, maybe.  It looks to me like the Go development
ecosystem is very close to "the Google way" (unsurprisingly, since Go was
basically birthed whole cloth from the Google womb).  When you build Go
software it finds (via heuristics) all of the libraries' source itself and
builds their newest versions.  Some have tried to invent "the Amazon way" in Go
using a dependency manager called [godep](https://github.com/tools/godep), but like most solutions it
solves the problem for a specific project, but not the larger ecosystem.  Two
projects using two different sets of dependencies via godep might never be able
to depend upon each other successfully.  Still, the way godep works is
brilliant and probably the best I've seen in open source before
[QBT](https://qbtbuildtool.com).  That, however, is an announcement for another
blog post.

At the end of the day, all companies have the same goals.  They want to create
value and solve problems.  They do this by attracting the best talent and
keeping them happy.  They want their engineers to be productive and produce
high-quality software that delivers the value promised on reliable and
predictable schedules.  Being blocked or broken interferes with that.  Having
severe pain whenever you try to update a third-party dependency also interferes
with that.  Both sides of the spectrum can contribute to, or subtract from,
that success.  Each optimizes for a different "common case".  In some ways, a
better name for this conversation might be "A Tale of Two Cultures", because
the arguments for one choice over the other aren't as much about technical
aspects as they are social and cultural ones.  You have to ask yourself these
questions:

* How do I want my teams to share code?
* How do I want to organize my teams?
* How independent do I want my teams to be?
* Which is worse, being blocked, or being broken?
* Which is more important - stability and reproducibility, or simplicity?

====

Title: A Tale of Two Build Systems
Date: 2016-01-20
Tags: qbt, build systems, dependency management, amazon, google, culture
