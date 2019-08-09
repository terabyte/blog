# New System76 Oryx Laptop Setup
## December 1st, 2015

So it's time once again to play the laptop setup game.  This time, I'm going to document it to make it easier next time.  My new laptop is the System76 Oryx Pro.  This bad boy has the new Intel Skylark (14nm process) CPU, 64GB of ram, and a 512GB M.2 PCIe SSD, plus a *beautiful* 17in screen and the ability to drive 3 external monitors (**in addition to** the built-in panel).  It came preinstalled with Ubuntu 15.10.

So the first task is to test everything.  If something doesn't work, I need to know it before I go mucking around and customizing things.  Then, and only then, can I burn the evil ubuntu install to the ground and install my distro of choice, Debian, including full disk encryption (look at the year, it's almost 2016, gotta encrypt that shit).

On that subject, let me expound briefly on why full disk encryption is completely necessary.  If you do not have full disk encryption, and instead only encrypt your home partition (or, even *worse*, only encrypt a "Secure" subdirectory of your user's home), you are vulnerable to many attacks.  You lack plausible deniability (hidden volumes, inability to estimate how much of your disk is used, etc).  More importantly, nothing protects your operating system from being compromised.  An entity with access to your laptop twice can simply backdoor your OS (which for a professional takes only seconds of access), then sit back and wait for you to unlock your encrypted partition, leaking all your data or keys for later perusal.  The best way to be secure is to have full disk encryption, a strong user password, and a reliable screensaver with password lock.  The "more paranoid" should always shut down their laptop before letting it leave their presence, rather than just using the sleep, because some kernel exploits may allow access even while a screensaver is running.  Also, make sure your screensaver is up to date, there are [many known problems](https://www.jwz.org/blog/2015/04/i-told-you-so-again/) with linux screensavers relating to security.

Back on track.  From my testing, in the stock Ubuntu install, I observed the following:

* All function keys (disable trackpad, turn LCD on/off, brightness, keyboard backlight, sound volume, etc) worked perfectly out of the box.  This seems like it should be a given but you'd be suprised how often that is not true for linux laptops.
* The machine should sleep and wake up correctly - we are truly living in the glorious Linux future when this works.  I had some difficulty with the resume process hanging or being very very slow, but I did an `apt-get update && apt-get dist-upgrade` and rebooted with a shiney new kernel and everything started working flawlessly.
* The sound should work.  Linux sound is pretty firmly in the "just works" camp these days, but you should absolutely make sure.
* Confirm what video driver you have with `lsmod`.  I unsuprisingly had `nvidia`, the proprietary non-free driver for my laptop's nvidia card.  This used to be a tragedy, but I went on to test and everything worked out to the best of my ability to observe.  Specifically, I was able to attach external monitors, which were immediately detected on the fly.  I was able to drag windows between monitors.  I was able to run arandr to configure my monitor resolution and relative layouts.  This all "just worked".  I am 95% idealist and 5% pragmatist, but the 5% might win out this time if the proprietary driver continues to "just work" after reinstalling my new OS.
* Wifi "just worked", no problem.
* The correct number of CPU Cores and amount of RAM registers (via htop or something similar), and the hard drive size and model looks correct.

With things seemingly working correctly, it was time to burn a new Debian Testing netinst CD, pop it into my usb cdrom drive, and reboot the machine.  I downloaded the netinst ISO from [https://www.debian.org/CD/netinst/](https://www.debian.org/CD/netinst/) and burned it using wodim as follows.
`wodim -v dev=/dev/sr0 -eject ~/debian-testing-amd64-netinst.iso` (this was on my old laptop, the Oryx Pro doesn't have a CD drive - I bought an external USB one just to make this easier though).  I went into the bios, changed the boot order, popped in the cdrom I just burned and restarted the machine.  Debian installer activate!

The first problem didn't take long to hit - the wifi requires a proprietary firmware blob (!!!).  What's the point of "supporting linux hardware" when it only works with terrible proprietary blobs all over.  Worse, it was already installed, so I had no idea what non-free software I was running.  I went off to research what to do about this and it turns out you just use a USB drive, download the blobs, toss the USB drive in when prompted, plug the drive in to your laptop and select "yes" to find them.  Then, hold out hope for a future where you don't have to flush your ideals down the crapper to have the sweetest notebook on the market.  Simply plugging the USB drive in didnt' work, I had to pop over to a virtual console (ctrl+alt+F2) and run "mount -a" to mount it.  Then I flipped back, asked it to search again, and it found the files.

So next comes hard drive setup.  I selected "use entire volume for encrypted LVM" and let it zero out the disk.  After that, it shows the partition layout.  Since I have 64GB of ram, the default of 15GB of swap seems fine to me, but the default of 10GB of root seems small.  I checked my old laptop which I've been using for a few years and it's at 8GB used.  I had chosen 20GB for it before.  Since this includes the /tmp directory, I go for 20GB over 15GB again.  After doing some research, I determined btrfs is "almost ready" for "normal use", but there are still some folks complaining about it so for now I chose to stick to ext4.  Even the ext4 devs say btrfs is "the way forward", so the question to ask is "am I comfortable with how stable it is/isn't?".  Not "if", but "when".  Maybe next time I'll use it.

Next the system begins installing.  When prompted, uncheck "debian desktop environment".  I throw your Gnome on the ground!  I ain't a part of your system.  I include print server, ssh server, and standard system utilities, because we aren't barbarians here.  If I want it, I'll install nginx later, I don't want to find out what they think "web server" means.  I'll install the xorg stuff I want, and not a bloated 3GB Gnome desktop I'll never use.

So next, it says "Install the GRUB boot loader" failed.  Great.  Seems to be because this new machine is using UFEI to boot.  I google around and find [some debian-specific details](http://tanguy.ortolo.eu/blog/article51/debian-efi).  I eventually figured out that the newest debian installer still had a bad regex that did not include nvme devices and thus could not install grub.  I had to boot off a live cd, chroot into my new system, and reinstall grub by hand.  With some difficulty, I eventually made this work.  The debian bug I filed is [here](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=806849) for posterity, and it includes the exact details of my workaround.

So the nouvea driver works fine for normal use, but for multiple monitor support and 3d gaming (i.e. via steam) it is still not there.  I again bit my tongue, swallowed my idealism, and installed the nvidia proprietary drivers without difficulty.  Under the proprietary drivers everything "magically" started working.  I am very angry Nvidia can't be fucked to support the open source driver (even just give them the documentation they need to write their own!), but I am glad the hardware works "at all" (and in fact, quite well).  After a month+ of use, the only remaining thing that worked "out of the box" that doesn't seem to work for me now is the screen dimmer (I'll probably eventually figure that out and update here, because it is important to preserve battery life).

For posterity, here is my complete "post install" setup list:
* Fix capslock key to be control in terminal and X (see details below)
* `apt-get install vim sudo less zsh dc mosh git network-manager alsa-utils lsof strace vpnc screen htop iotop build-essential`
* `apt-get install vnc4server xvnc4viewer arandr xscreensaver xscreensaver-gl xscreensaver-data-extra xserver-xorg fluxbox ratpoison`
* install externally java, google-chrome, tmux/gitscripts, "oh my zsh" and vim stuff
* retest everything above
* Copy over all user data

So, capslock is the devil.  I can barely function on a computer where capslock is not acting as an additional control key.  To achieve this globally (including in terminals outside X) you must do the following.
```
edit /etc/default/keyboard and set:

XKBOPTIONS="ctrl:nocaps"

Then run:

sudo dpkg-reconfigure -phigh console-setup
```
To remap in X11, do the following.
```
setxkbmap -layout us -option ctrl:nocaps
```
You can insert this into your .xinitrc file, your ratpoisonrc, or however you prefer to run crap automatically in X.  For USB keyboards, after unplugging and replugging, you will have to rerun the command.  On some machines, I actually have that set to run every minute in a cron job to make sure I never EVER accidentally get capslock behavior.
