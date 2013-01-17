.. _changelog:

ChangeLog
=========

0.6.0
-----


 - forked by Johannes Spielmann at http://github.com/shezi/eventlog)
 - friendlier import
 - made parameters optional
 - removed PUSHER support (see original eventlog for that, http://github.com/eldarion/eventlog)
 - add logging switch
 - switched to GPL license

0.5.5
-----

- use `django.utils.timezone.now` instead of `datetime.datetime.now` for timestamp


0.5.4
-----

- when a user is deleted set FK to null instead of losing data

0.5.3
-----

- bumped version on django-jsonfield


0.5.2
-----

- added docs


0.5.1
-----

- initial release
