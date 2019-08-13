# What is Engineering Work Product?
# March 21st, 2016

Software engineers come in a veritable cornucopia of flavors these days.  You have
your low-level kernel developers, your algorithms-heavy backend Java engineers, your
expert-CSS-tweaking front-end engineers, your full-stack engineers who work on a
web application from end to end, and specializations like tools engineers,
DevOps engineers, scale engineers, the list goes on.  When I think about the
work of telling computers what to do, I like to think first about the topics
that every single one of these roles deals with.  What is the overlap?  One
important aspect of software engineering that concerns every one of us is the
question "What is, and what is not, part of our work product?"

In the early days of computers, programs were just 1s and 0s.  Helplessly
coupled to the hardware architecture that documented which 1s and 0s meant add,
subtract, multiply, etc., a program was almost inseperable from the hardware it
was written on.  A good argument could be made that the work product was
in reality a functioning machine that did whatever the goal was.  An engineer
obtained a piece of hardware, put 1s and 0s into it using toggle switches,
cards, keyboards, or whatever - and the result was a machine that performed
certain calculations or responded to inputs with the desired outputs.

The next step was some of the early portable programs.  Once a program could
truly be expected to be written once, then run on multiple different types of
hardware, it changed this perspective significantly.  This allowed a person who
was not the engineer that wrote the software to understand, deploy, and configure
the software.  Now the software itself had obvious value, and the complete
working system was less important because it could be easily recreated from the
software.

However, what does it take for an engineer to understand, deploy, and configure the
work of some other engineer?  How can we make that easier, less costly, faster?
Our industry has (mostly) realized that not all software is equal in these
tasks.  Industry best practices began to form to optimize "mantainability".
Simplicity became a virtue in its own right because of the advantages it confers
in this respect.  There is a growing focus on code style - code should be easy
to read as well as correct and fast.  Sometimes readability is even more
important than performance!  What happens when there isn't a comment on a line
of code?

Well, you can *blame* that line of code to see the commit message it was
committed with.  Also, the other changes that are part of the same atomic commit
might give you a clue.  Check out this diff below from the QBT project:
```
    commit df424f561e00c0046ac74bd68374486db995399c
    Author: Keith Amling <amling@palantir.com>
    Date:   Tue Feb 23 13:39:42 2016 -0800
    
        Include intercept even the first time.
    
    diff --git a/app/main/src/qbt/build/PackageMapperHelper.java b/app/main/src/qbt/build/PackageMapperHelper.java
    index e13a7fe..9d99b99 100644
    --- a/app/main/src/qbt/build/PackageMapperHelper.java
    +++ b/app/main/src/qbt/build/PackageMapperHelper.java
    @@ -81,6 +81,7 @@ public final class PackageMapperHelper {
                             artifactResult = artifactResult.transform((input) -> {
                                 return artifactCacher.intercept(scope, bd.v.getDigest(), Pair.of(bd.metadata.get(PackageMetadata.ARCH_INDEPENDENT) ? Architecture.independent() : arch, input)).getRight();
                             });
    +                        result = Pair.of(artifactResult, result.getRight());
     
                             checkTree(bd, " after the build");
```

The added line is unclear by itself, but in the context of the commit message,
it is much clearer.  Imagine if this change was folded into a larger change that
did 5 different unrelated things ... especially imagine if this diff had a ton of
needless whitespace changes, text-wrapping changes that held no semantic
difference, or style changes (like moving curly braces to different lines).
Understanding what it does, and what it does or does not have to do with the
other changes in that commit, would be extremely confusing.  Something as simple
as trailing commas, and putting close-parens on the next line, can make a big
difference.  Which of these commits is clearer?
```
    commit 686bdad864e087fe1c084a56dce33f1285c3159f
    Author: Carl Myers <cmyers@cmyers.org>
    Date:   Fri May 20 11:06:49 2016 -0700
    
        bad
    
    diff --git a/Foo.java b/Foo.java
    index a8a0121..37bc008 100644
    --- a/Foo.java
    +++ b/Foo.java
    @@ -6,7 +6,8 @@ class Foo {
             callSomeMethod(
                     arg1,
                     arg2,
    -                arg3
    +                arg3,
    +                arg4
             );
         }
     }
    commit 6522701bcc5461d612716f78f965e7b235a18885
    Author: Carl Myers <cmyers@cmyers.org>
    Date:   Fri May 20 11:07:45 2016 -0700
    
        good
    
    diff --git a/Foo.java b/Foo.java
    index 62bdc6f..7f81afb 100644
    --- a/Foo.java
    +++ b/Foo.java
    @@ -7,6 +7,7 @@ class Foo {
                     arg1,
                     arg2,
                     arg3,
    +                arg4,
             );
         }
     }
```
So now we are thinking about engineering work product as including commit
messages, and even the very structure of your commit graph.  Are you changes
broken up into atomic, easy-to-understand commits?  Do commits that depend upon
each other correctly appear related in the commit graph?  Can you see clearly
when concurrent development diverged, and then when integration work happened to
join independent lines of development back into a unified release?  All of this
is key to producing clear, easy-to-understand, easy-to-maintain codebases.  This
is why a software engineer must be concerned with not just the current code, but
the history of the code in its entirety.  Context matters, and so history
matters.

====

