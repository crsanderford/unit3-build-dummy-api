# unit3-build-dummy-api
A dummy API for the Unit 3 Build.

https://unit3-build-dummy-api.herokuapp.com/

routes:

/reset: drops and recreates the database.

/dbload: loads entries from the .csv file into the database.

/feed GET: returns all entries from the database.
    expected response:
    ```[{'author': 'debacle',
        'id': 10331981,
        'text': "US is not really scared by BRICS at all. They're scared by China, and India maybe, but the other three economies have been pretty handily defused.",
        'tox': 0.1},
        {'author': 'sarciszewski',
        'id': 10343811,
        'text': "I wasn't really trying to argue, they said they didn't understand the point.",
        'tox': 0.05},
        {'author': 'debacle',
        'id': 10331538,
        'text': 'The examples on the homepage kind of underscore how little like Perl Perl 6 actually is.',
        'tox': 0.04},
        {'author': 'debacle',
        'id': 10340097,
        'text': 'No mention of a critical aspect of a service like this: what is the per request load time overhead?',
        'tox': 0.04}]```

/author POST - returns a user's average toxicity, total toxicity, and their top ten most toxic comments.
    expected request body:
    ```{'author': 'sarciszewski'}```

    expected response:
    ```
    {'author': 'sarciszewski',
 'avg_tox': 0.215454545454546,
 'top_ten_tox': [
        {'id': 10336073,
        'text': "Yeah, and also: Who gives a shit? It's the convention they chose, just adapt to it and get over it, or program in a different language. People who like to complain about PHP are rarely the same people who use it every day.",
        'tox': 0.79},
        {'id': 10335393,
        'text': "> TL;DR: people accusing me of being sarcastic are probably missing out on one of the few bullshit-free sources of information on the Internet. My experience with Reddit has been that, like most other places on the Internet, it's a mixed bag. Specifically, some of the moderators are authoritarian dicks (e.g. /r/technology) who evaluate rules without nuance and ban people for sharing a link even when given explicit permission by another moderator to share it. Other subreddits are a bit better (e.g. /r/php), others are probably worse. My opinion of /r/netsec has changed frequently over the past few months.",
        'tox': 0.68},
        {'id': 10313867,
        'text': "A link to this gist really should go in the OP by 'whoishiring. It's damn useful.",
        'tox': 0.66},
        {'id': 10336401,
        'text': 'You\'re the exception, not the rule. I mostly hear C/C++, Ruby, Python, etc. devs complain about PHP. Very rarely actual PHP developers. And typically, their complaints are less of the moan-ass "waaah, they use a \\ for namespace separation" and more "ugh, why don\'t they disabled emulated prepared statements by default"? Only one side is constructive.',
        'tox': 0.61},
        {'id': 10344165,
        'text': 'Doing things the right way is not very illustrative. This isn\'t meant to teach developers how to reinvent NaCl in $langOfChoice, it\'s meant to instill an understanding of the vocabulary. If nothing else, it aims to put to rest stupid phrases like "password encryption". If people copy&paste despite all the warnings, they\'re beyond the help of any blog post. EDIT: In the spirit of being more helpful, I\'ve added links to more complete sample code (on StackOverflow) and made the warnings less obnoxious.',
        'tox': 0.47},
        {'id': 10338225,
        'text': "Even if we adopted identical laws, the government would just ignore them. We're a nation of criminals.",
        'tox': 0.29},
        {'id': 10346484,
        'text': 'Yay, new djb slide deck. (I actually enjoy reading the work he and his colleagues produce.)',
        'tox': 0.22},
        {'id': 10321030,
        'text': "No, the absolute best filter is being a convicted federal felon. The few that I've worked with despite this fact have actually been pretty decent.",
        'tox': 0.11},
        {'id': 10349027,
        'text': '> abolish the security industry Good. Then I can focus on building valuable stuff without having to worry about security.',
        'tox': 0.09},
        {'id': 10319837,
        'text': 'Does this help?  https://scott.arciszewski.me/blog/2014/08/technology-recruit...',
        'tox': 0.08}],
 'total_tox': 4.74,
 'tox_rank': 1}
    ```