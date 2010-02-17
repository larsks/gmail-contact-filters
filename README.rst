=====================
GMail Contact Filters
=====================

The ``generate_group_filters.py`` will generate a Gmail filter expression
for all groups (optionally specific groups) you've defined in Google
Contacts.  You can copy and paste these into Gmail to create the
appropriatae filters.

Usage
=====

For the default behavior::

  generate_group_filters.py

You may also specify the following options::

  -h, --help            show this help message and exit
  -f CONFIG, --config=CONFIG
  -g GROUP, --group=GROUP
  -m MAX_RESULTS, --max-results=MAX_RESULTS

Configuration
=============

The ``generate_group_filters.py`` script requires an ini-style
configuration file with your Google credentials.  It should look like
this::


  [google]

  username = your_username
  password = your_password

The script will look for a file called ``google.ini`` in your current
directory by default; you may specify an alternate one with the ``-f``
command line option.

