# The Importance of Build Reliability
## January 28th, 2016

[Last time](2016-01-27-Better-Debugging-Through-Socratic-Method.html)
I wrote about the Socratic Method and how it applies to debugging.
For many engineers, the most important revelation comes simply by realizing
that they DO have the power to "figure it out" by asking the right questions,
not giving up, and insisting on a methodical approach.  Sometimes even more
senior folks who ought to know better, however, don't act this way.  Today I'm
going to share my thoughts on one reason why I think this happens.  I believe a
very common cause of this failure is, believe it or not, a faulty build system.
Let me explain.

When one sits at a computer 8+ hours a day running the same build, writing code
in the same technology stack, one starts to learn all the quirks.  Developers
know the ins and outs of their own tools.  When those tools occasionally do
things unexpected, developers notice this.  When the libraries a developer's
software depend upon are flakey or unreliable, a developer notices.  When the
build is frequently broken by coworkers who seem not to care, and builds are
left red for hours or days without so much as a "sorry" email, developers
notice.  So when **your** build breaks, and you have noticed all of these
things, what is your first thought?  Not "gee, I guess I have a bug".  Not "I
wonder what I've done wrong this time".  No, when you are a developer who has
noticed all the things I just listed, your first throught is "oh, great,
someone *who is not me* broke the build".

Rather than your first questions (again referring to my previous blog post
about debugging) being "how could my code be broken", instead, developers ask
"how can my code be absolved of this crime?".  "How can I blame the culprit
*who is not me*?".  It is difficult to fully capture the toll this has, the
very real cost every developer pays, for living in a world such as this.  And
wost of all - they aren't wrong to do so!  In the world I described, the
majority of the time, the build **is** broken, and by someone *who is not
you*.  Now think for a moment about how much more productive your developers
could be if you could make the build be broken only half as often as it
currently is!  Imagine the visceral difference felt by engineers when every time
they run a local build and it fails, their own experience tells them they can be
99% certain it is because THEY broke it, nobody else.

The first step to accomplishing this is what I call "unbreakable" builds.  Some
people call them "pre-commit checks" or in today's DVCS world, "pre-merge
checks".  They are implemented in the open source world by many different
tools, some free and some commerical.  Examples that support github include
TravisCI and CircleCI.  A completely free open-source, inside-the-firewall
solution can be built with Gerrit + Jenkins + some plugins.  If you already pay
for Atlassian's Bitbucket Server, you can get the free and open-source Stashbot
plugin (full disclosure: I am the author of the Stashbot plugin) to get "inside
the firewall" unbreakable builds.  The thing about unbreakable is, it doesn't
work if you don't have quality tests.  If your tests never detect anything
useful, it's just a waste.  If your tests flake frequently or get
false-positives all the time, people will be blocked from committing perfectly
good code, and people will stop believing the tests when they do raise a real
failure.

I watched Palantir (my previous employer) grow from a company of under 200
people to over a thousand people, the large majority of whom were software
engineers, whether backend or front-end, or deployed on site with customers.
Somewhere between 200 and 400 engineers, we implemented unbreakable, and it
changed **everything**.  It literally changed how people worked.  Remember,
hardware is cheap, engineers are expensive.  Instead of a developer starting a
local build, then going to read a web comic, or grab a cup of coffee, or some
other context switch, a developer would make a test commit, push it to a user
branch, and wait to see if it passes or not.  The build and tests run on a
beefy, super-fast build node.  The results come in faster, and more
importantly, the user's dev machine is free to start working on the next
commit.  Combined with git's famous talent for rapid context-switching (via
"git stash" and user branches) people became **drastically** more
productive.  Another important difference is, because no code can be committed
that hasn't successfully built, our "release" build (the post-merge build) was
almost always green.  Contrast this with before unbreakable, where people would
frequently send out emails "hey, does anyone know why the build is red?" or
worst of all, "Nobody update!  the master branch is broken!  I'm working on a
fix now!".  Before unbreakable, we were also on subversion, so pushing a bad
commit to the main development branch could break everyone terribly.  In
Subversion, you run "svn update" and it takes whatever changes have been made
and shoves them into your workspace, merging with your current work (and
riddling your workspace with conflict markers if needed), and there is no way
to "undo" it.  This means commiting a break could grind development to a
standstill leaving everyone who has updated unable to build.  It's easy to see
from this why unbreakable builds made such a huge impact at Palantir.

Unbreakable builds go a long way and are by far the lowest hanging fruit
available to any software shop that does not already have them.  There are many
other ways a build can be unreliable or unreproducible though.  A problem we
fought bitterly to overcome at Amazon, circa 2008, was related to
reproduciblity.  Even back then Amazon had an advanced custom build system
which worked very hard to ensure that every package built cleanly by depending
only on the other packages it explicitly asks for, allowing builds to be
reproducible.  Unfortunately, the system was pretty complex, every team had to
write their own package's build configuration (and sometimes, build code).
Experts on the build system were in high demand and short supply.  So, people
would write build code which relied upon environment variables, or made
assumptions about the machine the build was running on which were correct on
their desktop, but not correct on the official build nodes.  The build team got
several support requests per week that basically amounted to "my build works on
my desktop, but fails on the build nodes, what gives?" and the answer was
almost always (paraphrasing, of course) "you did something stupid", and almost
never "thanks to you, kind sir or madame, you have helped us identify a failure
in our infrastructure!".

How did we mitigate this problem?  Largely through user education, in this
instance.  Our build system already did what it could to prevent users from
doing things that were not reproducible, but by writing careful troubleshooting
documentation that helped people identify the problems themselves and
entreating people to read that documentation before filing a support request,
we delivered a better outcome to everyone.  And builds began to be percieved as
more reliable!  When a build failed on the build node, people learned to ask
"what might I have done that only works on my machine" instead of "why is their
infrastructure broken?  It worked for me!".

In my relatively unremarkable career of just over a decade of build system
engineering, I've seen a lot.  On one hand, I've seen developers fight their
own build system to get things done.  On the other hand, I've seen developers
lifted up by their build system able to accomplish astonishing tasks in a
single caffeene-fueled weekend.  I've seen companies say they can't afford to
drop everything and rewrite their build system, and I've seen companies realize
they can't afford **not** to rewrite.  I've seen expatriots of Google,
Amazon, and others say "I can't believe how hard it is to accomplish anything
here, this sucks".  I've even seen people reach the point where after leaving a
big-name company like that, they end up going back because writing software
there is "a joy" (and it's all because of the tools and development ecosystem).
On the other hand, I've seen developers say "I don't know how I'll ever write
software again outside of this company, the tools are so great".  Which one of
these groups can recruit and retain the best talent?  Which one of these groups
do you want the company you work for to belong to?  Which one of these will make
your company more successful?

====

