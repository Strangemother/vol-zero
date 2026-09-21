# Discussion

I've been asked the question 'why' - spending a lot of time on a compiler, of which is clearly not as expressive or mature as every other compiler available, listing C/C++, GO, ASM, BASIC... the list continues. Indeed I've already spend many years on the thought, scratching broken concepts and hating code for a few months. However when I was a an egg I was captured with understandig computing at its core and I've always wanted to trully build my own language and stuff. Just for the bragging rights know-doubt but it's an excpetionally fun challenge to attempt a cliff of new ideas when research 'what is a pc'...

One day someone challenged me with a statement "you cannot build a an OS with python". As python is one of my favorite languages I felt jaded by this and set about seeing if it's possible. Indeed I agree it's a silly idea and does weigh with and fortitude; however is it possible?

This question grips me with a lot of theories. When someone stated "it can't be done..." I set about proving to myself if that's true. A simple but obtuse statement; I was once told man will never fly - or course they corrected themselves "without a plane" when I rebuttled. And today we have wing suits and hove boards and jet packs... In a lot of cases I take up this challenge with python.

Can I build an OS with pure python? No. Python needs a runtime environment. But I feel that's a minor proxy to the overall goal. In response, I question - can someone build an OS with C? Technically no. As C also compiled down. So what's the lowest language? I feel you asking - knowning full-well it's ASM. But it's not. Is it HEX? nope. Bits? Binary? Nope; microcode.

So. Aside from Linus and the mad hats at Intel; no one really writes true, core, bare-metal machine code.

##

Therefore why is this a fun project? As I feel code could go as low as I want (ASM is almost bare metal) and  compounding to another case of wanting to own the core machine, I can write it in python.

Why python? It's lovely. I've tried C, C++, ASM, and JS. Surprisingly the JS was a great platform. But linguistically I want to throw my high-level structures into a lower-level, without specifying the throughput on my development process. Although C is the optimal choice, It's still a different language and comes with its own burderns. MS VS Is amazing and deletes much of the build work, but with examples like 'pyMCU', I know it's possible to write low-level code with a cleaner high-level syntax.

Python to ASM, has been done many times and there are a lot of libraries to cater for this. But my end goal is to build a framework allowing me to abstract the terminology of CPU commands into a cleaner call-set, Then use that to write extremely low-level such as bootloaders. In addition I done want to depend on a specific builder or hook tools.

Therefore the compiler should create clean, flat, explicit asm - compiled by the chosen environment builder such as NASM.
