========
eventlog
========

``eventlog`` is a simple app that provides an easy and clean
interface for logging diagnostic as well as business intelligence
data about activity that occurs in your site.

Each event you log gets added to the your database. You can use the Django
admin interface to review your events.

=====
Usage
=====

For each event you want to log in your code, simply put a call to the ``log_event`` function. You must supply a label
for the event. You will use this label to review and filter your events later in the database. You can select any
string you like as a label, but I suggest you use something distinctive and recognizable. The logging framework will
automatically add the datetime to your event and save it into the database.

Let's construct a sample where you would log the user logging in and out

::

  >>> from eventlog import log_event
  >>> log_event("USER_LOGIN")
  <Event: 2013-01-31 23:16:30.522918+00:00 0000000000000010 USER_LOGIN>
  
While that output itself isn't very useful, these events are saved in the database and can be accessed via the admin
or used to to aggregation and intelligence. By the way, that number is the event id.

You can add a message to the event to stay with the same label but add additional information. This will help you
filter your events later on::

  >>> from eventlog import log_event
  >>> log_event("USER_LOGIN", message="logged in")
  <Event: 2013-01-31 23:22:33.205591+00:00 0000000000000011 USER_LOGIN - logged in>
  >>> log_event("USER_LOGIN", message="logged out")
  <Event: 2013-01-31 23:22:38.501487+00:00 0000000000000012 USER_LOGIN - logged out>

You can also attach a user to the event and add extra information. These are given as the ``user`` and ``extra``
arguments::

  >>> from eventlog import log_event
  >>> from django.contrib.auth.models import User
  >>> user = User.objects.get(id=1)
  >>> log_event("USER_LOGIN", message="logged in", user=user, extra={'source': 'mobile client'})
  <Event: 2013-01-31 23:25:14.607540+00:00 0000000000000013 USER_LOGIN (user: root@example.com) - logged in {'source': 'mobile client'}>

The extra information gets stored in a JSON field and must therefore be JSON serializable.

Finally, it can be very useful to log an event for Django signals. For our example, we'd add a signal handler for user
login and logout::

  import logging
  from django.dispatch import receiver
  from django.contrib.auth import signals
  from eventlog import log_event

  @receiver(signals.user_logged_in)
  def handle_user_logged_in(sender, **kwargs):
      log_event("USER_LOGIN", message="login", user=kwargs.get("user"))
        
  @receiver(signals.user_logged_out)
  def handle_user_logged_out(sender, **kwargs):
      log_event("USER_LOGIN", message="logout", user=kwargs.get("user"))

Depending on your logging settings, you might notice output after you call ``log_event`` in the console. This output
comes from the Django logging system. All events you create are automatically fed to the normal Django logging system
and might produce output. This way, you don't have to call logging twice, you can simply log your events and have the
information show up in your normal server logs as well, which is also nice for debugging in the Django runserver. If
you don't want your events logged, simply pass ``django_log=False`` to any of the event functions and that event will
not be sent to the logger::

  >>> from eventlog import log_event
  >>> log_event("PUBLIC EVENT", message="our admins will probably see this")
  INFO 0000000000000015 PUBLIC EVENT - our admins will probably see this
  <Event: 2013-01-31 23:30:24.616683+00:00 0000000000000014 PUBLIC EVENT - our admins will probably see this>
  >>> log_event("SECRET EVENT", message="that will not be logged", django_log=False)
  <Event: 2013-01-31 23:30:42.024606+00:00 0000000000000015 SECRET EVENT - that will not be logged>

The events are sent to the logger ``eventlog``. To see the output of that logger, try these settings::

  LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'simple': {
              'format': '%(levelname)s %(message)s'
          },
      },
      'handlers': {
          'console':{
              'level':'DEBUG',
              'class':'logging.StreamHandler',
              'formatter': 'simple'
          },
      },
      'loggers': {
          'eventlog': {
              'handlers': ['console', ],
              'level': 'INFO',
              'propagate': True,
          },
      }
  }

Of course, you can log events at every logging level, by using the supplied functions: ``log_debug``, ``log_info``,
``log_warning``, ``log_error``, ``log_fatal``. Additionally, you can use ``log_event`` as shown above, which is the
same as ``log_info``, or ``log_critical`` which is the same as ``log_fatal``.


Exception logging
*****************

There's one more convenience function you can use: ``log_exception``. This function is a handy shortcut that will
capture the exception traceback for you. For this reason, you must not use the function outside of an exception
block: it will fail!

Here's a sample usage for ``log_exception``::

  >>> from eventlog import log_exception
  >>> try:
  ...     raise Exception()
  ... except:
  ...     log_exception("USER_LOGIN", message="login failed")
  ... 
  <Event: 2013-01-31 23:39:02.812958+00:00 0000000000000016 USER_LOGIN - login failed {'exception': 'Traceback (most recent call last):\n  File "<console>", line 2, in <module>\nException\n'}>

By default, the exception is logged as a ``logging.WARNING``. You can change that by adding a ``level`` to your call::

  >>> import logging
  >>> try:
  ...     raise Exception()
  ... except:
  ...     log_exception("USER_LOGIN", message="login failed", level=logging.ERROR)
  ... 
  ERROR 0000000000000018 USER_LOGIN - login failed {'exception': 'Traceback (most recent call last):\n  File "<console>", line 2, in <module>\nException\n'}
  <Event: 2013-01-31 23:41:19.161593+00:00 0000000000000018 USER_LOGIN - login failed {'exception': 'Traceback (most recent call last):\n  File "<console>", line 2, in <module>\nException\n'}>

All other arguments apply too, so you can add ``message``, ``user``, ``extra`` and ``django_log``.


============
Installation
============

The simplest way to install eventlog is using pip, directly from this git repository::

  pip install -e git://github.com/shezi/eventlog.git#egg=eventlog


=======
Credits
=======

 - eventlog was first developed by Eldarion, Inc, http://github.com/eldarion/eventlog
 - Additions were developed by Johannes Spielmann, http://github.com/shezi/eventlog

=======
License
=======

Copyright 2011, 2012, 2013, Eldarion, Inc. (https://github.com/eldarion/eventlog)

Copyright 2013, Johannes Spielmann (https://github.com/shezi/eventlog)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
