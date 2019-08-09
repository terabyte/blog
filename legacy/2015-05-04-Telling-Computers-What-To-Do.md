# Telling Computers What To Do
## May 4th, 2015

Two of my favorite sayings are, "I tell computers what to do for a living," and,
"Computers do what you tell them.” Most non-technical folks find these sayings
funny or quaint, but they mean something very specific and important. When a
user says that the computer deleted my file, there are only two things they can
mean. He or she told the computer to delete the file, or someone else told the
computer to delete the file. Saying that computers do what you tell them,
reminds even the most technical people that computers are, with very few
exceptions, deterministic, predictable, and reliable. Which means when they
don't do what you expect, it is not only likely to be your own fault, but also
absolutely in your power to fix it.  Always.  Because computers do what you tell
them.

Of course, the point isn't to provide apologetics for why today, after 60+ years
of computer science, it is still so very hard to get computers to do what you
want. In fact, in many ways it is harder than ever before. This is about a deep
truth of how computers work. When a junior engineer says, "It won't do X," or,
"I can't make it do X," what they mean is, "Something is going on that I don't
understand." But, you CAN understand it if you can figure out what questions to
ask, and how to ask them. You don't have to ask your boss or your mentor or your
technical support line - you can ask your computer.  Presumably, it knows. As we
experience progress, and experience increasingly complex hardware running
increasingly complex operating systems running increasingly complex application
stacks written in increasingly complex higher-level programming languages, our
understanding of the computer becomes more and more opaque, confusing, detached,
and mysterious. We must fight that inaccurate view, however, because underneath
that complexity still beats the 3-billion-times-per-second frequency of a
deterministic, finite-state machine that would have made Alan Turing proud.

Much like wrong answers on an essay question in English class, there are
and uncomfortably many ways a computer might break your expectations and
manifest an apparent failure to do what you think it should.  There are a quite
finite number of things, however, that could be the underlying cause, and
narrowing it down is the first step to fixing it.  Figuring out that underlying
cause, quickly and methodically, is what separates the good engineers from the
great ones, and what contributes to those few who are 10x or 100x engineers.

In the olden times, everything about a computer was laid bare, and your typical
computer operator could describe the state of every register and exactly what
the computer was doing.  You couldn't do much without this deep level of
understanding.  Today, things are not like that.  I don't know how a BIOS
works.  I'm not sure what happens when I press the power button on my laptop
and the electronics whir to life to complete their Sisyphean task of delivering
me pictures of cats falling into water and looking pretty unhappy about it, but
I am grateful that it works.  Somehow, all the registers go from random states
of not having enough electrons, to an appropriate, deterministic state where the
completely non-physical emergent phenomenon we call an operating system can
birth itself from the chaos.  I also don't know exactly how my operating system
works, but since I use Linux, which is open-source, at least I can *look* at
the code and try to figure it out.  "One of these days..." I always say... and
that is just one layer.  You probably don't know how your hard disk works.  You
probably don't know how your keyboard delivers I/O to your OS.  You probably
don't know how your CPU manages processes or memory.  You probably don't know
how your kernel's network stack delivers requests to and from applications like
your web browser.  You probably don't know how the video website's client-side
code makes continuous requests to refill its buffer with video as it plays, so
the cat falls gracefully into the water and does not stutter.

This is why people personify computers.  They are as inscruible to us as the
network of billions of neurons in your brain that conciousness mysteriously
arises from.  This is why people think "they" do "things" to "us".  Today, a
single person trying to understand everything about their computer seems more
like a person trying to know the state of every neuron in a living brain (how
would that work?  Think about it).

I know people who I consider to be 10x engineers.  Their talent amazes me.  How
do they always seem to know?  How do they run circles around the rest of us,
and just **get so much done**?  From my experience, my guess is that they
ask the right questions, and they ask it of the right entity - their computer.
They (often) don't settle on shoving random print statements into code - they
lay the entire thing bare with a debugger.  They read **and understand**
every line of code between the moment they press "enter", and the moment the
computer "does something wrong".  And I think they do this because they
understand that "computers do what you tell them".  Whatever is wrong, it has
to be in there somewhere.  I mean, short of a bad motherboard or some spotty
ram.  And good engineers think about that too.  I knew one who, after losing an
**entire week** debugging non-deterministic behavior, only to find the ram
in his new machine was faulty, swore that he would run memtest86 on every new
machine he bought or got from work annually, for all time.  For the price of a
few hours of burnin when he wouldn't have been using it anyways, he can save
himself countless hours of wondering if he is, in fact, taking crazy pills (a
detrimental state to find oneself in for certain).

So what is my advice to those who would tell computers what to do for a living?
The next time the computer doesn't seem to be listening, maybe you should be
the one who is listening, and asking the right questions.  Have you read the
logs?  What versions of the software are you using?  What has changed since it
worked last?  Can you examine the source code?  Can you examine the state of
the memory?  Does it fail deterministically?  If not, can you detect a pattern
in the failure?  Can you produce a simplified reproduction of the bug?  Maybe
you need to invest some serious time to answer some of these questions.  Maybe
you need to write a debugger or disassembler.  Maybe you even need to go learn
assembly, or Java bytecode.  Your boss should be happy to "pay" you for your
time in these endeavours, because the time you spend today writing these tools
or learning how these tools work, instead of "jiggling it until it works", is
paid back to your and your employer tenfold, or even a hundred fold, and those
are dividends worth having.
