# Better Debugging Through the Socratic Method
## January 27th, 2016

From personal experience, and from observing others, I think many engineers are
disposed to go through the various (now mostly debunked) "stages of grief",
when facing a tough debugging challenge, or when working on a feature or bug
which is particularly tough or confusing.  Here is what my cubicle-neighbors
hear at least a few times a week:

* Disbelief - "what?  Run it again, see if it still doesn't work"
* Anger - "Why is this @#%@# thing not working?  It worked yesterday!  I didn't even change anything major!"
* Bargaining - "Maybe if I just revert my latest commit... maybe if I do a build clean..."
* Depression - "All is lost.  These results are impossible.  This doesn't make any sense.  I hate my life."
* Acceptance - "It's going to be ok.  If we slip a day or two, my manager will understand.  Nothing is impossible.  Computers do what you tell them."

In fact, one of my favorite catch phrases, "[Computers do what you tell them](2015-05-04-Telling-Computers-What-To-Do.html)",
is a thinly veiled attempt to move myself or others along to the last
stage more quickly.

Why is this observation useful?  Because debugging is hard, but using the right
approach can make it easier.  It is very difficult to use the right approach
from a state of disbelief, anger, bargaining, or depression.  Computer Science
is much like any other STEM field, it relies heavily on the scientific method.
The code you write is a hypothesis, and a functioning program is your
successful experiment supporting that hypothesis.  When your program
misbehaves, it is like a negative result - something about either your
hypothesis or your experiment is mistaken.  To understand that requires belief
revision, and that is where the Socratic Method comes in.

The Socratic Method is a dialog (possibly with yourself) with the goal of
finding contradictions that follow from your hypothesis (thus, weakening it, or
allowing you to produce a stronger, more correct hypothesis).  It is the core
of the scientific method, named for Socrates, and attributed to him by
Aristotle, a later protégé of his teachings.

Let's say I wrote the following lines of code:
```
    Integer[] numArray = { 1, 2, 3 };
    ImmutableList&lt;Integer&gt; nums = ImmutableList.of(numArray);
```

This relatively simple code looks like it ought to work; unless you are a Guava
expert you might not see the mistake.  When it inevitably fails to compile
(thanks, strict type checking!) the error message tells you exactly what is wrong, but not necessarily how to fix it.

```
    Type mismatch: cannot convert from ImmutableList&lt;Integer[]&gt; to ImmutableList&lt;Integer&gt;
```

Instead of bashing our head against this, we can have a socratic dialoge with
ourselves.  First, a hypothesis: "ImmutableList.of(numArray) takes an array of
integers and converts it to an immutable list of integers."  How could this
statement be wrong?  One way it could be wrong is it could be returning some
other type besides an immutable list of integers - my assumption about how the
API works could be mistaken.  How do we test this?  In Java, we can do
something like this:

```
    Integer[] numArray = { 1, 2, 3 };
    System.out.println(String.valueOf(ImmutableList.of(numArray)));
```

What does it print out?

```
    [[Ljava.lang.Integer;@2d38eb89]
```

In case you aren't a Java expert either, this is what the Object.toString() method prints for an ImmutableList&lt;Integer[]&gt;.  For example, this code:
```
    System.out.println(String.valueOf(ImmutableList.of(numArray)));
    System.out.println(String.valueOf(numArray));
    System.out.println(String.valueOf(ImmutableList.of(1, 2, 3)));
```
prints out this:
```
    [[Ljava.lang.Integer;@2d38eb89]
    [Ljava.lang.Integer;@2d38eb89
    [1, 2, 3]
```

The list's "toString()" method prints out a set of brackets and comma-separated
values, and an integer array prints out a single starting bracket followed by
"L" and the java type of the array, so we can see that the type returned by the
ImmutableList.of() call is in fact a list of Integer arrays, not a list of
integers.  The reason the API is designed this way is that
ImmutableList.of(numArray) could mean the user wants to turn numArray into a
list, but it could also mean they want to make a list whose first item is an
array of integers.  The ImmutableList API includes ImmutableList.copyOf() for
this exact reason, to distinguish between these cases.  The corrected code is:
```
    Integer[] numArray = { 1, 2, 3 };
    ImmutableList&lt;Integer&gt; nums = ImmutableList.copyOf(numArray);
```

Now it compiles and works correctly!  In essence, we "asked the computer
questions" such as "what is the return type of this call" and "what does the
expected return type look like" to help convince ourselves our code was correct
- or discover how it was mistaken.  The key step here, as always, was figuring
out which questions to ask.  This is also the hardest part of the Socratic
Method when applied in philosophy or debate as well.  It isn't always obvious
what questions will lead to a "contradiction", but that is what you are looking
for.  Start with the most obvious things but keep going.  "When you have
exhausted all plausible explanations, whatever remains, no matter how
improbable, must contain the truth".  In computer science, you generally go
through the list in this order:

* There is a typo in my code
* There is a bug in my code
* There is a bug in my algorithm
* My code or algorithm assumes something untrue
* There is a bug in some other code I depend upon
* There is a bug in the operating system, web browser, or software elsewhere in the stack
* There is a bug in the hardware itself - or the hardware has gone bad
* Cosmic Rays / Electrical Interference / Supernatural Intervention

Use these "ways I might be mistaken" to help form the questions you should ask
of yourself.  For the earlier ones, sometimes you can convince yourself that
isn't how you are mistaken by simple inspection ("I double-checked, there are
no typos").  For more difficult or obscure "ways to be wrong", such as a bug in
your algorithm, you might need to produce a simplified reproduction of the
error, or write a suite of tests to exercise the code to convince yourself it
ought to work.

You don't start blaming cosmic rays until you are damn sure you have eliminated
with a high degree of certainty every single item above it.  This is how
science figures out why things happen ([Occam's Razor](http://en.wikipedia.org/wiki/Occam%27s_razor)), and
this is how Computer Scientists figure out why their code doesn't work (use
Occam's Razor to [Shave the Yak](http://en.wiktionary.org/wiki/yak shaving).

====

